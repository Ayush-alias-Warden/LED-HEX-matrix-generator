# Interactive LED Matrix Hex Generator 💡

A web-based interactive tool built with **Streamlit** that allows you to easily draw shapes on an LED matrix grid (8x8 or 16x16) and automatically generate the corresponding Hexadecimal arrays in real-time. 

Say goodbye to manually mapping binary 1s and 0s on graphing paper!

## 🚀 Features
* **Two Matrix Sizes**: Supports standard 8x8 matrices and larger 16x16 matrices.
* **Multi-Language Output**: Generate the arrays as `C/C++` code (perfect for Arduino / ESP32) or `Python` lists (great for Raspberry Pi).
* **Interactive Canvas**: Click to toggle individual LEDs on and off.
* **State Controls**: Features a built-in Undo button to easily revert mistakes, and a Clear/Delete button to wipe the board.
* **Shape Presets**: Start your drawing with a baseline template like a Box, Cross, or Smiley Face.
* **Dark Mode**: Comes pre-configured with a sleek dark theme and green active states.

## 💻 Data Structures & Algorithms Used
Behind the scenes, this tool heavily relies on foundational programming concepts:
* **2D Arrays (Matrices)**: The grid's state is strictly maintained in memory as a 2D boolean array representing the physical rows and columns of LEDs.
* **Bitwise Operations**: To generate the hex codes efficiently, the app takes the boolean states of a row (e.g. `[True, False, False, True...]`) and converts them into an integer using bitwise `OR` (`|`) and bitwise left-shifts (`<<`). This integer is then converted to its hexadecimal representation (e.g., `0x90`).

## 🛠️ How to run locally
If you want to run this application on your own machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
   cd YOUR-REPO-NAME
   ```

2. **Install the dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   python -m streamlit run led_matrix.py
   ```
4. The application will open in your default browser at `http://localhost:8501`.

## ⚙️ Hardware Integration
The output from this app is designed to be fed directly into LED matrix driver chips, such as the popular **MAX7219**. 
By pasting the generated hex array into your microcontroller code, you can easily control multiplexed LED displays without calculating the binary offsets by hand.
