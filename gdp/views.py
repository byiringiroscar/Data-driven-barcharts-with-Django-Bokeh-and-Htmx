from django.shortcuts import render
from django.db.models import Max
from gdp.models import GDP

# Create your views here.
def index(request):
    max_year = GDP.objects.aggregate(max_yr=Max('year'))
    return render(request, 'index.html')