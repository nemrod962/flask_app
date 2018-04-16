# -*- coding: utf-8 -*-
# config.py

from authomatic.providers import oauth2, oauth1, openid

CONFIG = {

    'tw': {  # Your internal provider name

        # Provider class
        'class_': oauth1.Twitter,

        # Twitter is an AuthorizationProvider so we need to set several other
        # properties too:
        'consumer_key': '########################',
        'consumer_secret': '########################',
    },

    'fb': {

        'class_': oauth2.Facebook,

        # Facebook is an AuthorizationProvider too.
        'consumer_key': '########################',
        'consumer_secret': '########################',

        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['user_about_me', 'email', 'publish_stream'],
    },

    'google': {
        'class_': 'authomatic.providers.oauth2.Google', 
        # Can be a fully qualified string path.

        # Provider type specific keyword arguments:
        #'short_name': 2, 
        # use authomatic.short_name() to generate this automatically
        #google auth provider. nemrod962@gmail.com
        'consumer_key': '933060102795-0hf4m6v3cuq4ocvubaide7ouqui2l4lg.apps.googleusercontent.com',
        'consumer_secret': '8pHg1tH45N1YEzVtCGKEBVt8',
        'scope':
        [
        #'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email'
        ]
    },

    'oi': {

        # OpenID provider dependent on the python-openid package.
        'class_': openid.OpenID,
    },

}
