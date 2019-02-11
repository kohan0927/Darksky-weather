# system modules
from forecastiopy import ForecastIO, FIODaily, FIOHourly
import os
import re
import sys
import datetime
import ctypes
import pandas as pd

todayArray = []
tomorrowList = []
yesterdayList = []

def CallFIO(apikey, nowLatitude, nowLongitude, startTime):
    try:
        fio = ForecastIO.ForecastIO(apikey,
                                    units=ForecastIO.ForecastIO.UNITS_SI,
                                    lang=ForecastIO.ForecastIO.LANG_ENGLISH,
                                    latitude=nowLatitude, longitude=nowLongitude,
                                    exclude='minutely, alerts',
                                    time=startTime)
        return fio
    except:
        ctypes.windll.user32.MessageBoxW(0, "The APIKEY is incorrect", "Error!", 0)
        sys.exit()

def TodayWeather(apikey, nowLatitude, nowLongitude):
    # Start from today 00:00
    global todayArray
    todayArray = []

    startTime = datetime.datetime(datetime.datetime.now().year,
                                  datetime.datetime.now().month,
                                  datetime.datetime.now().day, 0).isoformat()

    fio = CallFIO(apikey, nowLatitude, nowLongitude, startTime)

    if fio.has_hourly() is True:
        hourly = FIOHourly.FIOHourly(fio)
        hourList = hourly.get()['data']

        for num in range(len(hourList)):
            for idx, item in enumerate(hourList[num].items()):
                # Change timestamp to a readable time format
                if bool(re.findall('time', item[0], re.IGNORECASE)) == True:
                    hourList[num][item[0]] = datetime.datetime.fromtimestamp(item[1]).strftime('%Y-%m-%d %H:%M:%S')

            newList = list(filter(lambda x: x[0] == 'icon' or x[0] == 'temperature' or x[0] == 'humidity', hourList[num].items()))
            todayArray.append(newList)

        return True
    else:
        return False

def TomorrowWeather(apikey, nowLatitude, nowLongitude, selCity):
    global tomorrowList
    tomorrowList = []

    # Start from tomorrow 00:00
    selDate = datetime.datetime.now() + datetime.timedelta(days=1)
    startTime = datetime.datetime(selDate.year, selDate.month, selDate.day, 0).isoformat()

    fio = CallFIO(apikey, nowLatitude, nowLongitude, startTime)
    if fio.has_daily() is True:
        daily = FIODaily.FIODaily(fio)
        tomorrowList = daily.get()['data']

        for num in range(len(tomorrowList)):
            for idx, item in enumerate(tomorrowList[num].items()):
                # Change timestamp to a readable time format
                if bool(re.findall('time', item[0], re.IGNORECASE)) == True:
                    tomorrowList[num][item[0]] = datetime.datetime.fromtimestamp(item[1]).strftime('%Y-%m-%d %H:%M:%S')

        index_value = tomorrowList[0].values()

        index_name = tomorrowList[0].keys()
        report = {'': list(index_name),
                'Forecast': list(index_value)
                }
        df = pd.DataFrame(report, columns=['', 'Forecast'])

        outdir_LOG = "./Files/" + selCity + "/"
        if not os.path.exists(outdir_LOG):
            os.makedirs(outdir_LOG, exist_ok=True)

        nowTime = selDate.strftime('%Y%m%d')
        filename = outdir_LOG + nowTime + '.csv'

        if not os.path.exists(filename):
            df.to_csv(filename, index=False, encoding='utf-8-sig')
        else:
            df = pd.read_csv(filename)
            df['Forecast'] = list(index_value)
            df = df.rename(columns={'Unnamed: 0': ''})
            df.to_csv(filename, index=False, encoding='utf-8-sig')
        return True
    else:
        return False

def YesterdayWeather(apikey, nowLatitude, nowLongitude, selCity):
    global yesterdayList
    yesterdayList = []

    # Start from yesterday 00:00
    selDate = datetime.datetime.now() - datetime.timedelta(days=1)
    startTime = datetime.datetime(selDate.year, selDate.month, selDate.day, 0).isoformat()

    fio = CallFIO(apikey, nowLatitude, nowLongitude, startTime)

    if fio.has_daily() is True:
        daily = FIODaily.FIODaily(fio)
        yesterdayList = daily.get()['data']

        for num in range(len(yesterdayList)):
            for idx, item in enumerate(yesterdayList[num].items()):
                # Change timestamp to a readable time format
                if bool(re.findall('time', item[0], re.IGNORECASE)) == True:
                    yesterdayList[num][item[0]] = datetime.datetime.fromtimestamp(item[1]).strftime('%Y-%m-%d %H:%M:%S')


        index_value = yesterdayList[0].values()

        outdir_LOG = "./Files/" + selCity + "/"
        if not os.path.exists(outdir_LOG):
            os.makedirs(outdir_LOG, exist_ok=True)


        nowTime = selDate.strftime('%Y%m%d')
        filename = outdir_LOG + nowTime + '.csv'

        if not os.path.exists(filename):
            ctypes.windll.user32.MessageBoxW(0, "No past forecast record for yesterday", "Warning!", 0)
            return False
        else:
            df = pd.read_csv(filename)
            df['Reality'] = list(index_value)
            df = df.rename(columns={'Unnamed: 0': ''})
            df.to_csv(filename, index=False, encoding='utf-8-sig')
        return True
    else:
        return False