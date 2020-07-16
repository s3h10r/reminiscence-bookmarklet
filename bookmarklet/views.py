import json
import re
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from rest_framework.request import Request as DRF_Request
from rest_framework.response import Response as DRF_Response
from pages.dbaccess import DBAccess as dbxs
from pages.models import UserSettings
from restapi.views import AddURL


def index(request):
    return render(request, 'bookmarklet/index.html', context={})


def get(request, use_api=False):
    """
    renders bookmarklet (js-code)
    """
    URL_BASE = 'http://localhost' # TODO settings.py? docker.env-variable?
    if use_api:
        # if we can use the REST-API directly ...
        target_url = '{}/restapi/add-url/'.format(URL_BASE)
    else:
        # use our own view 'add_to_reminiscence'
        target_url = '{}{}'.format(URL_BASE, reverse('bookmarklet:add_url', args=[]))
    return render(request, 'bookmarklet/AddToReminiscence.js',
        context = {
            'target_url': target_url
        })

@login_required
def add_to_reminiscence(request, url=None, directory=None):
    """
    """
    if request.user:
        res = _add_url(request)
    return HttpResponse(json.dumps(res))


def _add_url(request):
        addURL = AddURL()
        usr = request.user
        if request.method == 'GET':
            url = request.GET.get("url")
            media_link = request.GET.get("media_link")
            if media_link and media_link == "yes":
                is_media_link = True
            else:
                is_media_link = False
            directory = request.GET.get("directory")
            save_favicon = request.GET.get("save_favicon")
        else:
            content = {"msg": "No HTTP-POST allowed here."}
        if media_link and media_link == "yes":
            is_media_link = True
        else:
            is_media_link = False
        if directory and directory.startswith("/"):
            directory = directory[1:]
        if save_favicon and save_favicon == "no":
             save_favicon = False
        else:
            save_favicon = True
        row = UserSettings.objects.filter(usrid=request.user)
        if url:
            http = re.match(r'^(?:http)s?://', url)
        else:
            http = None
        if http and directory:
            if addURL.check_dir_and_subdir(usr, directory):
                dbxs.add_new_url(usr, request, directory, row, is_media_link=is_media_link,
                                 url_name=url, save_favicon=save_favicon)
                content = {"url": url, "is_media_link": is_media_link, "directory": directory, "status": "added"}
            else:
                content = {"msg": "Maybe required directory not found. So please create directories before adding url"}
        else:
            content = {"msg": "wrong url format or directory. url='{}',directory={}".format(url,directory)}
        return content
