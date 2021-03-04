import requests
from bs4 import BeautifulSoup
import time
import json


class Main:
	def __init__(self):
		self.database_url = "https://weatherapp-6c195-default-rtdb.firebaseio.com/weather_data.json"

		self.url_now = "https://www.accuweather.com/en/us/youngstown/44503/weather-forecast/330121"
		self.url_hourly = "https://www.accuweather.com/en/us/youngstown/44503/hourly-weather-forecast/330121"
		# This is needed to avoid being detected by the site as a bot
		self.headers =  {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
		# start scraping here
		self.scrape_site()
		# upload to a database
		self.upload_to_database()
	def scrape_site(self):
		print("Scraping the site...")
		# Scrape both the hourly and now temps
		html_now = requests.get(self.url_now, headers = self.headers)
		html_hourly = requests.get(self.url_hourly, headers = self.headers)

		# Put em in beautiful soup
		soup_now = BeautifulSoup(html_now.content, 'html.parser')
		soup_hourly = BeautifulSoup(html_hourly.content, 'html.parser')

		# Find the current temp & other stuff
		weather_details_now = soup_now.find_all("div", class_="spaced-content detail")

		# First Hour
		weather_details_hourly_first = soup_hourly.find("div", id = "hourlyCard0")
		# Second Hour
		weather_details_hourly_second = soup_hourly.find("div", id = "hourlyCard1")
		# Third Hour
		weather_details_hourly_third = soup_hourly.find("div", id = "hourlyCard2")
		# Fourth Hour
		weather_details_hourly_fourth = soup_hourly.find("div", id = "hourlyCard3")
		# Fifth Hour
		weather_details_hourly_fifth = soup_hourly.find("div", id = "hourlyCard4")

		temp_vars = [weather_details_hourly_first,
					weather_details_hourly_second,
					weather_details_hourly_third,
					weather_details_hourly_fourth,
					weather_details_hourly_fifth]
		self.weather_data = []
		for i in weather_details_now:
			"""
			First: Current Temp
			Second: Air Quality
			Third: Wind
			Fourth: Wind Gusts
			"""
			self.weather_data.append(i.text.split("\n")[2])
		# Store the next 5 hours for temp
		self.hourly_data = []
		for weather in temp_vars:
			hourly_format = {"time":"", "temp":"", "air_quality":"", "wind":"", "wind_guhromets":""}
			hourly_format["time"] = (weather.find('span').text)
			hourly_format["temp"] = (weather.find(class_="temp").text.replace("	","").strip("\n"))
			hourly_format["wind"] = (weather.find_all('p')[3].text[4:])
			hourly_format["air_quality"] = (weather.find_all("p")[1].text.replace("Air Quality",""))
			hourly_format["wind_gusts"] = (weather.find_all("p")[4].text.replace("Wind Gusts", ""))
			self.hourly_data.append(hourly_format)
	def upload_to_database(self):
		print("Uploading to database...")
		upload = requests.put(self.database_url, json = (self.weather_data+self.hourly_data))
		if (upload.status_code != 200):
			print("Failed to upload.")
			return
		print("Uploaded successfully.")
		print("Writing locally...")
		with open("data.json", "w") as f:
			json.dump(self.weather_data+self.hourly_data, f, indent=4)
		print('Written successfully...')


		

while True:
	# Keep updating the database...
	WeatherFunction = Main()
	print("Waiting 1 hour now...")
	time.sleep(3600)


