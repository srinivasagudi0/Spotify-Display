# Wiring Guide

## TFT Display to ESP32 C3 Mini

| TFT Pin | ESP32 Pin |
|---|---|
| VCC | 3V3 |
| GND | GND |
| CS | GPIO 5 |
| DC | GPIO 2 |
| RST | GPIO 4 |
| SDA / MOSI | GPIO 6 |
| SCL / SCLK | GPIO 7 |
| LED / BL | 3V3 |

## Buttons

Each button should connect one side to the GPIO pin and the other side to GND.
The sketch uses `INPUT_PULLUP`, so no external pull-up resistor is required.

| Button | ESP32 Pin |
|---|---|
| Previous | GPIO 8 |
| Play / Pause | GPIO 9 |
| Next | GPIO 10 |
