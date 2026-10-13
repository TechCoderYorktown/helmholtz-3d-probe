# Helmholtz Coil Mapper

Real-time desktop application for reading up to eight MMC5603 magnetometers
through an Adafruit FT232H and PCA9548A I2C multiplexer.

## Hardware

- FT232H USB-to-I2C adapter
- PCA9548A multiplexer at `0x70`
- MMC5603 magnetometers at `0x30`
- Magnetometers connected to multiplexer channels `0` through `7`

The application scans every multiplexer channel at startup and only enables
channels where an MMC5603 is detected. The axis corrections from
`helmhotlz_coil (3).ipynb` are applied to channels 0 and 1; other channels
use their native axes.

## Run from source

Create a Python 3.12+ environment and install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run with the connected hardware:

```powershell
python src\main.py
```

Run without hardware to verify the live graph interface:

```powershell
python src\main.py --simulate
```

The simulator produces live data for all eight channels. Use **View All** or
an individual sensor in the left panel, and use **Save CSV** to export the
current run.

## Build the Windows executable

Install PyInstaller in the same environment and build with the checked-in
specification:

```powershell
python -m pip install pyinstaller
python -m PyInstaller HelmholtzCoilMapper.spec --clean
```

The executable is written to `dist\HelmholtzCoilMapper.exe`. The hardware
version is the default; `--simulate` can also be passed when launching the
executable.

On Windows, the FT232H may require a WinUSB/libusb driver selected with
[Zadig](https://zadig.akeo.ie).
