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
        self.default_maps = {
            'TinkerBell Map': TinkerbellMap,
            'Ikeda Map': None,
            'Clifford Attractor': CliffordAttractor
        }
        self.selected_map = TinkerbellMap()
        self.setWindowTitle("Draw Chaotic Map")
        self.title = self.create_title()
        self.dropdown_list_box = self.create_dropdown_list_box_maps()
        self.text_boxes = self.create_text_boxes()
        self.plot_widget = self.create_graph_space()
        self.set_layout([self.title, self.dropdown_list_box, *self.text_boxes.values(), self.plot_widget])

    def set_layout(self, widgets):
        layout = QtWidgets.QVBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def create_text_boxes(self):
        widgets = {}
        for label_text in ['a', 'b', 'c', 'd', 'x0', 'y0']:
            label = QtWidgets.QLabel(label_text)
            widget = QtWidgets.QLineEdit()
            widget.setMaxLength(10)
            widget.setPlaceholderText(f"Enter {label_text}")
            # Set the default text to the current value of the attribute
            Map = self.selected_map
            default_text = str(Map.get_attribute(label_text))
            widget.setText(default_text)
            widget.editingFinished.connect(lambda label_text=label_text, widget=widget: self.update_map(label_text, widget.text()))
            widgets[label_text] = widget
        return widgets

    def change_text_boxes(self, attributes):
        for attribute, value in attributes.items():
            self.text_boxes[attribute].setText(str(value))

    def create_dropdown_list_box_maps(self):
        widget = QtWidgets.QComboBox()
        widget.addItems(['TinkerBell Map', 'Ikeda Map', 'Clifford Attractor'])

        # There is an alternate signal to send the text.
        widget.currentTextChanged.connect(self.get_map_selection)
        return widget

    def get_map_selection(self, map_name):
        # Manual test code: will be rewritten
        sim = Simulator(self.default_maps[map_name](), 50000)
        xs, ys = sim.simulate()
        self.selected_map = self.default_maps[map_name]()
        self.change_text_boxes(self.selected_map.get_attributes())
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
    
    def update_map(self, label_text, entered_text):
        map_name = self.dropdown_list_box.currentText()
        Map = self.selected_map
        
        if Map:
            if entered_text:
                entered_value = float(entered_text)
            else:
                entered_value = Map.get_attribute(label_text)
            Map.set_attribute(label_text, entered_value)
            simulator = Simulator(Map, 50000)
            
            xs, ys = simulator.simulate()
            print(xs[:6])
            self.plot_widget.clear()
            self.plot_widget.plot(xs, ys, pen=None, symbol='o', symbolSize=1)
        else:
            self.plot_widget.clear()
    


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()