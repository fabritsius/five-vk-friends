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

            show_friends = 5
            friend_uuids = res['response']['items']
            num_friends = len(friend_uuids)

            if num_friends > show_friends:
                friend_uuids = sample(friend_uuids, show_friends)

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

            # create a friends message
            if num_friends == 0:
                context['message'] = 'You have no friends'
            elif num_friends == 1:
                context['message'] = 'You have one friend'
            elif num_friends < 6:
                numbers = ['two', 'three', 'four', 'five']
                context['message'] = f'You have {numbers[num_friends - 2]} friends'
            else:
                context['message'] = 'Here are five of your friends'

            return render(request, 'home_view.html', context)
        else:
            return redirect('login')

def is_token_valid(session):
    if 'vk_access_token' in session:
        if session['vk_expires_at'] > time():
            return True
    return False