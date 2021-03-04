import sys, requests, time, json
from datetime import datetime
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from PyQt5.QtCore import QCoreApplication, QUrl
from main_ui import Ui_Form



class MainWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		self.customSettings()
		self.getWeatherData()
		self.setButtons()
		print("Finishing up...")
		self.show()		
	def customSettings(self):
		print('Setting window configurations...')
		self.setWindowTitle("My Weather App")
	def getWeatherData(self):
		print("Getting weather from database...")
		get_data = requests.get("https://weatherapp-6c195-default-rtdb.firebaseio.com/weather_data.json")
		if (get_data.status_code != 200):
			print("Couldn't get weather data from the database...")
			time.sleep(5)
			raise SystemExit()
		self.weather_data = json.loads(get_data.text)
		global a 
		a = self.weather_data
	def setButtons(self):
		print("Setting up the buttons...")
		self.ui.current_weather_label.clicked.connect(buttonFunctions.current_weather_button)
		self.ui.first_button.clicked.connect(buttonFunctions.firstButton)
		self.ui.second_button.clicked.connect(buttonFunctions.secondButton)
		self.ui.third_button.clicked.connect(buttonFunctions.thirdButton)
		self.ui.fourth_button.clicked.connect(buttonFunctions.fourthButton)
		self.ui.fifth_button.clicked.connect(buttonFunctions.fifthButton)
	def setupMenu(self):
		print("Setting up values...")
		buttonFunctions.current_weather_button()
		QtCore.QTimer.singleShot(0, lambda: self.ui.first_button.setText(self.weather_data[4]['temp']))
		QtCore.QTimer.singleShot(0, lambda: self.ui.second_button.setText(self.weather_data[5]['temp']))
		QtCore.QTimer.singleShot(0, lambda: self.ui.third_button.setText(self.weather_data[6]['temp']))
		QtCore.QTimer.singleShot(0, lambda: self.ui.fourth_button.setText(self.weather_data[7]['temp']))
		QtCore.QTimer.singleShot(0, lambda: self.ui.fifth_button.setText(self.weather_data[8]['temp']))



class buttonFunctions:
	def change_data_global(current, time, quality, wind, gusts):
		QtCore.QTimer.singleShot(0, lambda: window.ui.title_weather.setText(current))
		QtCore.QTimer.singleShot(0, lambda: window.ui.time_label.setText(time))
		QtCore.QTimer.singleShot(0, lambda: window.ui.quality_label.setText(quality))
		QtCore.QTimer.singleShot(0, lambda: window.ui.wind_label.setText(wind))
		QtCore.QTimer.singleShot(0, lambda: window.ui.gusts_label.setText(gusts))
	def current_weather_button():
		print("Changing values to current weather...")
		buttonFunctions.change_data_global(a[0], datetime.today().strftime("%#H %p"), a[1], a[2], a[3])
	def firstButton():
		print("Changing values to first button...")
		buttonFunctions.change_data_global(a[4]['temp'], a[4]['time'], a[4]['air_quality'], a[4]['wind'], a[4]['wind_gusts'])
	def secondButton():
		print("Changing values to second button...")
		buttonFunctions.change_data_global(a[5]['temp'], a[5]['time'], a[5]['air_quality'], a[5]['wind'], a[5]['wind_gusts'])
	def thirdButton():
		print("Changing values to third button...")
		buttonFunctions.change_data_global(a[6]['temp'], a[6]['time'], a[6]['air_quality'], a[6]['wind'], a[6]['wind_gusts'])
	def fourthButton():
		print("Changing values to fourth button...")
		buttonFunctions.change_data_global(a[7]['temp'], a[7]['time'], a[7]['air_quality'], a[7]['wind'], a[7]['wind_gusts'])
	def fifthButton():
		print("Changing values to fifth button...")
		buttonFunctions.change_data_global(a[8]['temp'], a[8]['time'], a[8]['air_quality'], a[8]['wind'], a[8]['wind_gusts'])




if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = MainWindow()
	window.setupMenu()

	sys.exit(app.exec_())