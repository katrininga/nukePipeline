import nuke
import sys
from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        #creating widgets, os stands for overscan
        self.os_threshold_label = QtWidgets.QLabel("Overscan Threshold: ")
        self.os_threshold_input = QtWidgets.QLineEdit("1000")
        self.os_check_button = QtWidgets.QPushButton("Check Overscans")
        self.os_results = QtWidgets.QTableWidget()

        #creating layout
        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.addWidget(self.os_threshold_label, 0, 0)
        self.main_layout.addWidget(self.os_threshold_input, 0, 1)
        self.main_layout.addWidget(self.os_check_button, 1, 0, 1, 2)
        self.main_layout.addWidget(self.os_results, 2, 0, 1, 3)

        # Set layout for the window
        self.setLayout(self.main_layout)

    def get_threshold_value(self):
        threshold_value = 1000
        try:
            threshold_value = int(self.os_threshold_input.text())
        except ValueError:
            print("Invalid number entered!")

        return threshold_value


    def check_bbox_out_of_bounds(self):
        """
        Checks if any node's bounding box exceeds the project resolution by more than 300 pixels.
        Prints the node name and bbox size if it does.
        """
        # Get project resolution from root format
        root = nuke.root()
        project_format = root.format()
        proj_width = project_format.width()
        proj_height = project_format.height()
        bbox_data = dict()
        sorted_data = dict()

        # Threshold for exceeding the resolution
        threshold = 1000
        try:
            threshold = int(self.os_threshold_input.text())
        except ValueError:
            print("Invalid threshold value! setting to 1000")


        #TODO: set up a proper log system
        print(f"\nChecking for nodes with bounding boxes exceeding project resolution by more than {threshold} pixels...\n")

        # Iterate through all nodes
        for node in nuke.allNodes():
            try:
                # Ensure the node has a bbox() method (some nodes like BackdropNode don’t)
                if not hasattr(node, "bbox"):
                    continue

                # Get the bounding box
                bbox = node.bbox()
                x, y, h, w = bbox.x(), bbox.y(), bbox.h(), bbox.w()
                width = h - x
                height = w - y

                # Check if the bounding box exceeds project resolution by more than 300 pixels
                if (x < -threshold or y < -threshold or h > proj_width + threshold or w > proj_height + threshold):
                    total_size = int(width*height)
                    bbox_data[node.name()] = {"size": total_size, "X": x, "Y": y, "H": h, "W": w}
                    sorted_data = dict(sorted(bbox_data.items(), key=lambda item: item[1]["size"], reverse=False))

            except Exception as e:
                #TODO: log warning instead of print statement
                print(f"Skipping node {node.name()} due to error: {e}")

        return sorted_data


    def populate_result_table(self):
        # Get data from check_bbox_out_of_bounds()
        bbox_data = self.check_bbox_out_of_bounds()

        # Set up table
        self.os_results.setRowCount(len(bbox_data))  # Set rows based on data size
        self.os_results.setColumnCount(5)  # 5 columns: Name, X, Y, H, W
        self.os_results.setHorizontalHeaderLabels(["Node Name", "X", "Y", "H", "W"])

        # Populate table
        for row, (node_name, values) in enumerate(bbox_data.items()):
            self.os_results.setItem(row, 0, QtWidgets.QTableWidget(node_name))
            self.os_results.setItem(row, 1, QtWidgets.QTableWidget(str(values["X"])))
            self.os_results.setItem(row, 2, QtWidgets.QTableWidget(str(values["Y"])))
            self.os_results.setItem(row, 3, QtWidgets.QTableWidget(str(values["H"])))
            self.os_results.setItem(row, 4, QtWidgets.QTableWidget(str(values["W"])))



# showing the widget
app = QtWidgets.QApplication(sys.argv)
widget = MainWindow()
widget.show()
sys.exit(app.exec_())