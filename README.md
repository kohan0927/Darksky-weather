License.csv
1. Store the API key for this application
2. Please use your own API key to run this application

City_List.csv
Store Latitude and Longitude values of different cities

thread.py
1. Continuously update the current time every second
2. Continuously update Today's weather status every 30 mins
3. Continuously update Tomorrow's forecast report and save it every 1 hour
4. Continuously save Yesterday's weather record everyday at 1AM

timemachine_request.py
1. TimeMachine Request module is used.
2. TodayWeather function is to update Today's weather
3. TomorrowWeather function is to update Tomorrow's forecast and save it to a CSV file
4. YesterdayWeather function is to update Yesterday's record and save it to a CSV file
5. All CSV files will be saved corresponding to the selected city
NOTE: The main mission is to compare daily weather with forecast and reality record, so when saving the Yesterday record, it is necessary that the date of yesterady's CSV file has already existed. That is, the existing CSV file is created by TomorrowWeather function first, and then the YesterdayWeather function can save the history record into the existing file.

gui.py
This file is generated by gui.ui which is made by QT Designer
