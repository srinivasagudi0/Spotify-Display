# 🎵 Spotify Display (ESP32 + TFT)

A compact hardware project that displays your currently playing Spotify track in real time using an ESP32 and a TFT screen.

---

## 🚀 Features

- 🎵 Displays current song name and artist  
- 📡 Connects to Spotify via WiFi + API  
- 🖥 Runs on a 1.8" TFT display (ST7735)  
- 🎛 Includes 3-button control system:
  - Play / Pause  
  - Next Track  
  - Previous Track  
- ⚡ Lightweight and efficient using ESP32 C3 Mini  

---

## 🧠 What’s Original About This Project

- Designed a custom enclosure for ESP32 + TFT instead of using a pre-made case  
- Implemented a custom 3-button layout for media control  
- Built a custom UI on the TFT screen for clean display of track and artist  
- Integrated Spotify API directly with embedded hardware  
- Optimized for a compact ESP32 C3 Mini setup  
- Designed to be modular and upgradeable (album art, LEDs, battery support)  

---

## 📚 Reference Guide

This project was inspired by the following tutorial:  
👉 https://<PUT-YOUR-TUTORIAL-LINK-HERE>

---

## 🔧 What I Changed From the Tutorial

- Simplified the hardware setup to focus on core functionality  
- Modified the code structure for better readability and modularity  
- Adjusted the enclosure design to be more compact  
- Customized the screen layout for better readability  
- Built a working prototype first, then improved incrementally  

---

## 🧰 Hardware Components

- 1x ESP32 Board (LOLIN C3 Mini)  
- 1x 1.8" TFT Display (ST7735 / ILI9341)  
- 3x Tactile Switches (or keyboard switches)  
- 4x M3 Heatset Inserts  
- Jumper wires or soldering iron  

---

## 🔌 Wiring Overview

| Component | ESP32 Pin |
|----------|----------|
| TFT CS   | (set in code) |
| TFT DC   | (set in code) |
| TFT RST  | (set in code) |
| TFT MOSI | (set in code) |
| TFT SCLK | (set in code) |
| Buttons  | GPIO pins (pull-up configuration) |

⚠️ Exact pins may vary depending on your ESP32 board  

---

## 🖥️ Software Setup

### 1. Install Arduino IDE  
https://www.arduino.cc/en/software  

### 2. Install ESP32 Board  

Go to Preferences → Additional Board URLs and add:  
https://dl.espressif.com/dl/package_esp32_index.json  

### 3. Install Libraries  

- Adafruit GFX  
- Adafruit ST7735  
- SpotifyEsp32  

---

## 🔑 Spotify API Setup

1. Go to https://developer.spotify.com/dashboard  
2. Create a new app  
3. Copy:
   - Client ID  
   - Client Secret  

4. Add them in your code:

```cpp
const char* CLIENT_ID = "YOUR_CLIENT_ID";
const char* CLIENT_SECRET = "YOUR_CLIENT_SECRET";
```

## ▶️ How It Works

Spotify API → ESP32 → TFT Display

- ESP32 connects to WiFi  
- Authenticates with Spotify  
- Fetches current track info  
- Displays it on the screen  
- Buttons control playback  

---

## 🧪 Demo

*(Add your photo or video here)*

---

## 🛠 Future Improvements

- 🖼 Display album art  
- 🔋 Add battery + charging module  
- 🎨 Improve UI with fonts and layout  
- 🔊 Add volume control (rotary encoder)  
- 💡 Add LED indicators or animations  

---

## 📂 Project Structure
Spotify-Display/
│
├── spotify_display.ino
├── README.md
├── cad/
├── images/
└── docs/


---

## ⚠️ Notes

- Ensure correct pin mapping for your board  
- Spotify API has rate limits → use delays  
- Some features require active Spotify playback  

---

## 🏁 Conclusion

This project demonstrates how embedded systems can integrate with modern APIs like Spotify to create a real-time interactive device.
