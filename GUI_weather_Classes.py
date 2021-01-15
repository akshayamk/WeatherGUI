import tkinter as tk
import requests
import os

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

        label = tk.Label(lower_frame, font=('Arial', 18), anchor='nw', justify='left', bd=4)
        label.place(relwidth=1, relheight=1)

        scroll = tk.Scrollbar(lower_frame, activebackground='#80c1ff', elementborderwidth=1)
        scroll.place(relx=0.9, relwidth=0.1, relheight = 1)
        #mylist = Listbox(lower_frame, yscrollcommand = scro.set )  

        button_weather = tk.Button(frame, text='Current Weather', font=40, command=lambda: GetCurrentWeather(entry.get(), label))
        button_weather.place(rely=0.5, relwidth=0.3, relheight=0.5)

        button_forecast = tk.Button(frame, text='Next 24 Hours Forecast', font=40, command=lambda: GetHourlyForecast(entry.get(), label))
        button_forecast.place(relx= 0.3, rely=0.5, relwidth=0.4, relheight=0.5)

        button_future = tk.Button(frame, text='Next 5 days Forecast', font=40, command=lambda: GetCurrentWeather(entry.get(), label))
        button_future.place(relx= 0.7, rely=0.5, relwidth=0.3, relheight=0.5)

       

class GetHourlyForecast:
    def formate_forecast_response(self, forecast):
        final_str = ''
        try:
            name = forecast['city']['name']
            final_str += 'City: %s\n' % (name)
            for i in range(8):
                datetime = forecast['list'][i]['dt_txt']
                temperature = forecast['list'][i]['main']['temp']
                description = forecast['list'][i]['weather'][0]['description']

                final_str += 'Date/Time: %s\nConditions: %s\nTemperature (°C): %s\n\n' % (datetime, description, temperature)
        
        except:
            final_str = 'There was a problem retrieving information.\nPlease double check information keyed in.'
        
        return final_str
        


    def get_forecast(self, city, label):
        weather_key = '7076bdf1c054072d1fe38b5c092e2b6e'
        url = 'http://api.openweathermap.org/data/2.5/forecast'
        params={'APPID': weather_key, 'q':city, 'units':'metric'}
        response = requests.get(url, params=params)
        forecast = response.json()

        label['text']= self.formate_forecast_response(forecast)
        #self.formate_forecast_response(forecast)
    
    def __init__(self, userentry,label):
        self.label = label
        self.get_forecast(userentry,label)



class GetCurrentWeather:
    def format_response(self,weather,airpollution):
    
        try:
            name=weather['name']
            description = weather['weather'][0]['description']
            temp = weather['main']['temp']
            aqindex = airpollution['list'][0]['main']['aqi']

            #final_str =  str(name) + ' ' + str(description) + ' ' + str(temp)
            final_str = 'City: %s\nConditions: %s\nTemperature (°C): %s\nAir Quality Index: %s' % (name, description, temp, aqindex)

        except:
            final_str = 'There was a problem retrieving information.\nPlease double check information keyed in.'

        return final_str

    def get_weather(self,city,label):
        #print("Button clicked, " + entry)
        #api.openweathermap.org/data/2.5/forecast?q={city name}&appid={API key}
        weather_key = '7076bdf1c054072d1fe38b5c092e2b6e'
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params={'APPID': weather_key, 'q':city, 'units':'metric'}
        response = requests.get(url, params=params)
        weather = response.json()

        lat = weather['coord']['lat']
        lon = weather['coord']['lon']
        url= 'http://api.openweathermap.org/data/2.5/air_pollution'
        params={'APPID': weather_key, 'lat':lat, 'lon':lon}
        response = requests.get(url, params=params)
        airpollution = response.json()

        label['text']= self.format_response(weather, airpollution)

    def __init__(self, userentry,label):
        self.label = label
        self.get_weather(userentry,label)

def main():
    root = tk.Tk()
    root.title("Weather App")
    b = MakeGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
