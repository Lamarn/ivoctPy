import sys
from scan import Scan
from raw_data import RawData
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, \
    QFileDialog, QStatusBar, QLabel, QPlainTextEdit, QLayout, QFrame
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class Window(QDialog):
    "https://stackoverflow.com/questions/12459811/how-to-embed-matplotib-in-pyqt-for-dummies"

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.raw_data = None
        self.scan = None

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
        self.canvas5 = FigureCanvas(self.figure5)
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

        # Text Edit's
        self.diameter_min = QLabel("Diameter (min): ")
        self.diameter_max = QLabel("Diameter (max): ")
        self.diameter_average = QLabel("Diameter (average): ")

        self.diameter_min_text = QPlainTextEdit("...")
        self.diameter_min_text.setMaximumHeight(30)
        self.diameter_max_text = QPlainTextEdit("...")
        self.diameter_max_text.setMaximumHeight(30)
        self.diameter_average_text = QPlainTextEdit("...")
        self.diameter_average_text.setMaximumHeight(30)

        self.layout_diameter = QHBoxLayout()
        self.layout_diameter.addWidget(self.diameter_min)
        self.layout_diameter.addWidget(self.diameter_min_text)
        self.layout_diameter.addWidget(self.diameter_max)
        self.layout_diameter.addWidget(self.diameter_max_text)
        self.layout_diameter.addWidget(self.diameter_average)
        self.layout_diameter.addWidget(self.diameter_average_text)

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
        self.layout_raw_first_row.addWidget(self.VLine())
        self.layout_raw_first_row.addLayout(self.figure_element2)

        self.layout_raw_second_row = QHBoxLayout()
        self.layout_raw_second_row.addLayout(self.figure_element3)
        self.layout_raw_second_row.addWidget(self.VLine())
        self.layout_raw_second_row.addLayout(self.figure_element4)

        self.layout_ascan_first_row = QHBoxLayout()
        self.layout_ascan_first_row.addLayout(self.figure_element5)
        self.layout_ascan_first_row.addWidget(self.VLine())
        self.layout_ascan_first_row.addLayout(self.figure_element6)

        self.layout_tab_raw.addLayout(self.layout_buttons1)
        self.layout_tab_raw.addWidget(self.HLine())
        self.layout_tab_raw.addLayout(self.layout_raw_first_row)
        self.layout_tab_raw.addWidget(self.HLine())
        self.layout_tab_raw.addLayout(self.layout_raw_second_row)

        self.layout_tab_ascan.addLayout(self.layout_buttons2)
        self.layout_tab_ascan.addWidget(self.HLine())
        self.layout_tab_ascan.addLayout(self.layout_ascan_first_row)
        self.layout_tab_ascan.addWidget(self.HLine())
        self.layout_tab_ascan.addLayout(self.layout_diameter)

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
        self.status_bar = QStatusBar()
        self.status_bar_text = QLabel("Starting succesfully finished")
        self.status_bar.addWidget(self.status_bar_text)
        layout.addWidget(self.status_bar)
        self.setLayout(layout)

    def HLine(self):
        toto = QFrame()
        toto.setFrameShape(QFrame.HLine)
        toto.setFrameShadow(QFrame.Sunken)
        return toto

    def VLine(self):
        toto = QFrame()
        toto.setFrameShape(QFrame.VLine)
        toto.setFrameShadow(QFrame.Sunken)
        return toto

    def load_raw(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open binary file', '', "Binary (*.bin)")
        if path != "":
            self.raw_data = None

            self.status_bar_text.setText("Loading raw data")
            # Loading raw data
            self.raw_data = RawData(10000)
            self.raw_data.load_raw_data(path)
            # 5 raw ascans
            self.figure1.clear()
            ax = self.figure1.add_subplot(111)
            ax.plot(self.raw_data.cut_spectra[:, 120:125])
            self.canvas1.draw()
            # 5000 raw ascans
            self.figure3.clear()
            ax = self.figure3.add_subplot(111)
            ax.imshow(self.raw_data.cut_spectra)
            self.canvas3.draw()
            self.status_bar_text.setText("Finished loading raw data")
        else:
            self.status_bar_text.setText("Path was empty!")

    def process_raw(self):
        if self.raw_data is not None:
            self.status_bar_text.setText("Processing raw data")
            self.raw_data.process_raw_data()
            # 5 processed ascans
            self.figure2.clear()
            ax = self.figure2.add_subplot(111)
            ax.plot(self.raw_data.cut_spectra[:, 120:125])
            self.canvas2.draw()
            # processed image
            self.figure4.clear()
            ax = self.figure4.add_subplot(111)
            ax.imshow(self.raw_data.cut_spectra)
            self.canvas4.draw()
            self.status_bar_text.setText("Finished processing raw data")

    def load_ascans(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open b-scan file', '', "B Scans (*.bin)")
        if path != "":
            self.status_bar_text.setText("Loading processed data")
            # Loading Scan
            self.scan = Scan(10000)
            self.scan.load_data(path)
            self.scan.preprocess_matrix()
            # 5000 processed ascans
            self.figure5.clear()
            ax = self.figure5.add_subplot(111)
            ax.imshow(self.scan.cut_matrix)
            self.canvas5.draw()

            self.status_bar_text.setText("Finished loading processed data")
        else:
            self.status_bar_text.setText("Path was empty!")

    def process_ascans(self):
        if self.scan is not None:
            self.status_bar_text.setText("Processing polar view")
            self.scan.find_peaks()
            self.scan.create_polar_views()
            # polar_view = self.scan.interpolation_polar_view(self.scan.polar_views[2], 3)
            # Show polar view
            self.figure5.clear()
            ax = self.figure5.add_subplot(111)
            ax.imshow(self.scan.polar_views[2])
            self.canvas5.draw()

            self.status_bar_text.setText("Finished processing polar view")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.showMaximized()
    main.setWindowTitle("Intravascular Optical Coherence Tomograph - Viewer")
    main.show()

    sys.exit(app.exec_())
