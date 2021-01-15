import tkinter as tk
import requests
import os
import datetime as dt

HEIGHT = 600
WIDTH = 700


class MakeGUI:

    def __init__(self, root):

        canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
        canvas.pack()

        file_dir = os.path.dirname(__file__)
        image_dir = os.path.join(file_dir, 'background.png')
        self.background_image = tk.PhotoImage(file=image_dir)
        background_label = tk.Label(root, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        frame = tk.Frame(root, bg='#80c1ff', bd=5)
        frame.place(relx=0.5, rely=0.1, relwidth = 0.75, relheight = 0.2, anchor='n')

        entry = tk.Entry(frame, font=40, bd=3)
        #entry.place(relwidth=0.65, relheight=1)
        entry.place(relwidth=1, relheight=0.5, anchor='nw')

        lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
        lower_frame.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.6, anchor='n')

        label = tk.Label(lower_frame, anchor='nw', justify='left', bd=4)
        label.place(relwidth=1, relheight=1)

        scroll = tk.Scrollbar(lower_frame, activebackground='#80c1ff', elementborderwidth=1)
        scroll.place(relx=0.9, relwidth=0.1, relheight = 1)

        button_weather = tk.Button(frame, text='Current Weather', font=40, command=lambda: GetCurrentWeather(entry.get(), lower_frame))
        button_weather.place(rely=0.5, relwidth=0.3, relheight=0.5)

        button_forecast = tk.Button(frame, text='24 Hours Forecast', font=40, command=lambda: GetHourlyForecast(entry.get(), lower_frame))
        button_forecast.place(relx= 0.3, rely=0.5, relwidth=0.4, relheight=0.5)

        button_future = tk.Button(frame, text='Next 7 days Forecast', font=40, command=lambda: GetFutureForecast(entry.get(), lower_frame))
        button_future.place(relx= 0.7, rely=0.5, relwidth=0.3, relheight=0.5)
    

class GetFutureForecast:
    def format_future_forecast_response(self, forecast, lower_frame, weather_key):
        try:
            mylist = tk.Listbox(lower_frame)
            name = forecast['name']
            final_str = 'City: %s' % (name)
            mylist.insert(tk.END, final_str)
            mylist.insert(tk.END, ' ')
            lat = forecast['coord']['lat']
            lon = forecast['coord']['lon']
            url= 'http://api.openweathermap.org/data/2.5/onecall'
            params={'APPID': weather_key, 'lat':lat, 'lon':lon, 'exclude':['current,minutely,hourly,alerts'], 'units':'metric'}
            response = requests.get(url, params=params)
            futureforecast = response.json()
            for i in range(7):
                datetime = futureforecast['daily'][i]['dt']
                datetime_convert = dt.datetime.fromtimestamp(int(datetime)).strftime('%Y-%m-%d %H:%M:%S')
                daytemp = futureforecast['daily'][i]['temp']['day']
                nighttemp = futureforecast['daily'][i]['temp']['night']
                description = futureforecast['daily'][i]['weather'][0]['description']
        
                
                final_str = 'Date/Time: %s' % (datetime_convert)
                mylist.insert(tk.END, final_str)
                final_str = 'Conditions: %s' % (description)
                mylist.insert(tk.END, final_str)
                final_str = 'Day Temperature (°C): %s' % (daytemp)
                mylist.insert(tk.END, final_str)
                final_str = 'Night Temperature (°C): %s' % (nighttemp)
                mylist.insert(tk.END, final_str)
                mylist.insert(tk.END, ' ')


        except:
            final_str = 'There was a problem retrieving information. Please check again.'
            mylist.insert(tk.END, final_str)

        mylist.place(relwidth = 0.9, relheight = 1)


    def get_future_forecast(self, city, lower_frame):
        weather_key = '7076bdf1c054072d1fe38b5c092e2b6e'
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params={'APPID': weather_key, 'q':city, 'units':'metric'}
        response = requests.get(url, params=params)
        forecast = response.json()

        self.format_future_forecast_response(forecast, lower_frame, weather_key)

    def __init__(self,userentry,lower_frame):   
        self.lower_frame = lower_frame
        self.get_future_forecast(userentry,lower_frame)   

