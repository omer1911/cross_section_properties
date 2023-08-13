
#edited by Omer Can Demir From Istanbul 14.08.2023 


import sys
import matplotlib.pyplot as plt
from math import atan2, sin, cos, sqrt, pi, degrees
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from inertia import *


class CrossSectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cross-Section Properties")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.label = QLabel("Enter cross-section coordinates as (x, y) pairs:")
        self.coord_input = QTextEdit(self)
        self.coord_input.setPlaceholderText("Example: (45, 0), (55, 0), ... Please Enter counter clockwise")

        self.calculate_button = QPushButton("Calculate Properties")
        self.calculate_button.clicked.connect(self.calculateProperties)

        self.result_textedit = QTextEdit(self)
        self.result_textedit.setReadOnly(True)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.updateGeometry()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.coord_input)
        self.layout.addWidget(self.calculate_button)
        self.layout.addWidget(self.result_textedit)
        self.layout.addWidget(self.canvas)

        central_widget = QWidget(self)
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def calculateProperties(self):
        input_text = self.coord_input.toPlainText()
        coords = []
        try:
            coords = eval("[" + input_text + "]")
            if not all(isinstance(coord, tuple) and len(coord) == 2 for coord in coords):
                raise ValueError
        except (SyntaxError, ValueError):
            self.result_textedit.setPlainText("Invalid input. Please enter valid (x, y) pairs.")
            return
        shape = [(float(x), float(y)) for x, y in coords]
        summary_text = summary(shape)
        self.result_textedit.setPlainText(summary_text)
        self.ax.clear()
        x = [c[0] for c in shape]
        y = [c[1] for c in shape]
        cx, cy = centroid(shape)
        minx = min(x)
        maxx = max(x)
        miny = min(y)
        maxy = max(y)
        b = 0.05 * max(maxx - minx, maxy - miny)
        i = inertia(shape)
        p = principal(*i)
        length = min(maxx-minx, maxy-miny)/10
        a1x = [cx - length*cos(p[2]), cx + length*cos(p[2])]
        a1y = [cy - length*sin(p[2]), cy + length*sin(p[2])]
        a2x = [cx - length*cos(p[2] + pi/2), cx + length*cos(p[2] + pi/2)]
        a2y = [cy - length*sin(p[2] + pi/2), cy + length*sin(p[2] + pi/2)]
        x.append(x[0])  # added the end of the cross curve
        y.append(y[0])

        self.ax.plot(x, y, 'k*-', lw=2)
        self.ax.plot(a1x, a1y, '-', color='#0073B2', lw=2)  # blue
        self.ax.plot(a2x, a2y, '-', color='#D55E00')  # vermillion
        self.ax.plot(cx, cy, 'ko', mec='k')
        self.ax.set_aspect('equal')
        self.ax.set_xlim(xmin=minx - b, xmax=maxx + b)
        self.ax.set_ylim(ymin=miny - b, ymax=maxy + b)
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = CrossSectionApp()
    mainWindow.show()
    sys.exit(app.exec_())
