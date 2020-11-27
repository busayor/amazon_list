import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from . import models

# BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_EBAY_URL = 'https://www.ebay.com/deals/sch?_from=R40&_trksid=p2380779.m570.l1313&_nkw={}'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    # models.Search.objects.create(search=search)
    final_url = BASE_EBAY_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    # print(final_url)
    # soup = BeautifulSoup(data, features='html.parser')
    # error_listing = soup.find_all('div', {'class': 'page-notice__content'})
    # error_search = error_listing.find()
    # print(error_listing)
    soup = BeautifulSoup(data, features='html.parser')
    post_listings = soup.find_all('div', {'class': 'col'})
    post_title = post_listings[0].find(class_='ebayui-ellipsis-2').text
    post_url = post_listings[0].find('a').get('href')
    post_price = post_listings[0].find(class_='first').text
    post_img = post_listings[0].find('img').get('src')

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='ebayui-ellipsis-2').text
        post_url = post.find('a').get('href')
        # what is the underscore after class for?????
        post_price = post.find(class_='first').text
        post_img = post.find('img').get('src')

        final_postings.append((post_title, post_url, post_price, post_img))

    context = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', context)