import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QLabel,
)


class InputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_input_labels(self, labels):
        self.input_labels = [
            {"label": QLabel(label), "edit": QLineEdit()} for label in labels
        ]

    def init_buttons(self, button_labels):
        self.buttons = [QPushButton(button_label) for button_label in button_labels]

    def get_labels(self):
        return [input_label["label"] for input_label in self.input_labels]

    def get_edits(self):
        return [input_label["edit"] for input_label in self.input_labels]

    def init_layout(self):
        layout = QVBoxLayout()

        for input_label in self.input_labels:
            layout.addWidget(input_label["label"])
            layout.addWidget(input_label["edit"])

        for button in self.buttons:
            layout.addWidget(button)

        self.setLayout(layout)
        self.setWindowTitle("NDS Report Generator")
        self.setGeometry(0, 0, 960, 540)

    def init_ui(self):
        labels = ["Input 1:", "Input 2:", "Input 3:", "Result:"]
        button_labels = ["Print Inputs", "Clear Inputs"]

        self.init_input_labels(labels)
        self.init_buttons(button_labels)
        self.init_layout()
        self.show()

        # connect the button to the print_inputs method
        # filter a button to only get the print button
        filter_buttons = list(
            filter(lambda button: button.text() == "Print Inputs", self.buttons)
        )

        for button in filter_buttons:
            button.clicked.connect(self.display_inputs)

    def display_inputs(self):
        # filter a button to only get the result label
        filter_labels = list(
            filter(lambda label: label.text() == "Result:", self.get_labels())
        )
        for label in filter_labels:
            label.setText(
                "\n".join(
                    [
                        input_edit.text()
                        for input_edit in [
                            input_label["edit"] for input_label in self.input_labels
                        ]
                    ]
                )
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InputWindow()
    sys.exit(app.exec_())
