from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
from bs4 import BeautifulSoup
from .models import Link

# Create your views here.
def scraper_view(request):
    if request.method == 'POST':
        site = request.POST.get('site', '')

        page = requests.get(site)
        soup = BeautifulSoup(page.text, 'html.parser')

        for link in soup.find_all('a'):
            links = link.get('href')
            link_text = link.string
            Link.objects.create(address=links, name=link_text)
        return HttpResponseRedirect('/')
    else:
        data = Link.objects.all()
        context = {'data': data}
        return render(request, 'scraper/result.html', context)

def clear(request):
    Link.objects.all().delete()
    return render(request, 'scraper/result.html')