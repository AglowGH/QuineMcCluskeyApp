import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget,QLabel,QVBoxLayout,QHBoxLayout,QLineEdit,QSpacerItem
from PyQt6.QtCore import Qt, pyqtSlot

@pyqtSlot()
def say_hello():
    print("Button cliked!!")

#button = QPushButton("Click")
#button.clicked.connect(say_hello)


class Window(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        #setting windows size
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)
        self.setWindowTitle("QuineMcCluskey app")

        #main widget
        mainWidget = QWidget()
        mainLayout = QHBoxLayout()

        #first part
        fpWidget = QVBoxLayout()

        #input
        inputWidget = QHBoxLayout()
        input_label = QLabel('Input')
        inputWidget.addWidget(input_label,1)
        user_input = QLineEdit()
        inputWidget.addWidget(user_input,15)
        inputWidget.addItem(QSpacerItem(20,10))
        input_button = QPushButton('Generate Table')
        inputWidget.addWidget(input_button,1)

        #table
        tableWidget = QVBoxLayout()
        table_title = QLabel('Truth table')
        table = QLabel('Table should be here...')
        tableWidget.addWidget(table_title,1)
        tableWidget.addWidget(table,15)

        #options
        optionsWidget = QHBoxLayout()
        clear_button = QPushButton('Clear table')
        logic_function_button = QPushButton('Get Logic Function')
        spacer = QSpacerItem(50,10)
        optionsWidget.addWidget(clear_button)
        optionsWidget.addItem(spacer)
        optionsWidget.addWidget(logic_function_button)

        fpWidget.addLayout(inputWidget)
        fpWidget.addLayout(tableWidget)
        fpWidget.addLayout(optionsWidget)

        #############

        #second part
        sp_layout_widget = QVBoxLayout()

        process_label = QLabel('Process')
        process_area = QLabel('Procedure should be here...')
        result_label = QLabel('Result')
        result_area = QLabel('Result area should be here....')

        sp_layout_widget.addWidget(process_label,1)
        sp_layout_widget.addWidget(process_area,20)
        sp_layout_widget.addWidget(result_label,1)
        sp_layout_widget.addWidget(result_area,8)

        #adding main widget to window
        mainLayout.addLayout(fpWidget,1)
        mainLayout.addLayout(sp_layout_widget,1)
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()