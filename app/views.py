from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator
from urllib.parse import urlencode

import csv


def index(request):
    return redirect(reverse(bus_stations))


def get_content():
    with open(settings.BUS_STATION_CSV, newline='', encoding='cp1251') as csvfile:
        result = list(csv.DictReader(csvfile))
    return result


def bus_stations(request):
    current_page = int(request.GET.get("page", 1))

    paginator = Paginator(get_content(), settings.BUS_STATIONS_PER_PAGE)
    page_for_view = paginator.get_page(current_page)

    next_page_url = (reverse('bus_stations') + f"?" +
                     urlencode({'page': page_for_view.next_page_number()})
                     if page_for_view.has_next() else None)
    prev_page_url = (reverse('bus_stations') + f"?" +
                     urlencode({"page": page_for_view.previous_page_number()})
                     if page_for_view.has_previous() else None)

    return render(request, 'index.html', context={
        'bus_stations': page_for_view.object_list,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
        'pages': paginator.num_pages
    })
