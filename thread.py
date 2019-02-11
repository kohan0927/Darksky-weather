# system modules
from PyQt5.QtCore import pyqtSignal, QThread
import datetime
import threading

sleepBreak = threading.Event()

class StartThreadFunc(QThread):
    countChanged = pyqtSignal(int)

    def __init__(self, uiObj):
        QThread.__init__(self)
        self.mainUI = uiObj

    def run(self):
        global isStopThread, sleepBreak

        while isStopThread == False:
            # Assign the current date and time values
            nowYear = datetime.datetime.now().year
            nowMonth = datetime.datetime.now().month
            nowDay = datetime.datetime.now().day
            nowHour = datetime.datetime.now().hour
            nowMinute = datetime.datetime.now().minute
            nowSecond = datetime.datetime.now().second

            self.mainUI.label_Year.setText(str(nowYear))
            self.mainUI.label_Month.setText(str(nowMonth))
            self.mainUI.label_Day.setText(str(nowDay))
            self.mainUI.label_Hour.setText(str(nowHour))
            self.mainUI.label_Minute.setText(str(nowMinute))
            self.mainUI.label_Second.setText(str(nowSecond))

            # Automatically update today's weather every 30 mins
            if nowMinute%30 == 0 and nowSecond == 0:
                self.mainUI.UpdateTodayWeather()

            # Automatically save tomorrow's forecast every 1 hour
            if nowMinute%60 == 0 and nowSecond == 0:
                self.mainUI.SaveForecast()

            # Automatically save yesterday's record at 1AM everyday
            if nowHour == 1 and nowMinute == 0 and nowSecond == 0:
                self.mainUI.SaveHistory()

            sleepBreak.wait(timeout=1)
            self.countChanged.emit(True)