from PySide6.QtWidgets import QApplication, QMainWindow, QListWidget, QLabel, QVBoxLayout, QWidget, QStackedLayout
from PySide6.QtCore import Qt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.listWidget = QListWidget(self)
        self.empty_label = QLabel("The list is currently empty", self)
        self.empty_label.setAlignment(Qt.AlignCenter)
        #self.empty_label.setStyleSheet("QLabel { background-color : rgba(255, 255, 255, 150); color : black; }")

        layout = QStackedLayout()
        layout.addWidget(self.listWidget)
        layout.addWidget(self.empty_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('QListWidget Example')

        self.update_empty_label()

    def update_empty_label(self):
        if self.listWidget.count() == 0:
            self.empty_label.show()
        else:
            self.empty_label.hide()

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
