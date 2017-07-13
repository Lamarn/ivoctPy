import sys
import matplotlib.pyplot as plt
import show_ascan

from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, \
    QStatusBar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import random


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # First figure
        self.figure1 = plt.figure()
        self.canvas1 = FigureCanvas(self.figure1)
        # Second figure
        self.figure2 = plt.figure()
        self.canvas2 = FigureCanvas(self.figure2)
        # Third figure
        self.figure3 = plt.figure()
        self.canvas3 = FigureCanvas(self.figure3)
        # Fourth figure
        self.figure4 = plt.figure()
        self.canvas4 = FigureCanvas(self.figure4)

        # Buttons
        self.button_load_raw = QPushButton("Load raw data")
        self.button_load_raw.clicked.connect(self.load_raw)
        self.button_process_raw = QPushButton("Process raw data")
        self.button_load_raw.clicked.connect(self.process_raw)
        self.button_load_ascans = QPushButton("Load ascans")
        self.button_load_raw.clicked.connect(self.load_ascans)
        self.button_process_ascans = QPushButton("Process ascans")
        self.button_load_raw.clicked.connect(self.process_ascans)

        # Layouts
        self.layout_buttons1 = QHBoxLayout()
        self.layout_buttons1.addWidget(self.button_load_raw)
        self.layout_buttons1.addWidget(self.button_process_raw)

        self.layout_buttons2 = QHBoxLayout()
        self.layout_buttons2.addWidget(self.button_load_ascans)
        self.layout_buttons2.addWidget(self.button_process_ascans)

        self.layout_tab_raw = QHBoxLayout()
        self.layout_tab_ascan = QHBoxLayout()

        # Tab Widget
        self.tab_widget = QTabWidget()
        self.tab_raw_data = QWidget()
        self.tab_ascans = QWidget()

        self.tab_widget.addTab(self.tab_raw_data, "raw data")
        self.tab_widget.addTab(self.tab_ascans, "a-scans")

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)

        self.setLayout(layout)

    def load_raw(self):
        show_ascan.main()
        self.figure1.clear()
        ax = self.figure.add_subplot(111)
        # ax.plot(data, '*-')
        self.canvas1.draw()

    def process_raw(self):
        pass

    def load_ascans(self):
        pass

    def process_ascans(self):
        pass

        #
        # def plot(self):
        #     ''' plot some random stuff '''
        #     # random data
        #     data = [random.random() for i in range(10)]
        #
        #     # instead of ax.hold(False)
        #     self.figure.clear()
        #
        #     # create an axis
        #     ax = self.figure.add_subplot(111)
        #
        #     # discards the old graph
        #     # ax.hold(False) # deprecated, see above
        #
        #     # plot data
        #     ax.plot(data, '*-')
        #
        #     # refresh canvas
        #     self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.showMaximized()
    main.setWindowTitle("Intravascular Optical Coherence Tomograph - Viewer")
    main.show()

    sys.exit(app.exec_())
