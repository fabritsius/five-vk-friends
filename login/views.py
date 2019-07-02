import requests
import os

from .additional_logic import time_after

from django.shortcuts import render, redirect, reverse
from django.views import View

class LoginView(View):
    def get(self, request):
        return render(request, 'login_view.html', {})

class LoginWithVkAction(View):
    def get(self, request):
        VK_AUTHORIZE_URI = 'https://oauth.vk.com/authorize'
        payload = {
            'client_id':     os.getenv('VK_CLIENT_ID', default=0),
            'scope':         ['friends'],
            'redirect_uri':  request.build_absolute_uri(reverse('vk_token')),
            'response_type': 'code',
            'v':             '5.100'
        }

        req = requests.Request('GET', VK_AUTHORIZE_URI, params=payload).prepare()
        
        return redirect(req.url)

class VkCodeAction(View):
    def get(self, request):
        code = request.GET.get('code', '')
        
        VK_TOKEN_URI = 'https://oauth.vk.com/access_token'
        payload = {
            'client_id':     os.getenv('VK_CLIENT_ID', default=0),
            'client_secret': os.getenv('VK_CLIENT_SECRET', default=0),
            'code':          code,
            'redirect_uri':  request.build_absolute_uri(reverse('vk_token')),
            'v':             '5.100'
        }
        
        response = requests.get(VK_TOKEN_URI, params=payload).json()
        
        if 'error' in response:
            return redirect('login')
            
        request.session['vk_access_token'] = response['access_token']
        request.session['vk_expires_at'] =   time_after(response['expires_in'])

        return redirect('home')

class LogoutAction(View):
    def get(self, requests):
        requests.session.flush()
        
        return redirect('login')