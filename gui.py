from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
from chaotic_maps import TinkerbellMap, Simulator, CliffordAttractor
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Draw Chaotic Map")

        #self.graphWidget = pg.PlotWidget()
        #self.setCentralWidget(self.graphWidget)

        self.title = self.create_title()
        self.dropdown_list_box = self.create_dropdown_list_box_maps()
        self.plot_widget = self.create_graph_space()
        self.set_layout([self.title, self.dropdown_list_box, self.plot_widget])

    def set_layout(self, widgets):
        layout = QtWidgets.QVBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def create_text_boxes(self):
        pass
    def create_dropdown_list_box_maps(self):
        widget = QtWidgets.QComboBox()
        widget.addItems(['TinkerBell Map', 'Ikeda Map', 'Clifford Attractor'])

        # There is an alternate signal to send the text.
        widget.currentIndexChanged.connect(self.get_map_selection)
        return widget

    def get_map_selection(self, i):
        # Manual test code: will be rewritten
        if i == 0:
            tinkerbel = TinkerbellMap(0.9, -0.6013, 2, 0.5)
            sim = Simulator(tinkerbel, 50000)
            xs, ys = sim.simulate()
            self.plot_widget.clear()
            self.plot_widget.plot(xs, ys, pen=None, symbol='o', symbolSize=1)
        elif i == 1:
            # Handle Ikeda Map selection here
            pass
        elif i == 2:
            sim = Simulator(CliffordAttractor(), 50000)
            xs, ys = sim.simulate()
            self.plot_widget.clear()
            self.plot_widget.plot(xs, ys, pen=None, symbol='o', symbolSize=1)

    def create_title(self):
        widget = QtWidgets.QLabel('Draw Chaotic Map')
        font = widget.font()
        font.setPointSize(30)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        return widget
    
    def create_graph_space(self):
        plot_widget = pg.PlotWidget()
        plot_widget.setBackground('w')
        return plot_widget


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()