class GetHourlyForecast:
    def formate_forecast_response(self, forecast, lower_frame):
        final_str = ''
        mylist = tk.Listbox(lower_frame)
        try:
            name = forecast['city']['name']
            final_str += 'City: %s\n' % (name)
            mylist.insert(tk.END, final_str)
            mylist.insert(tk.END, ' ')
            final_str = ''
            for i in range(8):
                datetime = forecast['list'][i]['dt_txt']
                temperature = forecast['list'][i]['main']['temp']
                description = forecast['list'][i]['weather'][0]['description']

                final_str = 'Date/Time: %s' % (datetime)
                mylist.insert(tk.END, final_str)
                final_str = 'Conditions: %s' % (description)
                mylist.insert(tk.END, final_str)
                final_str = 'Temperature (°C): %s' % (temperature)
                mylist.insert(tk.END, final_str)
                mylist.insert(tk.END, ' ')
        
        except:
            final_str = 'There was a problem retrieving information. Please check again.'

            mylist.insert(tk.END, final_str)
        

        mylist.place(relwidth = 0.9, relheight = 1)
        

        
    
    def get_forecast(self, city, lower_frame):
        weather_key = '7076bdf1c054072d1fe38b5c092e2b6e'
        url = 'http://api.openweathermap.org/data/2.5/forecast'
        params={'APPID': weather_key, 'q':city, 'units':'metric'}
        response = requests.get(url, params=params)
        forecast = response.json()

        self.formate_forecast_response(forecast, lower_frame)
    
    def __init__(self, userentry,lower_frame):
        self.lower_frame = lower_frame
        self.get_forecast(userentry,lower_frame)



class GetCurrentWeather:
    def format_response(self,weather, lower_frame, weather_key):
    
        try:
            mylist = tk.Listbox(lower_frame)
            name=weather['name']
            description = weather['weather'][0]['description']
            temp = weather['main']['temp']

            lat = weather['coord']['lat']
            lon = weather['coord']['lon']
            url= 'http://api.openweathermap.org/data/2.5/air_pollution'
            params={'APPID': weather_key, 'lat':lat, 'lon':lon}
            response = requests.get(url, params=params)
            airpollution = response.json()
            aqindex = airpollution['list'][0]['main']['aqi']

            #final_str =  str(name) + ' ' + str(description) + ' ' + str(temp)
            #final_str = 'City: %s\nConditions: %s\nTemperature (°C): %s\nAir Quality Index: %s' % (name, description, temp, aqindex)
            final_str = 'City: %s' % (name)
            mylist.insert(tk.END, final_str)
            final_str = 'Conditions: %s' % (description)
            mylist.insert(tk.END, final_str)
            final_str = 'Temperature (°C): %s' % (temp)
            mylist.insert(tk.END, final_str)
            final_str = 'Air Quality Index: %s' % (aqindex)
            mylist.insert(tk.END, final_str)

        except:
            final_str = 'There was a problem retrieving information. Please check again.'
            mylist.insert(tk.END, final_str)

        mylist.place(relwidth = 0.9, relheight = 1)


    def get_weather(self,city,lower_frame):
        #print("Button clicked, " + entry)
        #api.openweathermap.org/data/2.5/forecast?q={city name}&appid={API key}
        weather_key = '7076bdf1c054072d1fe38b5c092e2b6e'
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params={'APPID': weather_key, 'q':city, 'units':'metric'}
        response = requests.get(url, params=params)
        weather = response.json()

        self.format_response(weather, lower_frame, weather_key)

    def __init__(self, userentry,lower_frame):
        self.lower_frame = lower_frame
        self.get_weather(userentry,lower_frame)

def main():
    root = tk.Tk()
    root.title("Weather App")
    b = MakeGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
