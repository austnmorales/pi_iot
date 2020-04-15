import epd2in7b  
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import requests 
import json 
import time
#import imagedata 

COLORED = 1 
UNCOLORED = 0 

response = requests.get("https://api.openweathermap.org/data/2.5/weather?zip=14222&appid=[API_KEY]")

temperature = response.json()['main']
sys = response.json()['sys']
sunrise = sys['sunrise']
sunset = sys['sunset']
temp_min = temperature['temp_min']
temp_max = temperature['temp_max']

weather = response.json()['weather']
weather_attributes = []
#this function iterates over the 'weather' array
#from the json response. We're interested only in the
#description key, so that's what this function grabs
#and then appends to the weather_attributes array
def get_weather():
    for d in weather:
        attribute = d['description']
        weather_attributes.append(attribute)
get_weather()


kelvin_temp = response.json()['main']['temp']

def temp_convert(temperature):
    return str(int(((temperature - 273.15) * 9/5 + 32)))

temperature = temp_convert(kelvin_temp)
minimum = temp_convert(temp_min)
maximum = temp_convert(temp_max)

#all the values that we're going to put in our
#message
name = response.json()['name']
weather = weather_attributes[0]
sunrise_time = time.strftime('%H:%M %p', time.localtime(sunrise))
sunset_time = time.strftime('%H:%M %p', time.localtime(sunset))

def main():
    epd = epd2in7b.EPD()
    epd.init()

    #clear the frame buffer
    frame_black = [0] * (epd.width * epd.height / 8)
    frame_red = [0] * (epd.width * epd.height / 8)
    #draw a rectangle
    #epd.draw_rectangle(frame_black, 165, 30, 30, 30, COLORED)
    #draw a string 
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18)
    epd.draw_string_at(frame_black, 20, 20, "Temperature:", font, COLORED)
    epd.draw_string_at(frame_red, 20, 40, temperature+"F", font, COLORED)
    epd.draw_string_at(frame_black, 20, 60, "Weather:", font, COLORED)
    epd.draw_string_at(frame_red, 20, 80, weather, font, COLORED)
    epd.draw_string_at(frame_black, 20, 100, "High:", font, COLORED)
    epd.draw_string_at(frame_red, 20, 120, maximum+"F", font, COLORED)
    epd.draw_string_at(frame_black, 20, 140, "Low", font, COLORED)
    epd.draw_string_at(frame_red, 20, 160, minimum+"F", font, COLORED)

   # bison = epd.get_frame_buffer(Image.open('bison.png'))

    epd.display_frame(frame_black, frame_red)
if __name__ == '__main__':
    main()


