import urllib.error
from django.shortcuts import render
import json
import urllib.request
from urllib.parse import quote

# Create your views here.
def index(request):
    data = {}
    city = ''

    if request.method == 'POST':
        try:
            city = request.POST['city']
            encoded_city = quote(city)
            url = f'https://api.openweathermap.org/data/2.5/weather?q={encoded_city}&appid=5e15df7e06a7bffaec25c3049e341532'

            res = urllib.request.urlopen(url).read()
            json_data = json.loads(res)

            data = {
                "country_code": str(json_data['sys']['country']),
                "coordinate": str(json_data['coord']['lon']) + ' ' + str(json_data['coord']['lat']),
                "temp": str(json_data['main']['temp'])+'k',
                "pressure": str(json_data['main']['pressure']),
                "humidity": str(json_data['main']['humidity']),
            }
        except urllib.error.URLError as e:
            data = {"error": "Unable to connect to weather service"}
        except json.JSONDecodeError:
            data = {"error": "Invalid response from weather service"}
        except KeyError:
            data = {"error": "Invalid data recieved from weather service"}
        except Exception as e:
            data = {"error": f"An unexpected error occurred: {str(e)}"}

    return render(request, 'index.html', {'city': city, 'data': data})
