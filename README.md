# Helmholtz 3D Magnetic Field Probe

A desktop application for real-time acquisition, visualization, and recording of magnetic field measurements from an array of eight 3-axis magnetometers. Designed for Helmholtz coil characterization, magnetic field mapping, and laboratory experiments.

---

## Overview

This application interfaces with an array of **Adafruit MMC5603** magnetometers through an **Adafruit TCA9548A I²C Multiplexer** and an **Adafruit FT232H USB-I²C bridge**.

The software provides:

- Live magnetic field visualization
- Individual sensor selection
- Simultaneous monitoring of all eight sensors
- Continuous data acquisition
- Run history management
- CSV export (planned)
- Hardware abstraction for easy expansion

The project is written entirely in **Python** using **PySide6** and **PyQtGraph**.

---

# Features

## Real-Time Data Acquisition

- Continuous acquisition while running
- One-click Start/Stop interface
- Threaded acquisition keeps the UI responsive
- Configurable sample rate

---

## Live Plotting

View any individual sensor in real time.

Each sensor displays:

- Bx
- By
- Bz

with automatic scaling.

---

## View All Mode

Monitor all eight magnetometers simultaneously.

Each sensor receives its own plot with independent scaling, making it easy to compare field variations across the array.

---

## Multiple Sensor Support

Supports eight independent magnetometers connected through an I²C multiplexer.

Current supported hardware:

- Sensor 0
- Sensor 1
- Sensor 2
- Sensor 3
- Sensor 4
- Sensor 5
- Sensor 6
- Sensor 7

---

## Run Recording

Each acquisition session is recorded independently.

Features include:

- Sample number
- Timestamp
- Bx
- By
- Bz

for every sensor.

Runs remain stored after plotting is cleared.

---

## Continue Previous Run

Optionally continue plotting on the current graph instead of clearing between acquisitions.

Useful for:

- Long experiments
- Coil tuning
- Incremental adjustments

---

# Hardware

Current hardware configuration

```
Computer
      │
USB
      │
Adafruit FT232H
      │
I²C
      │
Adafruit TCA9548A
      │
 ┌────┴────┐
 │         │
MMC5603 ×8 Sensors
```

---

## Components

- Adafruit FT232H USB to I²C Bridge
- Adafruit TCA9548A 8-Channel I²C Multiplexer
- 8 × Adafruit MMC5603 3-Axis Magnetometers

---

# Software Stack

- Python 3.13
- PySide6
- PyQtGraph
- NumPy
- Pandas
- Adafruit Blinka
- Adafruit CircuitPython MMC56X3
- Adafruit CircuitPython TCA9548A
- PyUSB
- libusb-package

---

# Installation

Clone the repository

```bash
git clone https://github.com/TechCoderYorktown/helmholtz-3d-probe.git

cd helmholtz-3d-probe
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Launch the application

```bash
python src/main.py
```

---

# Project Structure

```
helmholtz-3d-probe/

│
├── src/
│
├── gui/
│   ├── main_window.py
│   ├── toolbar.py
│   ├── sensor_panel.py
│   ├── plot_panel.py
│   └── status_panel.py
│
├── hardware/
│   ├── hardware_manager.py
│   ├── acquisition_thread.py
│   └── simulator.py
│
├── models/
│   ├── sensor_reading.py
│   ├── data_recorder.py
│   └── run_history.py
│
├── config.py
│
└── main.py
```

---

# Application Workflow

```
Run Button
      │
      ▼
Connect Hardware
      │
      ▼
Acquisition Thread
      │
      ▼
Read 8 Sensors
      │
      ▼
Store Data
      │
      ▼
Update Plots
      │
      ▼
Display Values
```

---

# Data Format

Each recorded sample contains

| Column | Description |
|---------|-------------|
| Sample | Sample number |
| Time | Seconds since acquisition started |
| B0_X | Sensor 0 X field |
| B0_Y | Sensor 0 Y field |
| B0_Z | Sensor 0 Z field |
| ... | ... |
| B7_X | Sensor 7 X field |
| B7_Y | Sensor 7 Y field |
| B7_Z | Sensor 7 Z field |

---

# Current Capabilities

✅ Real-time acquisition

✅ Live plotting

✅ Individual sensor view

✅ View All dashboard

✅ Threaded acquisition

✅ Independent sensor histories

✅ Multiple run storage

✅ Hardware abstraction layer

---

# Planned Features

- CSV export
- Adjustable sampling rate
- Maximum acquisition time
- Pause/Resume
- Plot zoom synchronization
- Statistics panel
- Calibration tools
- Field magnitude heatmap
- 3D magnetic field visualization
- Automatic sensor detection
- Binary data recording
- Session loading
- Session saving

---

# Intended Applications

- Helmholtz coil characterization
- Magnetic field mapping
- Sensor calibration
- Laboratory research
- Educational demonstrations
- Spin Polarized Fusion (SPF) instrumentation
- Electromagnet characterization

---

# Development

This application follows a modular architecture.

Hardware communication, plotting, data recording, and GUI components are separated into independent modules, allowing new sensors or acquisition hardware to be integrated with minimal changes.

---

# License

This project is licensed under the MIT License.

---

# Author

Developed for research involving multi-sensor magnetic field measurements and Helmholtz coil characterization.
