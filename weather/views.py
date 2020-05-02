from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    appid = '72830892de292e572f8f7b7e2bab8610'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    cities = City.objects.all()
    all_cities = []
    for city in cities:
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city.name}&units=metric&appid={appid}').json()
        if res["cod"]=='404':
            break
        city_info={
            'city': city.name,
            'temp': res["main"]["temp"],
            'icon': res["weather"][0]["icon"],
        }
        all_cities.append(city_info)

    context = {'all_info': all_cities, 'form':form}
    return render(request, 'weather/index.html', context)
