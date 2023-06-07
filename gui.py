from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
from typing import Union
import chaotic_maps
import os

class MainWindow(QtWidgets.QMainWindow):
    '''
    Represents the main window of the program.
    When created, the selected map is set to TinkerBell Map.
    '''

    def __init__(self, *args, **kwargs):
        '''
        Initialize the main window.

        :return: None
        '''
        super(MainWindow, self).__init__(*args, **kwargs)
        self.default_maps = chaotic_maps.default_maps
        # Set initial map to TinkerBell Map.
        self.selected_map = self.default_maps['TinkerBell Map']()

        self.setWindowTitle("Draw Chaotic Map")
        self.title = self.create_title()
        self.dropdown_list_box = self.create_dropdown_list_box_maps()
        # Create main text boxes with labels a, b, c, d, x0, y0.
        # The text boxes are always visible.
        # Note, when changing a text of a given text box, the effect will be seen
        # in the main window.
        self.main_text_boxes = self.create_labeled_main_text_boxes()
        # Create sub text boxes with labels xmin, xmax, ymin, ymax, step
        # These boxes are important for changing sim range for maps that
        # require multi point sim.
        # The text boxes are visible only for certain maps.
        # Note, when changing a text of a given text box, the effect will be seen
        # in the main window.
        self.sub_text_boxes = self.create_labeled_sub_text_boxes()
        # Create containers for proper layout
        self.container_lable_text_box = self.create_container_label_text_boxes(self.main_text_boxes)
        self.container_sub_text_boxes = self.create_container_sub_text_boxes(self.sub_text_boxes)
        self.plot_widget = self.create_graph_space()

        self.set_main_layout([self.title, self.dropdown_list_box, self.container_lable_text_box, self.container_sub_text_boxes, self.plot_widget])

        xs, ys = self.simulate_map()
        self.plot_widget.clear()
        self.plot_widget.plot(xs, ys, pen=None, symbol='o', symbolSize=1)

    def simulate_map(self, n: int = 50000) -> tuple[list[int], list[int]]:
        '''
        Simulate current map with a given number of iterations.

        :param n: int number of iterations for simulation
        :return: tuple in format (xs, ys)
            where xs is the list of points on x-axis
            and ys is the list of points on y-axis
        '''
        simulator = chaotic_maps.Simulator(self.selected_map, n)
        xs, ys = simulator.simulate()
        return xs,ys

    def set_main_layout(self, widgets) -> None:
        '''
        Set the main layout for the main window.

        :return: None
        '''
        layout = QtWidgets.QVBoxLayout()
        for widget in widgets:
            layout.addWidget(widget)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    
    def create_container_text_boxes(self, text_boxes: dict[str, QtWidgets.QLineEdit], layout_type: Union[QtWidgets.QVBoxLayout, QtWidgets.QHBoxLayout]) -> QtWidgets.QWidget:
        '''
        Create a container of labeled text boxes with a specific layout type
        out of a provided dictionary of str labels and coresponding text boxes.

        :param text_boxes: dict of format [str: QLineEdit]
        :param layout_type: QtWidgets.QVBoxLayout or QtWidgets.QHBoxLayout - preferred layout type
        :return: QWidget a widget out of text_boxes with preferred layout type
        '''
        valid_layout = (QtWidgets.QVBoxLayout, QtWidgets.QHBoxLayout)
        if not layout_type in valid_layout:
            raise ValueError('Invalid layout_type. Expected QVBoxLayout or QHBoxLayout.')
        
        widget = QtWidgets.QWidget()
        layout = layout_type()
        for label_text, widget_textbox in text_boxes.items():
            container_text_box = self.create_container_text_box(label_text, widget_textbox)
            layout.addWidget(container_text_box)
        widget.setLayout(layout)
        return widget
    
    def create_container_text_box(self, label_text: str, widget_textbox: QtWidgets.QLineEdit) -> QtWidgets.QWidget:
        '''
        Create a container widget out of str label name and textbox widget.
        Label name is placed to the left of the textbox.

        :param label_text: str label name
        :param widget_textbox: QLineEdit textbox
        :return: QWidget container widget with textbox and its label to the left of it.
        '''
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        # Set margins for the container, so that when later used, widgets wouldn't
        # be too spaced out.
        layout.setContentsMargins(1, 2, 5, 2)
        widget_label = QtWidgets.QLabel(label_text)
        layout.addWidget(widget_label)
        layout.addWidget(widget_textbox)
        widget.setLayout(layout)
        return widget
    
    def create_container_label_text_boxes(self, text_boxes):
        '''
        Create a container of labeled text boxes with a QVBoxLayout
        out of a provided dictionary of str labels and coresponding text boxes.
        The container is inteded to be later used inside other layout.

        :param text_boxes: dict of format [str: QLineEdit].
        :return: QWidget a widget out of text_boxes with QVBoxLayout
        '''
        return self.create_container_text_boxes(text_boxes, QtWidgets.QVBoxLayout)

    def create_container_sub_text_boxes(self, text_boxes):
        '''
        Create a container of labeled text boxes with a QHBoxLayout
        out of a provided dictionary of str labels and coresponding text boxes.
        The container's visibility depends on whether a selected map requires
        multi point sim or not.
        The container is inteded to be later used inside other layout.

        :param text_boxes: dict of format [str: QLineEdit].
        :return: QWidget a widget out of text_boxes with QHBoxLayout
        '''
        container = self.create_container_text_boxes(text_boxes, QtWidgets.QHBoxLayout)
        container.setVisible(self.selected_map.is_multi_point_sim)
        return container

    def create_labeled_text_boxes(self, text_labels: list[str]) -> dict[str, QtWidgets.QLineEdit]:
        '''
        Create a dictionary of labeles and corresponding text boxes.
        When value of text boxes is changed, the selected map is updated.

        :param text_labels: list of str(label names)
        :return: dict in format {str: QtWidgets.QLineEdit} 
            dictionary of labeles and corresponding text boxes
        '''
        widgets = {}
        for label_text in text_labels:
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
    
    def create_labeled_sub_text_boxes(self) -> dict[str, QtWidgets.QLineEdit]:
        '''
        Create a dictionary of labeles and corresponding main text boxes.
        When value of text boxes is changed, the selected map is updated.

        :return: dict in format {str: QtWidgets.QLineEdit} 
            dictionary of labeles and corresponding text boxes
            the labels are 'xmin', 'xmax', 'ymin', 'ymax', 'step_size'
        '''
        return self.create_labeled_text_boxes(['xmin', 'xmax', 'ymin', 'ymax', 'step_size'])
    
    def create_labeled_main_text_boxes(self) -> dict[str, QtWidgets.QLineEdit]:
        '''
        Create a dictionary of labeles and corresponding sub text boxes.
        When value of text boxes is changed, the selected map is updated.

        :return: dict in format {str: QtWidgets.QLineEdit} 
            dictionary of labeles and corresponding text boxes
            the labels are 'a', 'b', 'c', 'd', 'x0', 'y0'
        '''
        return self.create_labeled_text_boxes(['a', 'b', 'c', 'd', 'x0', 'y0'])

    def change_text_boxes(self) -> None:
        '''
        Update text box values with current map constants.

        :return: None
        '''
        attributes = self.selected_map.get_attributes()
        for attribute, value in attributes.items():
            self.main_text_boxes[attribute].setText(str(value))

    def create_dropdown_list_box_maps(self) -> QtWidgets.QComboBox:
        '''
        Create a dropdown box with default map names.
        When a selection is changed, the map plot will be redrawn.

        :return: QtWidgets.QComboBox dropdown box with default map names
        '''
        widget = QtWidgets.QComboBox()
        widget.addItems([map_name for map_name in self.default_maps])

        # There is an alternate signal to send the text.
        widget.currentTextChanged.connect(self.change_map_selection)
        return widget

    def change_map_selection(self, map_name: str) -> None:
        '''
        Process map selection change by running a new simulation
        and updating the plot.

        :param map_name: str name of a map
        :return: None
        '''
        self.selected_map = self.default_maps[map_name]()
        xs, ys = self.simulate_map()
        self.change_text_boxes()
        self.change_sub_text_boxes()
        self.plot_widget.clear()
        self.plot_widget.plot(xs, ys, pen=None, symbol='o', symbolSize=1)
        # Reset zoom of the plot_widget to fill the plot fully with graph
        self.plot_widget.plotItem.vb.autoRange()
    
    def change_sub_text_boxes(self) -> None:
        '''
        Update sub text box values with current map constants.
        The sub text boxes's visibility depends on whether a selected map requires
        multi point sim or not.

        :return: None
        '''
        if self.selected_map.is_multi_point_sim:
        # Update the existing sub text boxes
            for label_text, widget_textbox in self.sub_text_boxes.items():
                widget_textbox.setText(str(self.selected_map.get_attribute(label_text)))

        self.container_sub_text_boxes.setVisible(self.selected_map.is_multi_point_sim)

    def create_title(self) -> QtWidgets.QLabel:
        '''
        Create 'Draw Chaotic Map' title widget.

        :return: QLabel title set to 'Draw Chaotic Map'
        '''
        widget = QtWidgets.QLabel('Draw Chaotic Map')
        font = widget.font()
        font.setPointSize(30)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        return widget
    
    def create_graph_space(self) -> pg.PlotWidget:
        '''
        Create graph space widget.

        :return: PlotWidget graph space
        '''
        plot_widget = pg.PlotWidget()
        plot_widget.setBackground('w')
        return plot_widget
    
    def update_map(self, label_text: str, entered_text: str) -> None:
        '''
        Update selected map and change graph plot.

        :param label_text: str name of the parameter to be changed
        :param entered_text: str vale to be set for the parameter
        :return: None
        '''
        Map = self.selected_map
        
        if Map:
            if entered_text:
                entered_value = float(entered_text)
            else:
                entered_value = 0
                self.main_text_boxes[label_text].setText(str(0))
            Map.set_attribute(label_text, entered_value)
            xs, ys = self.simulate_map()
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