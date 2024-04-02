from django.shortcuts import render
from django.db.models import Max
from gdp.models import GDP
import math

from bokeh.models import ColumnDataSource
from bokeh.embed import components
from bokeh.plotting import figure



# Create your views here.
def index(request):
    # define which year we want the data from
    max_year = GDP.objects.aggregate(max_yr=Max('year'))['max_yr']
    year = request.GET.get('year', max_year)

    # define number of countries to fetch
    count = int(request.GET.get('count', 10))

    gdps = GDP.objects.filter(year=year).order_by('gdp').reverse()[:count]

    country_names = [d.country for d in gdps]
    country_gdps = [d.gdp for d in gdps]


    cds = ColumnDataSource(data=dict(country_names=country_names, country_gdps=country_gdps))

    fig = figure(x_range=country_names, plot_height=500, title=f'Top {count} GDPs ({year})')
    fig.title.align = 'center'
    fig.title.text_font_size = '1.5rem'
    fig.xaxis.major_label_orientation = math.pi /4

    fig.vbar(source=cds, x='country_names', top='country_gdps', width=0.8)

    script, div = components(fig)

    context = {
        'script': script,
        'div': div,
        'year': year,
        'count': count
    }

    return render(request, 'index.html', context)