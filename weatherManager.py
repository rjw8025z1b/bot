import requests
import datetime
import settings
import os
from logger import logger


class WeatherManager:

    API_LINK_FORECAST = 'http://api.openweathermap.org/data/2.5/weather'

    def getEmoji(self, weather_id):
        # Openweathermap Weather codes and corressponding emojis
        thunderstorm = u'\U0001F4A8'  # Code: 200's, 900, 901, 902, 905
        drizzle = u'\U0001F4A7'  # Code: 300's
        rain = u'\U00002614'  # Code: 500's
        snowflake = u'\U00002744'  # Code: 600's snowflake
        snowman = u'\U000026C4'  # Code: 600's snowman, 903, 906
        atmosphere = u'\U0001F301'  # Code: 700's foogy
        clear_sky = u'\U00002600'  # Code: 800 clear sky
        few_clouds = u'\U000026C5'  # Code: 801 sun behind clouds
        clouds = u'\U00002601'  # Code: 802-803-804 clouds general
        hot = u'\U0001F525'  # Code: 904
        default_emoji = u'\U0001F300'  # default emojis

        if weather_id:
            if str(weather_id)[0] == '2' or weather_id in (900, 901, 902, 905):
                return thunderstorm
            elif str(weather_id)[0] == '3':
                return drizzle
            elif str(weather_id)[0] == '5':
                return rain
            elif str(weather_id)[0] == '6' or weather_id in (903, 906):
                return snowflake + ' ' + snowman
            elif str(weather_id)[0] == '7':
                return atmosphere
            elif weather_id == 800:
                return clear_sky
            elif weather_id == 801:
                return few_clouds
            elif weather_id == 802 or weather_id == 803 or weather_id == 803:
                return clouds
            elif weather_id == 904:
                return hot
            else:
                return default_emoji

        else:
            return default_emoji


    def update_forecast(self):
        r = requests.get(self.API_LINK_FORECAST, params=f'q=Warsaw&appid={settings.OPEN_WEATHER_MAP_TOKEN}&units=metric')
        weather_forecast = r.json()
        condition = self.getEmoji(weather_forecast['weather'][0]['id'])
        symbol_degree = u"\u00B0"
        if weather_forecast['cod'] == 200:
            result = f"Today we are expecting {condition} with\nmax temperature of {weather_forecast['main']['temp_max']}{symbol_degree} and\nmin temperature of {weather_forecast['main']['temp_min']}{symbol_degree}\nwith humidity {weather_forecast['main']['humidity']}%\nSunrise was at {datetime.datetime.fromtimestamp(weather_forecast['sys']['sunrise'])} and\nSunset in {datetime.datetime.fromtimestamp(weather_forecast['sys']['sunset'])}"
            with open(os.path.join(settings.BASE_DIR, 'forecast.txt'), 'w+', encoding="utf-8") as f_file:
                f_file.write(result)
        else:
            logger.info(f'Weather was returned with status code : {weather_forecast["cod"]}')

    def check_if_forecast_need_update(self):
        file_name = os.path.join(settings.BASE_DIR, 'forecast.txt')
        if not os.path.isfile(file_name):
            return True

        forecast_update_date = os.path.getmtime(file_name)
        mod_time = datetime.date.fromtimestamp(forecast_update_date)

        return datetime.date.today() != mod_time

    def process_weather(self):
        if self.check_if_forecast_need_update():
            self.update_forecast()
            logger.info('Weather was updated')
