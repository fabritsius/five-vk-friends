from time import time
import requests
from random import sample

from django.shortcuts import render, redirect
from django.views import View

class HomeView(View):
    def get(self, request):
        if is_token_valid(request.session):

            VK_API = 'https://api.vk.com/method'
            payload = {
                'access_token': request.session['vk_access_token'],
                'v':            '5.100'
            }

            # get user's name
            res = requests.get(f'{VK_API}/users.get', params=payload).json()

            context = {
                'name':     res['response'][0]['first_name'],
                'friends':  []
            }

            # get user's friends
            res = requests.get(f'{VK_API}/friends.get', params=payload).json()

            friend_uuids = sample(res['response']['items'], 5)

            payload = {
                'user_ids':      ','.join(str(f) for f in friend_uuids),
                'fields':       ['photo_medium'],
                'access_token': request.session['vk_access_token'],
                'v':            '5.100'
            }
            
            # get friends names and profile pictures
            res = requests.get(f'{VK_API}/users.get', params=payload).json()
            
            for friend in res['response']:
                context['friends'].append(friend)

            return render(request, 'home_view.html', context)
        else:
            return redirect('login')

def is_token_valid(session):
    if 'vk_access_token' in session:
        if session['vk_expires_at'] > time():
            return True
    return False