import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget,QLabel,QVBoxLayout,QHBoxLayout,QLineEdit,QSpacerItem,QTableWidget,QTextEdit,QTableWidgetItem
from PyQt6.QtCore import Qt, pyqtSlot
import qmc

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
        self.user_input = QLineEdit()
        inputWidget.addWidget(self.user_input,15)
        inputWidget.addItem(QSpacerItem(20,10))
        self.input_button = QPushButton('Generate Table')
        self.input_button.clicked.connect(self.update_table)
        inputWidget.addWidget(self.input_button,1)

        #table
        self.tableWidget = QVBoxLayout()
        table_title = QLabel('Truth table')
        self.table = QTableWidget(0,0)
        self.tableWidget.addWidget(table_title,1)
        self.tableWidget.addWidget(self.table,15)

        #options
        optionsWidget = QHBoxLayout()
        self.clear_button = QPushButton('Clear table')
        self.clear_button.clicked.connect(self.clear_table)
        logic_function_button = QPushButton('Get Logic Function')
        spacer = QSpacerItem(50,10)
        optionsWidget.addWidget(self.clear_button)
        optionsWidget.addItem(spacer)
        optionsWidget.addWidget(logic_function_button)

        fpWidget.addLayout(inputWidget)
        fpWidget.addLayout(self.tableWidget)
        fpWidget.addLayout(optionsWidget)

        #############

        #second part
        sp_layout_widget = QVBoxLayout()

        process_label = QLabel('Process')
        process_area = QTextEdit()
        result_label = QLabel('Result')
        result_area = QTextEdit()

        sp_layout_widget.addWidget(process_label,1)
        sp_layout_widget.addWidget(process_area,20)
        sp_layout_widget.addWidget(result_label,1)
        sp_layout_widget.addWidget(result_area,8)

        #adding main widget to window
        mainLayout.addLayout(fpWidget,1)
        mainLayout.addLayout(sp_layout_widget,1)
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

    @pyqtSlot()
    def update_table(self)->None:
        ####Getting total of inputs
        total_inputs = int(self.user_input.text())
        self.user_input.clear()

        ####Disable editting of cells
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        ####
        self.table.cellDoubleClicked.connect(self.cell_clicked)

        ####Setting table size
        self.table.setColumnCount(total_inputs+1)
        self.table.setRowCount(2**total_inputs)
        ####Setting vertical headers
        vertical_headers = [str(i) for i in range(0,2**total_inputs)]
        self.table.setVerticalHeaderLabels(vertical_headers)
        ####Setting horizontal headers
        header_labels = []
        for i in range(total_inputs):
            header_labels.append(str(chr(65+i)))
        header_labels.append('function output')
        self.table.setHorizontalHeaderLabels(header_labels)
        ####
        self.last_coloumn = total_inputs

        ####Filling table
        for i in range(0,(2**total_inputs)):
            bits_number = qmc.int_to_str_bin(i,total_inputs)
            for j in range(0,len(bits_number)+1):
                if j < len(bits_number):
                    self.table.setItem(i,j,QTableWidgetItem(bits_number[j]))
                else:
                    self.table.setItem(i,j,QTableWidgetItem('0'))

    @pyqtSlot()
    def clear_table(self)->None:
        new_table = QTableWidget(0,0)
        self.tableWidget.replaceWidget(self.table,new_table)
        #self.table.deleteLater()
        self.table = new_table

    @pyqtSlot()
    def cell_clicked(self)->None:
        row = self.table.currentRow()
        column = self.table.currentColumn()
        if column == self.last_coloumn:
            current_value = self.table.item(row,column).text()
            if current_value == '0':
                self.table.item(row,column).setText('1')
            elif current_value == '1':
                self.table.item(row,column).setText('0')
            

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()