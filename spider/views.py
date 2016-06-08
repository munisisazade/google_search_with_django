from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.core.context_processors import csrf
# from django.views.generic import View
# from django.db.utils import IntegrityError
# from django.core.urlresolvers import reverse
from django.template import RequestContext
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, Http404, HttpResponseForbidden
from spider.models import *
from spider.forms import *
import requests as sorgu
from bs4 import BeautifulSoup as bs
# from news.forms import RegisterForm, LoginForm, AddArticleForm , SearchForm, ContactForm
# from django.contrib.auth.models import User
# from django.utils.translation import gettext_lazy as _
# from django.db.models import Q
# from django.db.models import Avg, Max, Min
# from django.core.mail import send_mail
#
# import json


def base(req=None):
    data = {}
    data.update(csrf(req))
    return data


def index(request):
    rend_it = base(req=request)
    return render_to_response('index.html', rend_it, context_instance=RequestContext(request))


def Search(request):
    if request.method == 'POST' and 'q' in request.POST:
        rend_it = base(req=request)
        post = request.POST.copy()
        form = SearchForm(post)
        if form.is_valid():
            data = form.cleaned_data
            try:
                r = sorgu.get('http://google.ru/search?q=' + data.get('q'))
                if r.status_code == 200:
                    soup = bs(r.text, 'html.parser')
                    arr = soup.find(attrs={"id":"ires"})
                    for x in arr.find_all('a'):
                        x['href'] = 'https://google.ru' + x['href']
                    rend_it['links'] = arr
                    rend_it['abr'] = data.get('q')
                    return render_to_response('index.html', rend_it, context_instance=RequestContext(request))
                else:
                    rend_it['abr'] = data.get('q')
                    rend_it['error'] = 'Belə url yoxdu'
                    return render_to_response('index.html', rend_it, context_instance=RequestContext(request))
            except:
                rend_it['error'] = 'Belə url yoxdu'
                return render_to_response('index.html', rend_it, context_instance=RequestContext(request))
        else:
            return redirect('/')
