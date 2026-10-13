APP_NAME = "Helmholtz Coil Mapper"

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

NUM_SENSORS = 8

MAX_PLOT_POINTS = 500

# The notebook's geometry correction for the mounted probes. Channels not
# listed here use the sensor's native axes.
SENSOR_AXIS_CONFIGS = {
    0: lambda raw_x, raw_y, raw_z: (raw_z, -raw_y, raw_x),
    1: lambda raw_x, raw_y, raw_z: (-raw_z, -raw_y, -raw_x),
}

I2C_MULTIPLEXER_ADDRESS = 0x70
SENSOR_ADDRESS = 0x30