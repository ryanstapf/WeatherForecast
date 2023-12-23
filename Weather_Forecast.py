# import the module
import python_weather

import asyncio
import os

# imported to create an hourly table
from prettytable import PrettyTable

# converts wind heading to compass directions
def direction_getter(degrees):

  if degrees >= 337.5 or degrees < 22.5:
    direction = "N"
  if degrees >= 22.5 and degrees < 67.5:
    direction = "NE"
  if degrees >= 67.5 and degrees < 112.5:
    direction = "E"
  if degrees >= 112.5 and degrees < 157.5:
    direction = "SE"
  if degrees >= 157.5 and degrees < 202.5:
    direction = "S"
  if degrees >= 202.5 and degrees < 247.5:
    direction = "SW"
  if degrees >= 247.5 and degrees < 292.5:
    direction = "W"
  if degrees >= 292.5 and degrees < 337.5:
    direction = "NW"

  return direction


# simple rain or snow converter used for chance of precipitation
def rain_or_snow(temp, timeframe):
  if temp > 32:
    return (timeframe.chances_of_rain, "rain")
  else:
    return (timeframe.chances_of_snow, "snow")


# Input a city and state
async def getweather(city):
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:

    # fetch a weather forecast from the input city
    weather = await client.get(city)
    
    # returns the current conditions
    current_date = weather.current.date
    current_conditions = weather.current.description
    current_temp = weather.current.temperature
    current_feel = weather.current.feels_like

    # print the current conditions
    print("="*100)
    print()
    print(f'{current_date}\n')
    print("Current Conditions:")
    print(f'\n{current_conditions}\n\nTemperature: {current_temp}(F)\nFeels Like: {current_feel}(F)')

    # get the weather forecast for a few days
    for forecast in weather.forecasts:
      moon_phase = forecast.astronomy.moon_phase
      sun_rise = forecast.astronomy.sun_rise
      sun_set = forecast.astronomy.sun_set
      high = forecast.highest_temperature
      low = forecast.lowest_temperature

      print()

      # date
      print("="*100)
      print()
      print("{0}\n".format(forecast.date))

      # daily Data
      print("High: {0} (F)".format(high))
      print("Low: {0} (F)\n".format(low))
      print("Sunrise: {0}   Sunset: {1}   Lunar Phase: {2}\n".format(sun_rise, sun_set, moon_phase))

      # generate a table to tabulate hourly data into
      hourlyTable = PrettyTable(["Time", "Temperature", "Conditions", "Winds", "Feels Like", "Chance of Precipitation", "Humidity", "Pressure", "UV Index"])
      
      # hourly forecasts
      for hourly in forecast.hourly:

        # time
        time = hourly.time

        # actual temperature in (F)
        temp_at_time = hourly.temperature

        # weather conditions
        conditions = hourly.description

        # wind speed and direction
        wind_speed = hourly.wind_speed
        wind_direction = hourly.wind_direction.degrees
        wind_data = "{0} at {1} mph".format(direction_getter(wind_direction), wind_speed)

        # feels like temperature in (F)
        feels_like = f'{hourly.feels_like} (F)'

        # precipitation chance
        precpt_tupple = rain_or_snow(temp_at_time, hourly)
        precpt_chance = "{0}%".format(precpt_tupple[0])
        precpt_type = "{0}".format(precpt_tupple[1])
        precpt_data = f'Chance of {precpt_type}: {precpt_chance}'

        # humidity percentage
        humidity = f'{hourly.humidity}%'

        # pressure in inHg
        pressure = f'{float(hourly.pressure)} inHg'

        # UV Index
        uv_index = hourly.ultraviolet

        # tabulate data
        hourlyTable.add_row([time, f'{temp_at_time} (F)', conditions, wind_data, feels_like, precpt_data, humidity, pressure, uv_index])

      
      print(hourlyTable)
      print()



if __name__ == '__main__':
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  city = input("Enter City, State: ")

  asyncio.run(getweather(city))