import sys
import numpy as num
import csv
import statistics as sta
import random as rand
import pyqtgraph as pg
import pandas as pd
from PyQt5 import QtGui as gu
from PyQt5.QtCore import QLine,QSize,Qt,pyqtSignal,QRunnable,QThread,QThreadPool,QAbstractTableModel,QVariant
from PyQt5.QtWidgets import (
QApplication,
QWidget,
QMainWindow,
QLabel,
QPushButton,
QVBoxLayout,
QGridLayout,
QLineEdit,
QHBoxLayout,
QCheckBox,
QComboBox,
QTabWidget,
QToolBar,
QAction,
QStatusBar,
QMenuBar,
QMenu,
QListWidget,
QSpinBox,
QSlider,
QDialog,
QDialogButtonBox,
QMainWindow,
QPushButton,
QMessageBox,
QPlainTextEdit,
QTextEdit,
QFileDialog,
QTableView,
)
class Variables():
    def __init__(self):
        super().__init__()
        Variables.column1 = []
        Variables.column2 = []
        Variables.column3 = []
        Variables.column4 = []
        Variables.saved1 = []
        Variables.saved2 = []
        Variables.saved3 = []
        Variables.saved4 = []
        Variables.list_of_lists = []

#class Legend_CheckBox(QCheckBox):
 #   def __init__(self):
  #      super().__init__()
   #     unchecked = pyqtSignal(int)

class TableView(QAbstractTableModel):
    def __init__(self, infos=None):
        super(TableView, self).__init__()

        self.infos = [] or infos

    def data(self,index,role):
        if role == Qt.DisplayRole:
            #i = index.row()
            #j = index.column()
            #text = self.infos[index.column()]
            return QVariant(str(self.infos.iloc[index.row()][index.column()]))
        return QVariant()

    def rowCount(self, index):
        return len(self.infos.index)
    def columnCount(self,index):
        return len(self.infos.columns.values)

class TableViewWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table_view = QTableView()
        self.setWindowTitle("Table von CSV OP")
        self.setMinimumWidth(700)


        self.df = pd.DataFrame(Variables.list_of_lists)
        infos = self.df
        print(self.df)

        self.model = TableView()
        self.model = TableView(infos)
        self.table_view.setModel(self.model)

        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


class PlotsubWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    #Plots
        self.ploty = pg.PlotWidget()
        self.setWindowTitle("Plot CSV OP")
        self.ploty.setBackground("#242526")
        self.ploty.setLabel('left', 'Y', color="#ffffff")
        self.ploty.setLabel('bottom', 'CSV Column', color="#ffffff")
        #self.setMouseTracking(True)

        self.ploty.setTitle("CSV Data Plotted", color="w", size="18pt")

        #print("SAVED",type(Variables.saved1[0]))
        #print("PEN",type(self.pens))

        x_column1 = Variables.column1
        y_column1 = [_ for _ in list(range(len(Variables.column1)))]
        #self.plot_widget.addItem(self.plot_data[i])
        #self.data1 = [x_column1, y_column]

        #print("Column1",x_column1)
        #print("Range",y_column)

        x_column2 = Variables.column2
        y_column2 = [_ for _ in list(range(len(Variables.column2)))]
        #print("Column2", x_column2)
        #print("Range", y_column)

        x_column3 = Variables.column3
        y_column3 = [_ for _ in list(range(len(Variables.column3)))]
        #print("Column3", x_column3)
        #print("Range", y_column)

        x_column4 = Variables.column4
        y_column4 = [_ for _ in list(range(len(Variables.column4)))]
        #print("Column4", x_column4)
        #print("Range", y_column)
        self.ploty.addLegend()

        self.ploty.showGrid(x=True, y=True)

    #Buttons
        self.stat_button = QPushButton("Statistiken")
        self.stat_button.clicked.connect(self.statistiken_plot_clicked)

        self.remove_button = QPushButton("remove Statistiken")

    #CheckBoxs with connection
        self.num = 4
        self.check_boxes = [QCheckBox(f"Column {i + 1}") for i in range(self.num)]
        for i in range(self.num):
            self.check_boxes[i].stateChanged.connect(self.box_changed)

        self.h_box = QHBoxLayout()
        #self.h_box.addWidget(self.remove_button)
        self.h_box.addWidget(self.stat_button)


        self.layout = QVBoxLayout()
        self.layout.addWidget(self.ploty)
        for i in range(self.num):
            self.layout.addWidget(self.check_boxes[i])

        self.layout.addLayout(self.h_box)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    #Data für Plot
        self.plot_data = [None for _ in range(self.num)]
    #Damit alle checkboxs sicherlich ungecheickt sind
        self.state = [False for _ in range(self.num)]

        self.box_data = [[[0], [0]] for _ in range(self.num)]
        self.add_data(x_column1, y_column1, 0)
        self.add_data(x_column2, y_column2, 1)
        self.add_data(x_column3, y_column3, 2)
        self.add_data(x_column4, y_column4, 3)

    def add_data(self, x, y, ind):

        self.box_data[ind] = [x, y]
        if self.plot_data[ind] is not None:
            self.plot_data[ind].setData(x, y)

    def box_changed(self):
        for i in range(self.num):
            if self.check_boxes[i].isChecked() != self.state[i]:
                self.state[i] = self.check_boxes[i].isChecked()
                if self.state[i]:
                    if self.plot_data[i] is not None:
                        self.ploty.addItem(self.plot_data[i])
                    else:
                        try:
                           self.plot_data[i] = self.ploty.plot(*self.box_data[i], name=f'Column{i+1}',pen=(self.pens()),symbol ="o")
                        except ValueError:
                            print("Couldn't plot one item")

                else:
                    self.ploty.removeItem(self.plot_data[i])
                break

    def pens(self,color=[]):
        rgb = list(range(255))
        color= [rand.choice(rgb),rand.choice(rgb),rand.choice(rgb)]
        pen = pg.mkPen(color=(color), width=3)
        return pen

    def statistiken_plot_clicked(self,checked):
        try:
           x_saved1 = Variables.saved1
           y_saved = [_ for _ in list(range(len(Variables.saved1)))]
           self.ploty.plot(x_saved1, y_saved, name='Statistiken1', pen=pg.mkPen(self.pens(), width=3), symbol='o')
        except ValueError:
            print("Couldn't plot an item")

        try:
           x_saved2 = Variables.saved2
           y_saved = [_ for _ in list(range(len(Variables.saved2)))]
           self.ploty.plot(x_saved2, y_saved, name='Statistiken2', pen=pg.mkPen(self.pens(), width=3), symbol='+')
        except ValueError:
            print("Couldn't plot an item")

        try:
           x_saved3 = Variables.saved3
           y_saved = [_ for _ in list(range(len(Variables.saved3)))]
           self.ploty.plot(x_saved3, y_saved, name='Statistiken3', pen=pg.mkPen(self.pens(), width=3), symbol='x')
        except ValueError:
            print("Couldn't plot an item")

        try:
           x_saved4 = Variables.saved4
           y_saved = [_ for _ in list(range(len(Variables.saved4)))]
           self.ploty.plot(x_saved4, y_saved, name='Statistiken4', pen=pg.mkPen(self.pens(), width=3), symbol='o')
        except ValueError:
            print("Couldn't plot an item")
    #Complete the String detector
    #def string_detector(self):



