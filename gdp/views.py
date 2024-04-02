from django.shortcuts import render
from django.db.models import Max
from gdp.models import GDP

# Create your views here.
def index(request):
    # define which year we want the data from
    max_year = GDP.objects.aggregate(max_yr=Max('year'))
    year = request.GET.get('year', max_year)

    # define number of countries to fetch
    count = int(request.GET.get('count', 10))

    gpps = GDP.objects.filter(year=year).order_by('gdp').reverse()[:count]
    return render(request, 'index.html')