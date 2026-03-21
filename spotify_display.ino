#include <Arduino.h>
#include <ArduinoJson.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7735.h>
#include <WiFi.h>
#include <SpotifyEsp32.h>
#include <SPI.h>

// =========================
// Pin configuration
// Update these if needed for your exact C3 Mini wiring.
// =========================
#define TFT_CS    5
#define TFT_DC    2
#define TFT_RST   4
#define TFT_MOSI  6
#define TFT_SCLK  7

#define BTN_PREV  8
#define BTN_PLAY  9
#define BTN_NEXT  10

// =========================
// Credentials
// =========================
const char* SSID = "YOUR_WIFI_SSID";
const char* PASSWORD = "YOUR_WIFI_PASSWORD";
const char* CLIENT_ID = "YOUR_CLIENT_ID";
const char* CLIENT_SECRET = "YOUR_CLIENT_SECRET";

// =========================
// Globals
// =========================
Spotify sp(CLIENT_ID, CLIENT_SECRET);
Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_MOSI, TFT_SCLK, TFT_RST);

String lastArtist = "";
String lastTrack = "";
unsigned long lastPoll = 0;
const unsigned long pollInterval = 2000;

bool lastPrevState = HIGH;
bool lastPlayState = HIGH;
bool lastNextState = HIGH;

void drawCenteredText(const String& text, int y, uint8_t textSize) {
  int16_t x1, y1;
  uint16_t w, h;
  tft.setTextSize(textSize);
  tft.getTextBounds(text.c_str(), 0, y, &x1, &y1, &w, &h);
  int x = (160 - w) / 2;
  if (x < 0) x = 0;
  tft.setCursor(x, y);
  tft.print(text);
}

void drawUI(const String& artist, const String& track, bool isPlaying) {
  tft.fillScreen(ST77XX_BLACK);

  tft.drawRect(4, 4, 152, 120, ST77XX_WHITE);
  tft.setTextColor(ST77XX_WHITE);

  tft.setTextSize(1);
  tft.setCursor(12, 12);
  tft.print("Spotify Display");

  tft.drawLine(10, 24, 150, 24, ST77XX_WHITE);

  tft.setTextColor(ST77XX_GREEN);
  drawCenteredText(track, 40, 2);

  tft.setTextColor(ST77XX_CYAN);
  drawCenteredText(artist, 75, 1);

  tft.setTextColor(isPlaying ? ST77XX_GREEN : ST77XX_RED);
  tft.setCursor(12, 104);
  tft.print(isPlaying ? "Status: Playing" : "Status: Paused");
}

void connectWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(SSID, PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
}

void authenticateSpotify() {
  Serial.println("Starting Spotify authentication...");
  sp.begin();

  while (!sp.is_auth()) {
    sp.handle_client();
    delay(50);
  }

  Serial.println("Spotify authenticated");
}

void handleButtons() {
  bool currentPrev = digitalRead(BTN_PREV);
  bool currentPlay = digitalRead(BTN_PLAY);
  bool currentNext = digitalRead(BTN_NEXT);

  if (lastPrevState == HIGH && currentPrev == LOW) {
    Serial.println("Previous");
    sp.previous();
    delay(250);
  }

  if (lastPlayState == HIGH && currentPlay == LOW) {
    Serial.println("Play / Pause");
    sp.start_resume_playback();
    delay(250);
  }

  if (lastNextState == HIGH && currentNext == LOW) {
    Serial.println("Next");
    sp.skip();
    delay(250);
  }

  lastPrevState = currentPrev;
  lastPlayState = currentPlay;
  lastNextState = currentNext;
}

void setup() {
  Serial.begin(115200);

  pinMode(BTN_PREV, INPUT_PULLUP);
  pinMode(BTN_PLAY, INPUT_PULLUP);
  pinMode(BTN_NEXT, INPUT_PULLUP);

  tft.initR(INITR_BLACKTAB);
  tft.setRotation(1);
  tft.fillScreen(ST77XX_BLACK);
  tft.setTextWrap(false);
  tft.setTextColor(ST77XX_WHITE);
  tft.setCursor(10, 10);
  tft.print("Booting...");

  connectWiFi();
  authenticateSpotify();

  drawUI("Waiting...", "No track", false);
}

void loop() {
  handleButtons();

  if (millis() - lastPoll >= pollInterval) {
    lastPoll = millis();

    String currentArtist = sp.current_artist_names();
    String currentTrack = sp.current_track_name();
    bool playing = sp.is_playing();

    bool validArtist = !currentArtist.isEmpty() && currentArtist != "Something went wrong";
    bool validTrack = !currentTrack.isEmpty() && currentTrack != "Something went wrong" && currentTrack != "null";

    if (validArtist && validTrack) {
      if (currentArtist != lastArtist || currentTrack != lastTrack) {
        lastArtist = currentArtist;
        lastTrack = currentTrack;
        Serial.println("Track updated");
        Serial.println("Artist: " + currentArtist);
        Serial.println("Track: " + currentTrack);
      }
      drawUI(currentArtist, currentTrack, playing);
    } else {
      drawUI("Spotify", "No active track", false);
    }
  }
}
