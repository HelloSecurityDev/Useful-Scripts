# This is a script to add a "sparkles and glitter" effect to your apps, creations, and GUIs.
# By Adam Rivers of Hello Security LLC 2024.
# Inspired By Lauren Carlson's love for all things glittery and an insistance that my inventions must sparkle.

import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor

class SparklingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.sparkles = []

        # Start timer to add sparkles periodically
        self.sparkle_timer = QTimer(self)
        self.sparkle_timer.timeout.connect(self.add_sparkle)
        self.sparkle_timer.start(200)  # Add sparkle every 200 milliseconds

    def add_sparkle(self):
        # Generate random sparkle coordinates
        x = random.randint(0, self.width())
        y = random.randint(0, self.height())
        self.sparkles.append((x, y))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        for sparkle in self.sparkles:
            color = QColor(random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
            painter.setBrush(color)
            painter.drawEllipse(sparkle[0], sparkle[1], 10, 10)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SparklingWidget()
    window.setGeometry(100, 100, 800, 600)
    window.setWindowTitle("Sparkling Effect")
    window.show()
    sys.exit(app.exec_())