class MainWindow(QMainWindow):
      """-This is a programm that opens a CSV data with length of 4 and caluclate max, min, medien, average and variance.
    -you can click (CTRL+o) to do all the operations on the choosen column.
    -you can also save all the statistics with the save button, the button will create a .txt named New Data which contains
     all the statistics and the comments.
     -you can reset the data and the statistics with the button reset or it's shortcut."""

      def __init__(self):
          super().__init__()
          self.setWindowTitle("CSV OP")

        #Variables
          Variables.column1 = []
          Variables.column2 = []
          Variables.column3 = []
          Variables.column4 = []
          Variables.saved1 = []
          Variables.saved2 = []
          Variables.saved3 = []
          Variables.saved4 = []
          Variables.list_of_lists = []

        #Labels
          self.label_datei = QLabel("Datei Auswahl:")

        #Plain text and toolbar
          self.input = QPlainTextEdit()
          self.input.setFixedHeight(100)
          self.input.setPlaceholderText("Wtite your comments")

          self.toolbar = QToolBar("Comments")
          self.addToolBar(self.toolbar)
          self.toolbar.addWidget(self.input)

          #Buttons
          self.button_max = QPushButton("Max")
          self.button_max.clicked.connect(self.max_button)
          self.button_min = QPushButton("Min")
          self.button_min.clicked.connect(self.min_button)
          self.button_med = QPushButton("Median")
          self.button_med.clicked.connect(self.med_button)
          self.button_avg = QPushButton("Average")
          self.button_avg.clicked.connect(self.avg_button)
          self.button_varianz = QPushButton("Varianz")
          self.button_varianz.clicked.connect(self.varianz_button)
          self.button_save = QPushButton("Save")
          self.button_save.clicked.connect(self.save_data)
          self.button_reset = QPushButton("reset")
          self.button_reset.clicked.connect(self.reset_data)
          self.button_browse = QPushButton("&Browse Files")
          self.button_browse.clicked.connect(self.browse_button_clicked)
          self.button_plot = QPushButton("make a plot")
          self.button_plot.clicked.connect(self.plot_button_clicked)
          self.button_tabel = QPushButton("view a table")
          self.button_tabel.clicked.connect(self.table_button_clicked)


        #Combo-Boxes
          self.csv_datei=QComboBox()
          self.csv_datei.addItems(["none","Column1","Column2","Column3","Column4"])
          self.csv_datei.currentTextChanged.connect(self.data_picker)

        #Menu and action
          action1 = QAction("All operations",self)
          action1.setToolTip('Get Maximum,Minimum,Medien,Average,Varianaz in this order with one click')
          action1.setStatusTip("Operations will be saved as a list of strings")
          action1.triggered.connect(self.max_button)
          action1.triggered.connect(self.min_button)
          action1.triggered.connect(self.med_button)
          action1.triggered.connect(self.avg_button)
          action1.triggered.connect(self.varianz_button)

          action2 = QAction("reset",self)
          action2.setToolTip('Reset the file to nothing')
          action2.triggered.connect(self.reset_data)

          action3 = QAction("Save",self)
          action3.setToolTip('Save to the File')
          action3.triggered.connect(self.save_data)

          menu = self.menuBar()
          file_menue = menu.addMenu("&Operations")
          file_menue.addAction(action1)
          file_menue.addAction(action2)
          file_menue.addAction(action3)

          file_menue.addSeparator()
          action1.setShortcut("Ctrl+o")
          action3.setShortcut("Ctrl+s")
          action2.setShortcut("Ctrl+r")
      #MVCTable
      #the Layout
          layout = QGridLayout()
          layout.addWidget(self.label_datei,1,1)
          layout.addWidget(self.csv_datei,2,1)
          layout.addWidget(self.button_browse,2,2)
          layout.addWidget(self.button_max,3,1)
          layout.addWidget(self.button_min,3,2)
          layout.addWidget(self.button_med,3,3)
          layout.addWidget(self.button_avg,3,4)
          layout.addWidget(self.button_varianz,3,5)
          layout.addWidget(self.button_save,4,1)
          layout.addWidget(self.button_reset,4,2)
          layout.addWidget(self.button_plot,4,3)
          layout.addWidget(self.button_tabel,4,4)


          self.container = QWidget()
          self.container.setLayout(layout)

          self.setCentralWidget(self.container)

      #slots and Methods:
      def max_button(self,checked):

          if self.csv_datei.currentText() == "Column1" :
              try:
                  self.max_col1 = max(Variables.column1)
                  print("The Maximum of Column1 is:", self.max_col1)
                  Variables.saved1.append(self.max_col1)

              except (ValueError,TypeError):
                  self.button_clicked()
              print("-"*20)
              return

          elif self.csv_datei.currentText() == "Column2":
             try:
                self.max_col2 = max(Variables.column2)
                print("The Maximum of Column2 is:", self.max_col2)
                Variables.saved2.append(self.max_col2)

             except (ValueError,TypeError):
                 self.button_clicked()
             print("-" * 20)
             return

          elif self.csv_datei.currentText() == "Column3":
             try:
                self.max_col3 = max(Variables.column3)
                print("The Maximum of Column3 is:", self.max_col3)
                Variables.saved3.append(self.max_col3)

             except (ValueError,TypeError):
                 self.button_clicked()
             print("-" * 20)
             return

          elif self.csv_datei.currentText() == "Column4":
             try:
                self.max_col4 = max(Variables.column4)
                print("The Maximum of Column2 is:", self.max_col4)
                Variables.saved4.append(self.max_col4)

             except (ValueError,TypeError):
                 self.button_clicked()
             print("-" * 20)
             return

          else:
              print("No Max")
              print("-" * 20)
              self.button_clicked()


      def min_button(self, checked):
          if self.csv_datei.currentText() == "Column1":
              try:
                 self.min_col1 = min(Variables.column1)
                 print("The Minimum of Column1 is:",self.min_col1 )
                 Variables.saved1.append(self.min_col1)

              except (ValueError,TypeError):
                  self.button_clicked()
              print("-" * 20)
              return

          elif self.csv_datei.currentText() == "Column2":
              try:
                 self.min_col2 = min(Variables.column2)
                 print("The Minimum of Column2 is:",self.min_col2 )
                 Variables.saved2.append(self.min_col2)

              except (ValueError,TypeError):
                 self.button_clicked()
              print("-" * 20)
              return

          elif self.csv_datei.currentText() == "Column3":
               try:
                  self.min_col3 = min(Variables.column3)
                  print("The Minimum of Column3 is:", self.min_col3)
                  Variables.saved3.append(self.min_col3)

               except (ValueError,TypeError):
                   self.button_clicked()
               print("-" * 20)
               return

          elif self.csv_datei.currentText() == "Column4":
               try:
                  self.min_col4 = min(Variables.column4)
                  print("The Minimum of Column4 is:", self.min_col4)
                  Variables.saved4.append(self.min_col4)

               except (ValueError,TypeError):
                   self.button_clicked()
               print("-" * 20)
               return

          else:
              print("No Minimum")
              print("-" * 20)
              self.button_clicked()


      def med_button(self, checked):
          if self.csv_datei.currentText() == "Column1":
              try:
                 self.med_col1 = sta.median(Variables.column1)
                 print("The Median of Column1 is:",self.med_col1)
                 Variables.saved1.append(self.med_col1)

              except (ValueError,TypeError):
                  self.button_clicked()
              print("-"*20)
              return

          elif self.csv_datei.currentText() == "Column2":
              try:
                 self.med_col2 = sta.median(Variables.column2)
                 print("The Median of Column2 is:", self.med_col2)
                 Variables.saved2.append(self.med_col2)

              except (ValueError,TypeError):
                  self.button_clicked()
              print("-" * 20)
              return

          elif self.csv_datei.currentText() == "Column3":
              try:
                 self.med_col3 = sta.median(Variables.column3)
                 print("The Median of Column3 is:", self.med_col3)
                 Variables.saved3.append(self.med_col3)

              except (ValueError,TypeError):
                  self.button_clicked()
              print("-" * 20)
              return

          elif self.csv_datei.currentText() == "Column4":
              try:
                 self.med_col4 = sta.median(Variables.column4)
                 print("The Median of Column4 is:", self.med_col4)
                 Variables.saved4.append(self.med_col4)

              except (ValueError,TypeError):
                  self.button_clicked()
              print("-" * 20)
              return
          else:
              print("No Median")
              print("-" * 20)
              self.button_clicked()

      def avg_button(self, checked):
          if self.csv_datei.currentText() == "Column1":
              try:
                 self.avg_col1 =  sum(Variables.column1)/len(Variables.column1)
                 print("The Avg. of Column1 is:",self.avg_col1)
                 Variables.saved1.append(self.avg_col1)

              except (ValueError,TypeError):
                  self.button_clicked()
              print("-" * 20)
              return
          elif self.csv_datei.currentText() == "Column2":
              try:
                 self.avg_col2 =  sum(Variables.column2)/len(Variables.column2)
                 print("The Avg. of Column2 is:", self.avg_col2)
                 Variables.saved2.append(self.avg_col2)

              except (ValueError,TypeError):
                  self.button_clicked()
              print("-" * 20)
              return
          elif self.csv_datei.currentText() == "Column3":
              try:
                 self.avg_col3 = sum(Variables.column3) / len(Variables.column3)
                 print("The Avg. of Column3 is:", self.avg_col3)
                 Variables.saved3.append(self.avg_col3)

              except (ValueError,TypeError):
                  self.button_clicked()
              print("-" * 20)
              return

          elif self.csv_datei.currentText() == "Column4":
              try:
                 self.avg_col4 = sum(Variables.column4) / len(Variables.column4)
                 print("The Avg. of Column4 is:", self.avg_col4)
                 Variables.saved4.append(self.avg_col4)

              except (ValueError,TypeError):
                  self.button_clicked()
              print("-" * 20)
              return
          else:
              print("No Average")
              print("-" * 20)
              self.button_clicked()

      def varianz_button(self, checked):
          if self.csv_datei.currentText() == "Column1":
              try:
                 self.varianz_col1 = sta.variance(Variables.column1)
                 print("The Varianz of Column1 is:", self.varianz_col1)
                 Variables.saved1.append(self.varianz_col1)
              except (ValueError,TypeError):
                  self.button_clicked()
              return
              print("-"*20)

          elif self.csv_datei.currentText() == "Column2":
              try:
                 self.varianz_col2 = sta.variance(Variables.column2)
                 print("The Varianz of Column2 is:", self.varianz_col2)
                 Variables.saved2.append(self.varianz_col2)

              except (ValueError,TypeError):
                  self.button_clicked()
              print("-" * 20)
              return

          elif self.csv_datei.currentText() == "Column3":
              try:
                 self.varianz_col3 = sta.variance(Variables.column3)
                 print("The Varianz of Column3 is:", self.varianz_col3)
                 Variables.saved3.append(self.varianz_col3)

              except (ValueError,TypeError):
                  self.button_clicked()
              print("-" * 20)
              return

          elif self.csv_datei.currentText() == "Column4":
              try:
                 self.varianz_col4 = sta.variance(Variables.column4)
                 print("The Varianz of Column4 is:", self.varianz_col4)
                 Variables.saved4.append(self.varianz_col4)

              except (ValueError,TypeError):
                  self.button_clicked()
              print("-" * 20)
              return
          else:
              print("No Varianz")
              print("-" * 20)
              self.button_clicked()

      def browse_button_clicked(self,checked):
          fname = QFileDialog.getOpenFileName(self,"Open CSV files"," ","CSV Files (*.csv)")
          self.opened = open(str(fname[0]))

          print(f"opening {self.opened.name}")
          csv_reader = csv.DictReader(self.opened,delimiter = ';')
          line_count = 0
          for row in csv_reader:
              print(row)
              self.column_maker = [x.strip().replace(',','.') for x in row.values()]
              Variables.list_of_lists.append(self.column_maker)
              try:
                  Variables.column1.append(float(self.column_maker[0]))
              except ValueError as ve:
                    Variables.column1.append(self.column_maker[0])
              try:
                  Variables.column2.append(float(self.column_maker[1]))
              except ValueError as ve:
                  Variables.column2.append(self.column_maker[1])
              try:
                  Variables.column3.append(float(self.column_maker[2]))
              except ValueError as ve:
                  Variables.column3.append(self.column_maker[2])
              try:
                  Variables.column4.append(float(self.column_maker[3]))
              except ValueError as ve:
                  Variables.column4.append(self.column_maker[3])

              line_count += 1
          print(f'Processed {line_count} lines.')
          #print(Variables.list_of_lists)
          print("-"*30)

      def data_picker(self,txt):
          if txt =="Column1" :
             print("opening",txt)
             print(Variables.column1)
             print(20*"-")

          elif txt == "Column2":
               print("opening",txt)
               print(Variables.column2)
               print("-"*20)

          elif txt == "Column3":
               print("opening", txt)
               print(Variables.column3)
               print("-"*20)

          elif txt == "Column4":
               print("opening", txt)
               print(Variables.column4)
               print("-"*20)

          else:
              print("None")


      def save_data(self,checked):
          dlg = QMessageBox(self)
          dlg.setText("The order of the data in each column depends on which operation the user started with"
                      " and the data of each click are redunant.")
          dlg.setStandardButtons(QMessageBox.Ok)
          response = dlg.exec_()
          self.name = QFileDialog.getSaveFileName(self,"Save File","",('*.txt'))
          self.file = open(str(self.name[0]),'w')
          self.file.write(f'\nColumn1: {Variables.saved1}')
          self.file.write(f'\nColumn2: {Variables.saved2}')
          self.file.write(f'\nColumn3: {Variables.saved3}')
          self.file.write(f'\nColumn4: {Variables.saved4}')
          self.file.write(f'\n\n\n{str(self.input.toPlainText())}')
          self.file.close()

      def reset_data(self,checked):
          with open(str(self.name[0]),'w') as file:
               file.write(" ")
               self.csv_datei.setCurrentIndex(0)
               self.input.setPlainText(" ")
               Variables.column1 = []
               Variables.column2 = []
               Variables.column3 = []
               Variables.column4 = []
               Variables.column4 = []

               Variables.saved1 = []
               Variables.saved2 = []

          dlg = QMessageBox(self)
          dlg.setText("Reseted")
          dlg.setStandardButtons(QMessageBox.Ok)
          response = dlg.exec_()


      def button_clicked(self):
          dlg = QMessageBox(self)
          dlg.setWindowTitle("Unacceptable data were choosen!")
          dlg.setText("Either you picked a colmun which contain a type that can't get caluclated or you didn't open a file before you caluclate")
          dlg.setStandardButtons(QMessageBox.Ok)
          dlg.setIcon(QMessageBox.Warning)
          response = dlg.exec_()
          if response == QMessageBox.Ok:
             self.csv_datei.setCurrentIndex(0)

      def plot_button_clicked(self,checked):
          self.plotted = PlotsubWindow()
          #print(self.plotted)
          #self.plotted.exec_()
          self.plotted.show()

      def table_button_clicked(self,checked):
          self.table_view = TableViewWindow()
          self.table_view.show()


QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

app = QApplication([])
window = MainWindow()
window.show()

app.exec_()
