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

## 🔧 What I Changed From the Tutorial

- Simplified the hardware setup to focus on core functionality first
- Modified the code structure to keep WiFi, Spotify, and display logic easy to understand
- Adjusted the enclosure direction toward a compact desk-friendly format
- Customized the screen output for a cleaner UI
- Built the software as a working prototype first and left room for future upgrades

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
| TFT CS   | 5 |
| TFT DC   | 2 |
| TFT RST  | 4 |
| TFT MOSI | 6 |
| TFT SCLK | 7 |
| BTN_PREV | 8 |
| BTN_PLAY | 9 |
| BTN_NEXT | 10 |

> Adjust the pins above if your exact C3 Mini wiring is different.

---

## 🖥️ Software Setup

### 1. Install Arduino IDE

Download Arduino IDE from the official website.

### 2. Install ESP32 Board Support

Go to **Preferences → Additional Board URLs** and add:

```text
https://dl.espressif.com/dl/package_esp32_index.json
```

### 3. Install Libraries

Install these libraries:

- Adafruit GFX
- Adafruit ST7735
- SpotifyEsp32
- ArduinoJson

---

## 🔑 Spotify API Setup

1. Go to the Spotify Developer Dashboard
2. Create a new app
3. Copy your:
   - Client ID
   - Client Secret
4. Add them in the code

```cpp
const char* CLIENT_ID = "YOUR_CLIENT_ID";
const char* CLIENT_SECRET = "YOUR_CLIENT_SECRET";
```

---

## ▶️ How It Works

Spotify API → ESP32 → TFT Display

- ESP32 connects to WiFi
- Authenticates with Spotify
- Fetches current track info
- Displays it on the screen
- Buttons control playback

---

## 🧪 Demo

Add your project photo or video here.

---

## 🛠 Future Improvements

- 🖼 Display album art
- 🔋 Add battery + charging module
- 🎨 Improve UI with better fonts and layout
- 🔊 Add volume control with a rotary encoder
- 💡 Add LED indicators or animations

---

## 📂 Project Structure

```text
Spotify-Display/
├── spotify_display.ino
├── README.md
├── cad/
│   └── README.md
├── images/
│   └── README.md
└── docs/
    └── wiring.md
```

---

## ⚠️ Notes

- Ensure correct pin mapping for your board
- Spotify API has rate limits, so use delays responsibly
- Some features require active Spotify playback on your Spotify account

---

## 🏁 Conclusion

This project demonstrates how embedded systems can integrate with modern APIs like Spotify to create a real-time interactive device.

---

## 👤 Author

Srinivasa Gudi  
GitHub: https://github.com/srinivasagudi0
