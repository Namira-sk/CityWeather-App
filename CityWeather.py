import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from configparser import ConfigParser
import requests
import PIL

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

def get_weather(city):
    result = requests.get(url.format(city,api_key))
    if result:
        json = result.json()
        #(City, Country, temp_celcius, temp_fahrenheit, icon, weather)
        city = json['name']
        country = json['sys']['country']
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin - 273.15
        temp_fahrenheit = (temp_kelvin - 273.15) * 9/5+32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        final = (city,country,temp_celsius,temp_fahrenheit,icon,weather)
        return final

    else:
        return None


def search():
    city = city_text.get()
    weather = get_weather(city)
    if weather:
        location_lbl['text'] = '{},{}'.format(weather[0], weather[1])
        img = ImageTk.PhotoImage(image = PIL.Image.open("weather_icons/{}.png".format(weather[4])))
        image_lbl = Label(image=img)
        image_lbl.image = img 
        image_lbl['bg'] = '#ADD8E6'
        image_lbl.place(x=245,y=280)
        #image_lbl['image'] = 'weather_icons/{}.png'.format(weather[4])
        temp_lbl['text'] = '{:.2f}°C, {:.2f}°F'.format(weather[2], weather[3])
        weather_lbl['text'] = weather[5]
    else:
        messagebox.showerror('Error', 'Cannot find city {}'.format(city))
""""
def clear_text():
    city_entry.delete(0, END)
"""

app = Tk()
app.title('City Weather')
app.geometry('600x400')
app.configure(bg='#ADD8E6')
#Font_tuple = ("Comic Sans MS", 20, "bold")
#bg = PhotoImage(file = "clouds.png")
img = PhotoImage(file='icon.png')
Label(app,image=img, width='100',height='60', bg='#ADD8E6').place(x=247, y=5)


txt_label = Label(app, text='City Weather',font=('Comic Sans MS',15,'bold'),bg='#ADD8E6',width=15)
txt_label.place(x=205,y=60)

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text, font=('Comic Sans MS',8,'bold'),bg='#ffffff')
city_entry.place(x=225,y=100)


search_btn = Button(app, text='Search weather',font=('Comic Sans MS',8,'bold'), width=15, command=search)
search_btn.place(x=239,y=132)

#clearbtn = Button(app, text='Clear', width=12, command=clear_text)
#clearbtn.place(x=252, y=80)

location_lbl = Label(app, text='',font=('Comic Sans MS',20,'bold'), bg='#ADD8E6',width=16)
location_lbl.place(x=159, y=170)

#image_lbl = Label(app, image='')
#image_lbl.pack()

temp_lbl = Label(app, text='',font=('Comic Sans MS',10,'bold'), bg='#ADD8E6',width=16)
temp_lbl.place(x=230,y=220)

weather_lbl = Label(app, text='',font=('Comic Sans MS',15,'bold'), bg='#ADD8E6',width=16)
weather_lbl.place(x=198,y=250)


app.mainloop()