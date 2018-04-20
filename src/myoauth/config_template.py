# -*- coding: utf-8 -*-
# config.py

from authomatic.providers import oauth2

CONFIG = {

    'google': {
        # Can be a fully qualified string path.
        'class_': 'authomatic.providers.oauth2.Google', 
        #google auth provider. nemrod962@gmail.com
        'consumer_key': '933060102795-0hf4m6v3cuq4ocvubaide7ouqui2l4lg.apps.googleusercontent.com',
        'consumer_secret': '8pHg1tH45N1YEzVtCGKEBVt8',
        'scope':
        [
        #'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email'
        ]
    }
}
