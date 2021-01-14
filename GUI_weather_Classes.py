import tkinter as tk
import requests
import os

HEIGHT = 500
WIDTH = 600

class MakeGUI:

    def __init__(self, root):

        canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
        canvas.pack()

        file_dir = os.path.dirname(__file__)
        image_dir = os.path.join(file_dir, 'background.png')
        background_image = tk.PhotoImage(file=image_dir)
        background_label = tk.Label(root, image=background_image)
        background_label.place(relwidth=1, relheight=1)

        frame = tk.Frame(root, bg='#80c1ff', bd=5)
        frame.place(relx=0.5, rely=0.1, relwidth = 0.75, relheight = 0.1, anchor='n')

        entry = tk.Entry(frame, font=40)
        entry.place(relwidth=0.65, relheight=1)

        lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
        lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

        label = tk.Label(lower_frame, font=('Arial', 18), anchor='nw', justify='left', bd=4)
        label.place(relwidth=1, relheight=1)

        button = tk.Button(frame, text='Get Weather', font=40, command=lambda: GetWeather(entry.get(), label))
        button.place(relx=0.7, relwidth=0.3, relheight=1)

       

        

class GetWeather:
    def format_response(self,weather):
    
        try:
            name=weather['name']
            description = weather['weather'][0]['description']
            temp = weather['main']['temp']

            #final_str =  str(name) + ' ' + str(description) + ' ' + str(temp)
            final_str = 'City: %s\nConditions: %s\nTemperature (°C): %s' % (name, description, temp)

        except:
            final_str = 'There was a problem retrieving information.'

        return final_str

    def get_weather(self,city,label):
        #print("Button clicked, " + entry)
        #api.openweathermap.org/data/2.5/forecast?q={city name},{state code},{country code}&appid={API key}
        weather_key = '7076bdf1c054072d1fe38b5c092e2b6e'
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params={'APPID': weather_key, 'q':city, 'units':'metric'}
        response = requests.get(url, params=params)
        weather = response.json()

        label['text']= self.format_response(weather)

    def __init__(self, userentry,label):
        self.label = label
        self.get_weather(userentry,label)

def main():
    root = tk.Tk()
    b = MakeGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
