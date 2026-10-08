import streamlit as st
import pandas as pd
import copy

st.set_page_config(page_title="LED Matrix Hex Generator", layout="centered")

st.title("Interactive LED Matrix Hex Generator")

st.markdown("""
### 📖 How to Use This Tool
1. **Grid Setup**: Select your desired grid size (8x8 or 16x16) and your target programming language (C/C++ or Python) from the options below.
2. **Draw your Shape**: Click the individual checkboxes in the **Matrix Canvas** below to turn LEDs **ON** (green) or **OFF**.
3. **Controls**: Make a mistake? Use the **Undo** button to revert. Want to start over? Click **Clear All** or **Delete**. You can also use the preset buttons to quickly load common shapes.
4. **Copy the Code**: As you draw, the code block at the bottom will automatically update with the correct hexadecimal array representation of your matrix. You can simply copy and paste this into your project.
""")

st.divider()

# Grid size selection
col1, col2 = st.columns(2)
with col1:
    size = st.radio("Select Grid Size", [8, 16], horizontal=True)
with col2:
    out_lang = st.radio("Select Output Language", ["C/C++", "Python"], horizontal=True)

# Initialize grid in session state
if 'grid_size' not in st.session_state or st.session_state.grid_size != size:
    st.session_state.grid_size = size
    st.session_state.grid = [[False] * size for _ in range(size)]
    st.session_state.history = []
    st.session_state.editor_key = 0

def save_history():
    st.session_state.history.append(copy.deepcopy(st.session_state.grid))
    if len(st.session_state.history) > 50:
        st.session_state.history.pop(0)

def clear_grid():
    save_history()
    st.session_state.grid = [[False] * size for _ in range(size)]
    st.session_state.editor_key += 1

def undo():
    if st.session_state.history:
        st.session_state.grid = st.session_state.history.pop()
        st.session_state.editor_key += 1

def set_preset(preset_type):
    save_history()
    st.session_state.editor_key += 1
    new_grid = [[False] * size for _ in range(size)]
    if preset_type == "box":
        for i in range(size):
            new_grid[0][i] = True
            new_grid[size-1][i] = True
            new_grid[i][0] = True
            new_grid[i][size-1] = True
    elif preset_type == "cross":
        for i in range(size):
            new_grid[i][i] = True
            new_grid[i][size - 1 - i] = True
    elif preset_type == "smile":
        # simple smile for both sizes
        eye_y = size // 4
        eye_x = size // 3
        new_grid[eye_y][eye_x] = True
        new_grid[eye_y][size - 1 - eye_x] = True
        mouth_y = size - (size // 3)
        for i in range(eye_x, size - eye_x):
            new_grid[mouth_y][i] = True
        new_grid[mouth_y - 1][eye_x - 1] = True
        new_grid[mouth_y - 1][size - eye_x] = True
    st.session_state.grid = new_grid

st.write("### Matrix Controls")
t_col1, t_col2, t_col3, _ = st.columns([1, 1, 1, 3])
with t_col1:
    if st.button("🧹 Clear All", use_container_width=True):
        clear_grid()
with t_col2:
    if st.button("🗑️ Delete", help="Clears the entire grid", use_container_width=True):
        clear_grid()
with t_col3:
    if st.button("↩️ Undo", disabled=len(st.session_state.history) == 0, use_container_width=True):
        undo()

st.write("### Presets")
p_col1, p_col2, p_col3, _ = st.columns([1, 1, 1, 3])
with p_col1:
    if st.button("🔲 Box", use_container_width=True):
        set_preset("box")
with p_col2:
    if st.button("❌ Cross", use_container_width=True):
        set_preset("cross")
with p_col3:
    if st.button("🙂 Smile", use_container_width=True):
        set_preset("smile")

# Prepare dataframe for data_editor
df = pd.DataFrame(st.session_state.grid, columns=[str(i) for i in range(size)])

# Configure columns to just show checkboxes without large headers
col_config = {
    str(i): st.column_config.CheckboxColumn(
        label=str(i),
        default=False,
        width="small"
    ) for i in range(size)
}

st.write("### Matrix Canvas")
edited_df = st.data_editor(
    df,
    hide_index=True,
    column_config=col_config,
    use_container_width=False,
    key=f"editor_{st.session_state.editor_key}"
)

# Detect if user made a change in the UI canvas
current_grid = edited_df.values.tolist()
if current_grid != st.session_state.grid:
    save_history()
    st.session_state.grid = current_grid
    # We must force a rerun so the undo button state enables immediately
    st.rerun()

def generate_hex(grid, size):
    hex_values = []
    for row in grid:
        row_val = 0
        # Bitwise operations to convert boolean row to integer
        for i, bit in enumerate(row):
            if bit:
                # Set the corresponding bit (MSB is index 0)
                row_val |= (1 << (size - 1 - i))
        
        # Format as hexadecimal
        if size == 8:
            hex_values.append(f"0x{row_val:02X}")
        else:
            hex_values.append(f"0x{row_val:04X}")
    return hex_values

hex_array = generate_hex(st.session_state.grid, size)

st.write("### Generated Array")

if out_lang == "C/C++":
    type_str = "uint8_t" if size == 8 else "uint16_t"
    code = f"const {type_str} led_matrix[{size}] = {{\n"
    
    if size == 8:
        code += "  " + ", ".join(hex_array)
    else:
        # Split 16 elements into two rows of 8 for readability
        code += "  " + ", ".join(hex_array[:8]) + ",\n"
        code += "  " + ", ".join(hex_array[8:])
    
    code += "\n};\n"
    st.code(code, language="cpp")
else:
    code = f"led_matrix = [\n"
    
    if size == 8:
        code += "  " + ", ".join(hex_array)
    else:
        code += "  " + ", ".join(hex_array[:8]) + ",\n"
        code += "  " + ", ".join(hex_array[8:])
    
    code += "\n]\n"
    st.code(code, language="python")

st.markdown("""
---
### 💡 How LED Matrices Work
LED matrices are usually controlled using a technique called **Multiplexing**. Instead of dedicating a single microcontroller pin for each of the 64 LEDs (which would require 64 pins!), the LEDs are wired into intersecting rows and columns.
* For an 8x8 matrix, you only need 16 pins (8 for rows, 8 for columns).
* By rapidly switching through the rows one-by-one and turning on the specific columns needed for that row, the human eye perceives the whole image as steadily lit due to **persistence of vision**.

### 🔧 Wiring and Code Integration
When integrating this hex array into your Arduino or Raspberry Pi project:
* You typically use a driver chip like the **MAX7219** which handles the fast multiplexing logic for you so your microcontroller doesn't have to work as hard.
* The hexadecimal array generated above corresponds perfectly to the data you send to the MAX7219 chip. 
* For Python (e.g. Raspberry Pi), libraries like `luma.led_matrix` can directly ingest this array format!

---

### 💻 DSA Concepts Used:
* **2D Arrays (Matrices):** The state of the LED grid is stored and managed as a 2D array of boolean values.
* **Bitwise Operations:** The boolean values in each row are converted into a single integer using the bitwise OR (`|`) and bitwise left shift (`<<`) operators. This integer is then formatted as a hexadecimal string. For example, `[True, False, False, True, False, False, False, False]` becomes `10010000` in binary, which is `0x90` in hex.
""")
