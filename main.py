# system modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets

import sys
import os
import datetime
import pandas as pd
import gui
import ctypes

# self-used module
import thread
import timemachine_request

class Main(QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        global apikey, foundCities

        # Read from APIKEY from License.csv file
        try:
            licenseKey = pd.read_csv('./license.csv')

            if list(licenseKey)[0] == "APIKEY":
                apikey = licenseKey['APIKEY'][0]
        except:
            ctypes.windll.user32.MessageBoxW(0, "The License.csv file cannot be found or the format is incorrect", "Error!", 0)
            sys.exit()

        # Read from City_List.csv file
        self.LoadCity()

        self.comboBox_City.currentTextChanged.connect(lambda comboBox, it=self.lineEdit_Latitude: it.setText(str(self.foundCities['Latitude'][self.comboBox_City.currentIndex()])))
        self.comboBox_City.currentTextChanged.connect(lambda comboBox, it=self.lineEdit_Longitude: it.setText(str(self.foundCities['Longitude'][self.comboBox_City.currentIndex()])))

        # Update today's weather
        self.UpdateTodayWeather()
        self.pushButton_Update.clicked.connect(lambda: self.UpdateTodayWeather())

        # Save forecast file
        self.pushButton_SaveForecast.clicked.connect(lambda: self.SaveForecast())

        # Save history file
        self.pushButton_SaveHistory.clicked.connect(lambda: self.SaveHistory())

        # Start thread
        self.StartThread()

        # Close application
        self.closeEvent = self.closeEvent

        # Clear log
        self.pushButton_Clear.clicked.connect(lambda: self.listWidget.clear())

        # Export log
        self.pushButton_Export.clicked.connect(lambda: self.ExportOperationLOG())

        self.show()

    def LoadCity(self): # Read from City_List.csv file
        try:
            self.foundCities = pd.read_csv('./City_List.csv')

            if list(self.foundCities)[0] == "City" and list(self.foundCities)[1] == "Latitude" and list(self.foundCities)[2] == "Longitude":
                self.comboBox_City.clear()

                # Load all the cities into comboBox_City selection
                for num in range(len(self.foundCities)):
                    self.comboBox_City.addItem(self.foundCities['City'][num])

                # Assign Latitude and Longitude values
                self.lineEdit_Latitude.setText(str(self.foundCities['Latitude'][0]))
                self.lineEdit_Longitude.setText(str(self.foundCities['Longitude'][0]))

                timeMSG = "{0}".format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
                logMSG = "City list renewed successfully! -- " + timeMSG
                self.listWidget.addItem(logMSG)
            else:
                ctypes.windll.user32.MessageBoxW(0, "The columns' values cannot be empty in the City_List.csv", "Error!", 0)
                timeMSG = "{0}".format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
                logMSG = "City list renewed failed! -- " + timeMSG
                self.listWidget.addItem(logMSG)
                #sys.exit()
        except:
            ctypes.windll.user32.MessageBoxW(0, "The City_List.csv file cannot be found", "Error!", 0)
            timeMSG = "{0}".format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            logMSG = "City list renewed failed! -- " + timeMSG
            self.listWidget.addItem(logMSG)
            #sys.exit()

    def UpdateTodayWeather(self):
        isGet = timemachine_request.TodayWeather(apikey,
                                      self.lineEdit_Latitude.text(),
                                      self.lineEdit_Longitude.text())

        if isGet == True:
            nowArray = timemachine_request.todayArray

            # Load all values into today's table
            for num in range(len(nowArray)):
                self.tableWidget.setItem(0, num, QtWidgets.QTableWidgetItem(str(nowArray[num][0][1])))
                self.tableWidget.setItem(1, num, QtWidgets.QTableWidgetItem(str(nowArray[num][1][1])))
                self.tableWidget.setItem(2, num, QtWidgets.QTableWidgetItem(str(nowArray[num][2][1])))
            self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

            timeMSG = "{0}".format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            logMSG = "Today's weather updated successfully! -- " + timeMSG
            self.listWidget.addItem(logMSG)
        else:
            ctypes.windll.user32.MessageBoxW(0, "No Hourly data in Today's weather", "Warning!", 0)
            timeMSG = "{0}".format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            logMSG = "Failed to update Today's weather! -- " + timeMSG
            self.listWidget.addItem(logMSG)

    def SaveForecast(self):
        isGet = timemachine_request.TomorrowWeather(apikey,
                                                    self.lineEdit_Latitude.text(),
                                                    self.lineEdit_Longitude.text(),
                                                    self.comboBox_City.currentText())

        if isGet == False:
            timeMSG = "{0}".format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            logMSG = "Failed to save Tomorrow's forecast report! -- " + timeMSG
            self.listWidget.addItem(logMSG)
        elif isGet == True:
            timeMSG = "{0}".format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            logMSG = "Tomorrow's report saved successfully! -- " + timeMSG
            self.listWidget.addItem(logMSG)

    def SaveHistory(self):
        isGet = timemachine_request.YesterdayWeather(apikey,
                                                    self.lineEdit_Latitude.text(),
                                                    self.lineEdit_Longitude.text(),
                                                    self.comboBox_City.currentText())
        if isGet == False:
            timeMSG = "{0}".format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            logMSG = "Failed to save Yesterday's record! -- " + timeMSG
            self.listWidget.addItem(logMSG)
        elif isGet == True:
            timeMSG = "{0}".format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            logMSG = "Yesterday's record saved successfully! -- " + timeMSG
            self.listWidget.addItem(logMSG)

    def StartThread(self):
        thread.isStopThread = False
        self.trdProcess = thread.StartThreadFunc(self)
        self.trdProcess.start()

    def ExportOperationLOG(self):
        outdir_LOG = './OperationLog'
        if not os.path.exists(outdir_LOG):
            os.makedirs(outdir_LOG, exist_ok=True)

        nowTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        filename = outdir_LOG + '/LOG_' + nowTime + '.txt'

        with open(filename, 'a', encoding='utf8') as s:
            for i in range(self.listWidget.model().rowCount()):
                text = self.listWidget.model().data(self.listWidget.model().index(i))
                text = text + "\n"
                s.write(text)

        timeMSG = "{0}".format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        logMSG = "Export operation log successfully! -- " + timeMSG
        self.listWidget.addItem(logMSG)

    def closeEvent(self, event):
        print("Close Application!")
        #sys.exit(0)
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = Main()
    MainWindow.show()
    sys.exit(app.exec_())
