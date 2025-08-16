# air-ink
# ✋ A Hand Gesture Drawing & Math Solver

This project is an **interactive OpenCV app** that uses **hand tracking with a webcam** to let you:
- 🎨 Draw on a virtual canvas with finger gestures  
- 🖱️ Select tools and colors by tapping on a **header menu** at the top of the screen  
- ✍️ Write simple math expressions and equations by hand and convert them into **LaTeX**  
- 🧮 Automatically **solve the expressions**  

---

## 🚀 Features
- **Gesture-based controls**
  - 1 finger → Draw  
  - 2 fingers → Select mode (menu interaction)  
- **Header menu for tools & colors**
  - Switch colors (coming soon)
  - Clear canvas  
  - Save drawing  
- **Handwritten math OCR**
  - Captures handwritten expressions (e.g. `(4 + 4)/2`)  
  - Converts them into **LaTeX** (currently via **Mathpix API**)  
  - Evaluates using **Sympy**  
- **Work in progress:** Training a **CNN-based OCR model** to replace Mathpix for a fully open-source solution  
- **No mouse or keyboard required!**

---

## 🛠️ Tech Stack
- **Python 3.10.11**
- [OpenCV](https://opencv.org/) – webcam input, drawing, preprocessing  
- [Mediapipe](https://developers.google.com/mediapipe) – hand tracking  
- [pix2tex](https://github.com/lukas-blecher/LaTeX-OCR) – LaTeX OCR (alternative experiments)  
- [Mathpix API](https://mathpix.com/) – image-to-LaTeX conversion (current implementation)  
- [Sympy](https://www.sympy.org/) – solving math expressions  
- [NumPy](https://numpy.org/) & [Pillow](https://pillow.readthedocs.io/) – image processing  
- [python-dotenv](https://github.com/theskumar/python-dotenv) – environment variable management  

---

## 📝 Environment Notes
- Developer on Windows 11
- Python version: 3.10.11

---

## 📦 Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/air-ink
   cd air-ink
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/MaC
   venv\Scripts\activate      # Windows
3. Install Dependencies
   ```bash
   pip install -r requirements.txt
4. Set up environment variables for Mathpix (create a .env file):
   ```bash
   ID=your_app_id
   KEY=your_app_key
