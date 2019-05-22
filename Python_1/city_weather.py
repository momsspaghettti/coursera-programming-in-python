import requests
from dateutil.parser import parse
import pprint


class YahooWeatherForecast:

    def __init__(self):
        self._city_cache = {}
        

    def get(self, city):
        if city in self._city_cache:
            return self._city_cache

        url = f"https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22{city}%22)%20and%20u%3D%22c%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
        print("sending HTTP request ...")
        data = requests.get(url).json()
        print("HTTP request completed")
        forecast_data = data["query"]["results"]["channel"]["item"]["forecast"]
        forecast = []
        for day_data in forecast_data:
            forecast.append({
                "date": parse(day_data["date"]),
                "high": day_data["high"],
                "low": day_data["low"]
            })
        self._city_cache[city] = forecast
        return forecast

class Forecast:

    def __init__(self, city):
        self.city = city
        self.data = YahooWeatherForecast() or []

    def get_data(self):
        result = self.data.get(self.city)
        return result


class CityInfo:

    def __init__(self, city):
        self.city = city

    def weather_forecast(self):
        result = Forecast(self.city)
        return result.get_data()


def _main_():
    print("Type Your city")
    city_name = input()
    city_info = CityInfo(city_name)
    forecast = city_info.weather_forecast()
    pprint.pprint(forecast)


if __name__ == "__main__":
    _main_()

