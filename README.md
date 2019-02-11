# Files
1. License.csv
  - Store the API key for this application
  - Please use your own API key to run this application

2. City_List.csv
  - Store Latitude and Longitude values of different cities
  
3. gui.py
  - This file is generated by gui.ui which is made by QT Designer
  
4. thread.py
  - Continuously update the current time every second
  - Continuously update Today's weather status every 30 mins
  - Continuously update Tomorrow's forecast report and save it every 1 hour
  - Continuously save Yesterday's weather record everyday at 1AM

5. timemachine_request.py
  - TimeMachine Request module is used
  - TodayWeather function is to update Today's weather
  - TomorrowWeather function is to update Tomorrow's forecast and save it to a CSV file
  - YesterdayWeather function is to update Yesterday's record and save it to a CSV file
  - All CSV files will be saved corresponding to the selected city

# Folders
1. Files
  - Store all CSV files in corresponding to selected city

2. OperationLog
  - Store all operation log txt files
  
# NOTE
The main mission is to compare daily weather with forecast and reality record, so when saving the Yesterday record, it is necessary that the date of yesterady's CSV file has already existed. That is, the existing CSV file is created by TomorrowWeather function first, and then the YesterdayWeather function can save the history record into the existing file.
