from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
from typing import Union
import chaotic_maps
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.default_maps = chaotic_maps.default_maps
        self.selected_map = self.default_maps['TinkerBell Map']()

        self.setWindowTitle("Draw Chaotic Map")
        self.title = self.create_title()
        self.dropdown_list_box = self.create_dropdown_list_box_maps()
        self.text_boxes = self.create_main_text_boxes()
        self.sub_text_boxes = self.create_sub_text_boxes()
        self.container_lable_text_box = self.create_container_label_text_boxes(self.text_boxes)
        self.container_sub_text_boxes = self.create_container_sub_text_boxes(self.sub_text_boxes)
        self.plot_widget = self.create_graph_space()
        self.set_layout([self.title, self.dropdown_list_box, self.container_lable_text_box, self.container_sub_text_boxes, self.plot_widget])

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
    
    def create_container_text_boxes(self, text_boxes: dict, layout_type: Union[QtWidgets.QVBoxLayout, QtWidgets.QHBoxLayout]) -> QtWidgets.QWidget:
        '''
        Create a container of labeled text boxes with a specific layout type

        '''
        valid_layout = (QtWidgets.QVBoxLayout, QtWidgets.QHBoxLayout)
        if not layout_type in valid_layout:
            raise ValueError('Invalid layout_type. Expected QVBoxLayout or QHBoxLayout.')
        
        widget = QtWidgets.QWidget()
        layout = layout_type(widget)
        for label_text, widget_textbox in text_boxes.items():
            container_text_box = self.create_container_text_box(label_text, widget_textbox)
            layout.addWidget(container_text_box)
        return widget
    
    def create_container_text_box(self, label_text: str, widget_textbox: QtWidgets.QLineEdit):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(1, 1, 1, 1)
        widget_label = QtWidgets.QLabel(label_text)
        layout.addWidget(widget_label)
        layout.addWidget(widget_textbox)
        return widget
    
    def create_container_label_text_boxes(self, text_boxes):
        return self.create_container_text_boxes(text_boxes, QtWidgets.QVBoxLayout)

    def create_container_sub_text_boxes(self, text_boxes):
        container = self.create_container_text_boxes(text_boxes, QtWidgets.QHBoxLayout)
        container.setVisible(self.selected_map.is_multi_point_sim)
        return container

    def create_sub_text_boxes(self):
        widgets = {}
        for label_text in ['xmin', 'xmax', 'ymin', 'ymax', 'step_size']:
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
    
    def create_main_text_boxes(self):
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

    def create_text_box(self, label_text):
        widget = QtWidgets.QLineEdit()
        widget.setMaxLength(10)
        widget.setPlaceholderText(f"Enter {label_text}")
        # Set the default text to the current value of the attribute
        Map = self.selected_map
        default_text = str(Map.get_attribute(label_text))
        widget.setText(default_text)

    def change_text_boxes(self, attributes):
        for attribute, value in attributes.items():
            self.text_boxes[attribute].setText(str(value))

    def create_dropdown_list_box_maps(self):
        widget = QtWidgets.QComboBox()
        widget.addItems([map_name for map_name in self.default_maps])

        # There is an alternate signal to send the text.
        widget.currentTextChanged.connect(self.change_map_selection)
        return widget

    def change_map_selection(self, map_name):
        # Manual test code: will be rewritten
        sim = chaotic_maps.Simulator(self.default_maps[map_name](), 50000)
        xs, ys = sim.simulate()
        self.selected_map = self.default_maps[map_name]()
        self.change_text_boxes(self.selected_map.get_attributes())
        self.update_sub_text_boxes()
        self.plot_widget.clear()
        self.plot_widget.plot(xs, ys, pen=None, symbol='o', symbolSize=1)
        #self.plot_widget.plotItem.vb.autoRange()
    
    def update_sub_text_boxes(self):
        if self.selected_map.is_multi_point_sim:
        # Update the existing sub text boxes
            for label_text, widget_textbox in self.sub_text_boxes.items():
                widget_textbox.setText(str(self.selected_map.get_attribute(label_text)))

        self.container_sub_text_boxes.setVisible(self.selected_map.is_multi_point_sim)

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
                self.text_boxes[label_text].setText(str(0))
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