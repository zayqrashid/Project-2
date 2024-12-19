from flask import Blueprint, render_template, request
import socket
import datetime
import json

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('base.html')

@bp.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    weather_info, icon, description, temp, feels_like, humidity, wind_speed, time = get_weather_info(city)
    return render_template('city.html', cityname=city, weather_info=weather_info, icon=icon, description=description, 
                           temp=temp, feels_like=feels_like, humidity=humidity, wind_speed=wind_speed, time=time)

def get_weather_info(city):
    host = '192.168.13.88'  # Server IP address
    port = 8080              # Port to connect to

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.send(city.encode())  # Send city name

    weather_info = client_socket.recv(1024).decode()  # Receive weather information

    client_socket.close()

    print(f"Raw data received: {weather_info}")

    weather_info_parts = weather_info.split('|')

    # Handle the error case where the city was not found
    if weather_info_parts[0] == 'error':
        return weather_info_parts[1], "", "", "", "", "", "", ""

    # Extract data from the split string
    temp = weather_info_parts[1]
    feels_like = weather_info_parts[2]
    humidity = weather_info_parts[3]
    description = weather_info_parts[4]
    time = weather_info_parts[5]
    icon = f"https://openweathermap.org/img/wn/{weather_info_parts[6]}.png"
    wind_speed = weather_info_parts[7]


    return weather_info, icon, description, temp, feels_like, humidity, wind_speed, time