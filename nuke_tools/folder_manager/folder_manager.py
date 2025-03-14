import sys
import traceback
import os
from PySide2 import QtWidgets, QtCore, QtGui


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        '''Folder Generator: creates a general folder structure for freelance projects'''

        super(MainWindow, self).__init__()
        #folder items
        self.Nuke = QtGui.QStandardItem()
        self.layers = QtGui.QStandardItem()
        self.scripts = QtGui.QStandardItem()
        self.renders = QtGui.QStandardItem()
        self.comprender = QtGui.QStandardItem()
        self.precomprender = QtGui.QStandardItem()
        self.compVersion = QtGui.QStandardItem()
        self.precompVersion = QtGui.QStandardItem()
        self.Layers = QtGui.QStandardItem()


        #layouts
        self.setWindowTitle('Folder Generator')
        self.generalLayout = QtWidgets.QVBoxLayout()
        self.path_layout = QtWidgets.QFormLayout()
        self.folder_layout = QtWidgets.QGridLayout()
        self.generalLayout.addLayout(self.path_layout)

        #setting central widget
        self.centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.generalLayout)

        #widgets
        self.root_path_le = QtWidgets.QLineEdit()
        self.model = QtGui.QStandardItemModel()
        self.tree = QtWidgets.QTreeView()
        self.tree.setHeaderHidden(True)
        self.rootNode = self.model.invisibleRootItem()
        self.tree.setModel(self.model)
        self.tree.setObjectName('tree')

        #setting main layout
        self.generalLayout.addWidget(self.tree)

        #button to create folders in root path
        self.createButton = QtWidgets.QPushButton('Create Folders')
        self.generalLayout.addWidget(self.createButton)
        self.createButton.pressed.connect(self.createFolders)

        #creating widgets
        self.createFolderWidgets()
        self.createRootPathWidget()

    def createRootPathWidget(self):
        # creating line edit for user to input the root folder path
        self.root_path_le.setFixedHeight(20)
        self.root_path_le.setAlignment(QtCore.Qt.AlignRight)
        self.path_layout.addRow('Folder Path: ', self.root_path_le)

    def createFolderWidgets(self):
        # creating folder widgets

        self.Nuke.setText('Nuke')
        self.Nuke.setEditable(False)
        self.rootNode.appendRow(self.Nuke)
        index = self.model.indexFromItem(self.Nuke)
        self.tree.setExpanded(index, True)

        self.renders.setText('Renders')
        self.renders.setEditable(False)
        self.Nuke.appendRow(self.renders)
        index = self.model.indexFromItem(self.renders)
        self.tree.setExpanded(index, True)

        self.comprender.setText('Comp')
        self.comprender.setEditable(False)
        self.renders.appendRow(self.comprender)
        index = self.model.indexFromItem(self.comprender)
        self.tree.setExpanded(index, True)

        self.compVersion.setText('Comp_v0001')
        self.compVersion.setEditable(False)
        self.comprender.appendRow(self.compVersion)
        index = self.model.indexFromItem(self.compVersion)
        self.tree.setExpanded(index, True)

        self.precomprender.setText('Precomp')
        self.precomprender.setEditable(False)
        self.renders.appendRow(self.precomprender)
        index = self.model.indexFromItem(self.precomprender)
        self.tree.setExpanded(index, True)

        self.precompVersion.setText('Precomp_01')
        self.precompVersion.setEditable(False)
        self.precomprender.appendRow(self.precompVersion)
        self.tree.setExpanded(index, True)

        self.scripts.setText('Scripts')
        self.scripts.setEditable(False)
        self.Nuke.appendRow(self.scripts)

        self.layers.setText('Layers')
        self.layers.setEditable(False)
        self.Nuke.appendRow(self.layers)




    def getPaths(self):
        # creating paths that match folder widgets
        rootpath = str(self.root_path_le.text())

        if not rootpath:
            print('Folder path is empty')
            return list()

        rootPath = os.path.join(rootpath)

        folders = {
                   'Renders': ['Comp\Comp_v0001', 'Precomp\Precomp_01'],
                   'Scripts': ['Scripts']
                   }

        folderPaths = list()

        for folder, subFolders in folders.items():
            newPath = os.path.join(rootPath, folder).replace('\\', '/')
            folderPaths.append(newPath)
            for subFolder in subFolders:
                subPath = os.path.join(newPath, subFolder).replace('\\', '/')
                folderPaths.append(subPath)

        return folderPaths

    def createFolders(self):
        # creating folders
        folderPaths = self.getPaths()
        for path in folderPaths:
            if not os.path.exists(path):
                print(path)
                print('Creating path:', path)
                try:
                    os.makedirs(path)
                except (IOError, PermissionError):
                    print('Attempt to create directory failed:', path)
                    traceback.print_exc()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
