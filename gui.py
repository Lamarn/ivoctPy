import sys
import matplotlib.pyplot as plt
import show_ascan

from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, \
    QStatusBar, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # First figure
        self.figure1 = plt.figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.toolbar1 = NavigationToolbar(self.canvas1, self)
        self.figure_element1 = QVBoxLayout()
        self.figure_element1.addWidget(self.canvas1)
        self.figure_element1.addWidget(self.toolbar1)
        # Second figure
        self.figure2 = plt.figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.toolbar2 = NavigationToolbar(self.canvas2, self)
        self.figure_element2 = QVBoxLayout()
        self.figure_element2.addWidget(self.canvas2)
        self.figure_element2.addWidget(self.toolbar2)
        # Third figure
        self.figure3 = plt.figure()
        self.canvas3 = FigureCanvas(self.figure3)
        self.toolbar3 = NavigationToolbar(self.canvas3, self)
        self.figure_element3 = QVBoxLayout()
        self.figure_element3.addWidget(self.canvas3)
        self.figure_element3.addWidget(self.toolbar3)
        # Fourth figure
        self.figure4 = plt.figure()
        self.canvas4 = FigureCanvas(self.figure4)
        self.toolbar4 = NavigationToolbar(self.canvas4, self)
        self.figure_element4 = QVBoxLayout()
        self.figure_element4.addWidget(self.canvas4)
        self.figure_element4.addWidget(self.toolbar4)
        # Fifth figure
        self.figure5 = plt.figure()
        self.canvas5 = FigureCanvas(self.figure4)
        self.toolbar5 = NavigationToolbar(self.canvas5, self)
        self.figure_element5 = QVBoxLayout()
        self.figure_element5.addWidget(self.canvas5)
        self.figure_element5.addWidget(self.toolbar5)
        # Sixth figure
        self.figure6 = plt.figure()
        self.canvas6 = FigureCanvas(self.figure6)
        self.toolbar6 = NavigationToolbar(self.canvas6, self)
        self.figure_element6 = QVBoxLayout()
        self.figure_element6.addWidget(self.canvas6)
        self.figure_element6.addWidget(self.toolbar6)

        # Buttons
        self.button_load_raw = QPushButton("Load raw data")
        self.button_load_raw.clicked.connect(self.load_raw)
        self.button_process_raw = QPushButton("Process raw data")
        self.button_process_raw.clicked.connect(self.process_raw)
        self.button_load_ascans = QPushButton("Load ascans")
        self.button_load_ascans.clicked.connect(self.load_ascans)
        self.button_process_ascans = QPushButton("Process ascans")
        self.button_process_ascans.clicked.connect(self.process_ascans)

        # Layouts
        self.layout_buttons1 = QHBoxLayout()
        self.layout_buttons1.addWidget(self.button_load_raw)
        self.layout_buttons1.addWidget(self.button_process_raw)

        self.layout_buttons2 = QHBoxLayout()
        self.layout_buttons2.addWidget(self.button_load_ascans)
        self.layout_buttons2.addWidget(self.button_process_ascans)

        self.layout_tab_raw = QVBoxLayout()
        self.layout_tab_ascan = QVBoxLayout()

        self.layout_raw_first_row = QHBoxLayout()
        self.layout_raw_first_row.addLayout(self.figure_element1)
        self.layout_raw_first_row.addLayout(self.figure_element2)

        self.layout_raw_second_row = QHBoxLayout()
        self.layout_raw_second_row.addLayout(self.figure_element3)
        self.layout_raw_second_row.addLayout(self.figure_element4)

        self.layout_ascan_first_row = QHBoxLayout()
        self.layout_ascan_first_row.addLayout(self.figure_element5)
        self.layout_ascan_first_row.addLayout(self.figure_element6)



        self.layout_tab_raw.addLayout(self.layout_buttons1)
        self.layout_tab_raw.addLayout(self.layout_raw_first_row)
        self.layout_tab_raw.addLayout(self.layout_raw_second_row)

        self.layout_tab_ascan.addLayout(self.layout_buttons2)
        self.layout_tab_ascan.addLayout(self.layout_ascan_first_row)

        # Tab Widget
        self.tab_widget = QTabWidget()
        self.tab_raw_data = QWidget()
        self.tab_ascans = QWidget()

        self.tab_raw_data.setLayout(self.layout_tab_raw)
        self.tab_ascans.setLayout(self.layout_tab_ascan)

        self.tab_widget.addTab(self.tab_raw_data, "Raw data from OCT system")
        self.tab_widget.addTab(self.tab_ascans, "Preprocessed image from IVOCT")

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)

        self.setLayout(layout)

    def load_raw(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open binary file', '', "Binary (*.bin)")

        # show_ascan.main()
        # self.figure1.clear()
        # ax = self.figure.add_subplot(111)
        # ax.plot(data, '*-')
        # self.canvas1.draw()

    def process_raw(self):
        pass

    def load_ascans(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open b-scan file', '', "B Scans (*.bin)")

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
