from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
import chaotic_maps
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.default_maps = {
            'TinkerBell Map': chaotic_maps.TinkerbellMap,
            'Ikeda Map': chaotic_maps.IkedaMap,
            'Clifford Attractor': chaotic_maps.CliffordAttractor,
            'Bogdanov Map': chaotic_maps.BogdanovMap, # Bogdanov map does not work with the default range provided for sim
            'Gingerbread Map': chaotic_maps.GingerbreadMap,
            'Standard Map': chaotic_maps.StandardMap,
            'Gumowski-Mira Attractor': chaotic_maps.GumowskiMiraAttractor
        }
        self.selected_map = chaotic_maps.TinkerbellMap()
        self.setWindowTitle("Draw Chaotic Map")
        self.title = self.create_title()
        self.dropdown_list_box = self.create_dropdown_list_box_maps()
        self.text_boxes = self.create_text_boxes()
        self.container_lable_text_box = self.create_container_lable_text_box(self.text_boxes)
        self.plot_widget = self.create_graph_space()
        self.set_layout([self.title, self.dropdown_list_box, self.container_lable_text_box, self.plot_widget])
        simulator = chaotic_maps.Simulator(self.selected_map, 50000)
        xs, ys = simulator.simulate()
        self.plot_widget.clear()
        self.plot_widget.plot(xs, ys, pen=None, symbol='o', symbolSize=1)

    def set_layout(self, widgets):
        layout = QtWidgets.QVBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def create_container_lable_text_box(self, text_boxes):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        row = 0
        for label_text, widget_textbox in text_boxes.items():
            widget_label = QtWidgets.QLabel(label_text)
            layout.addWidget(widget_label, row, 0)
            layout.addWidget(widget_textbox, row, 1)
            row += 1
        return widget

    def create_text_boxes(self):
        widgets = {}
        for label_text in ['a', 'b', 'c', 'd', 'x0', 'y0']:
            
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
        widget.addItems([map_name for map_name in self.default_maps])

        # There is an alternate signal to send the text.
        widget.currentTextChanged.connect(self.get_map_selection)
        return widget

    def get_map_selection(self, map_name):
        # Manual test code: will be rewritten
        sim = chaotic_maps.Simulator(self.default_maps[map_name](), 50000)
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
                entered_value = 0
            Map.set_attribute(label_text, entered_value)
            simulator = chaotic_maps.Simulator(Map, 50000)
            
            xs, ys = simulator.simulate()
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