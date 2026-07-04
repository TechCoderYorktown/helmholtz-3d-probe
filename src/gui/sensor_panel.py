from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QRadioButton,
    QButtonGroup,
)


class SensorPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Sensors")
        layout.addWidget(title)

        self.button_group = QButtonGroup(self)

        self.buttons = []

        # ----- All Sensors -----
        all_button = QRadioButton("View All")
        all_button.setChecked(True)

        self.button_group.addButton(all_button)

        self.buttons.append(all_button)

        layout.addWidget(all_button)

        # ----- Individual Sensors -----
        for i in range(8):

            button = QRadioButton(f"Sensor {i}")

            self.button_group.addButton(button)

            self.buttons.append(button)

            layout.addWidget(button)

        layout.addStretch()

        self.setLayout(layout)

    def selected_sensor(self):
        """
        Returns:
            -1  -> All Sensors selected
             0  -> Sensor 0
             1  -> Sensor 1
             ...
             7  -> Sensor 7
        """

        for index, button in enumerate(self.buttons):

            if button.isChecked():

                return index - 1

        return -1