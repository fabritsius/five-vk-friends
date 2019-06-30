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
        return redirect('home')

class VkCodeAction(View):
    def get(self, request):
        code = request.GET.get('code', '')
        
        VK_TOKEN_URI = 'https://oauth.vk.com/access_token'
        payload = {
            'client_id':     os.getenv('VK_CLIENT_ID', default=0),
            'client_secret': os.getenv('VK_CLIENT_SECRET', default=0),
            'code':          code,
            'redirect_uri':  request.build_absolute_uri(reverse('home'))
        }
        
        response = requests.get(VK_TOKEN_URI, params=payload).json()
        
        print(f'\n-> Response: {response}\n')
        
        if 'error' in response:
            return redirect('login')
            
        request.session['vk_access_token'] = response['access_token']
        request.session['vk_expires_at'] =   time_after(response['expires_in'])

        return redirect('home')