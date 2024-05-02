import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget,QLabel,QVBoxLayout,QHBoxLayout,QLineEdit,QSpacerItem,QTableWidget,QTextEdit,QTableWidgetItem
from PyQt6.QtCore import Qt, pyqtSlot
import qmc
from PyQt6.QtGui import QFont

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
        self.logic_function_button = QPushButton('Get Logic Function')
        self.logic_function_button.clicked.connect(self.quineMcClusky)
        spacer = QSpacerItem(50,10)
        optionsWidget.addWidget(self.clear_button)
        optionsWidget.addItem(spacer)
        optionsWidget.addWidget(self.logic_function_button)

        fpWidget.addLayout(inputWidget)
        fpWidget.addLayout(self.tableWidget)
        fpWidget.addLayout(optionsWidget)

        #############

        #second part
        sp_layout_widget = QVBoxLayout()

        process_label = QLabel('Process')
        self.process_area = QTextEdit()
        self.process_area.setFont(QFont("Courier New", 10))
        result_label = QLabel('Result')
        self.result_area = QTextEdit()

        sp_layout_widget.addWidget(process_label,1)
        sp_layout_widget.addWidget(self.process_area,20)
        sp_layout_widget.addWidget(result_label,1)
        sp_layout_widget.addWidget(self.result_area,8)

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

    def group_minterms(self,size:int,rows:list)->list:
        first_group = qmc.group_rows(rows)
        lists = [first_group]#table concent it is here

        pairs = qmc.look_for_matched_pairs(first_group,size)
        while len(pairs) > 0:
            lists.append(pairs)
            pairs = qmc.look_for_matched_pairs(pairs,size)

        #------Adding tables to process text area
        for table in lists:
            self.process_area.append(' index |          minterm          |     binary     |    prime')
            self.process_area.append('--------------------------------------------------------------')
            for key in table:
                for row in table[key]:
                    for minterm in row[0]:
                        self.process_area.append( str(key).center(7) + '|' + str(minterm).center(28) + "|" + row[2].center(16) + "|" + str(row[1]).center(10))
                    if row != table[key][-1]:
                        self.process_area.append('       -------------------------------------------------------')
                    else:
                        self.process_area.append('--------------------------------------------------------------')
            self.process_area.append("\n")
        return lists

    def get_and_show_primeImplicans(self,tables:list)->list:
        prime_implicants = qmc.look_for_prime_implicants(lists=tables)
        text = "Prime implicants: {"
        for prime_implicant in prime_implicants:
            text += prime_implicant[0] + ","
        text = text[:-1]
        text+= "}"
        self.process_area.append(text)
        self.process_area.append("\n")
        return prime_implicants
    
    def get_prime_implicant_table(self,prime_implicants:list,minterms:list,size:int)->dict:
        table = qmc.prime_implicant_table(prime_implicants,minterms)
        
        keys = list(table.keys())
        columns = []
        header = "  " + (" " * size) + " |"
        for key in keys:
            header += " " + key + " |"
            columns.append(key)
        self.process_area.append(header)

        reverse_table = {}
        for key in keys:
            for prime in table[key]:
                if prime not in reverse_table.keys():
                    reverse_table[prime] = [key]
                else:
                    reverse_table[prime].append(key)

        self.process_area.append("-" + ("-" * ((size+3) * (len(keys)+1) )))
        for prime in reverse_table:
            row = header = "| " + prime + " |"
            accepted_values = []
            for value in reverse_table[prime]:
                for column in columns:
                    if value == column:
                        accepted_values.append(column)

            for column in columns:
                if column in accepted_values:
                    row += " " + "x".center(size) + " |"
                else:
                    row += " " + (" " * size) + " |"
            self.process_area.append(row)
            self.process_area.append("-" + ("-" * ((size+3) * (len(keys)+1) )))
        self.process_area.append("\n")

        return table
    
    def simplification(self,table:dict)->list:
        binaries = list(qmc.simplification(table))
        text = "Prime implicants selected from the simplification process: "
        for binary in binaries:
            text+= binary + ", "
        text = text[:-2]
        self.process_area.append(text)
        self.process_area.append("\n")
        return binaries
    
    def get_logic_func(self,primes:list)->str:
        logic_func = qmc.create_function(primes)
        self.result_area.append("f = " + logic_func)
        return logic_func

    @pyqtSlot()
    def quineMcClusky(self)->None:
        minterms = []
        size = self.last_coloumn
        for i in range(0,self.table.rowCount()):
            item = self.table.item(i,self.last_coloumn)
            if item.text() == '1':
                minterms.append(i)
        rows = [qmc.int_to_str_bin(minterm,size) for minterm in minterms]
        lists = self.group_minterms(size,rows)
        prime_implicants = self.get_and_show_primeImplicans(lists)
        last_table = self.get_prime_implicant_table(prime_implicants,rows,size)
        picked_primes = self.simplification(last_table)
        self.get_logic_func(picked_primes)
            

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()