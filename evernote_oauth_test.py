#!/usr/bin/python
# This simple script will enable the oauth callbacks to the Evernote OAuth
# services. As of now, the Evernote OAuth url is using the Evernote sandbox servers.
# Be sure to fill in your callback url as well as your consumer key and secret key.
#
# @author linbr

import sys, os
import time
import urllib
import urlparse
import oauth2 as oauth

class EvernoteOAuth(object):
    CONSUMER_KEY = "CONSUMER_KEY"
    CONSUMER_SECRET = "CONSUMER_SECRET"
    OAUTH_TOKEN_URL = "https://www.evernote.com/oauth"
    AUTHORIZE_URL = "https://www.evernote.com/OAuth.action"

    def __init__(self, temp_token=None, verifier=None, signature_method=oauth.SignatureMethod_PLAINTEXT()):
        """
        Constructs the EvernoteOAuth class by creating consumer and client.
        The token is created if an existing token and verifier was passed in

        @param temp_token
        @param verifier
        @param signature_method
        """
        #Perform the initial request to get the temporary token
        if verifier is None:
            self.consumer = oauth.Consumer(key=EvernoteOAuth.CONSUMER_KEY,
                                           secret=EvernoteOAuth.CONSUMER_SECRET)
            self.client = oauth.Client(self.consumer)
         
        else:
            #Peforms the third-leg request from the temporary token from Evernote
            self.consumer = oauth.Consumer(key=EvernoteOAuth.CONSUMER_KEY,
                                           secret=EvernoteOAuth.CONSUMER_SECRET)
            #Create a token from the temporary token to be authorized
            self.token = oauth.Token(temp_token,'')
            self.token.set_verifier(verifier)
            self.client = oauth.Client(self.consumer, self.token)
            self.client.set_signature_method(signature_method)
            
    def get_access_token(self):
        """
        Gets the access token for the last call of the oauth process
        """
        resp, content = self.client.request(EvernoteOAuth.OAUTH_TOKEN_URL, "POST")
        return dict(urlparse.parse_qsl(content))
        
    def get_request_token(self, callback):
       """
       Gets the temporary credentials with the request token content.

       @param callback
       The callback url for the client service to return to.

       @return A dictionary response of the temporary credentials (token, secret)
       """
       params = {
           'oauth_timestamp' : int(time.time()),
           'oauth_nonce' : oauth.generate_nonce(),
           'oauth_callback' : callback
           }
       #make the request call for temporary credentials
       resp, request_content = self.client.request(EvernoteOAuth.OAUTH_TOKEN_URL, "POST",
                                                   body=urllib.urlencode(params))
       if resp['status'] != '200':
           raise Exception('Invalid response %s. Response Body: ' 
                           % (resp['status'], request_content))
        
       return dict(urlparse.parse_qsl(request_content))
                                                         
    def get_redirect_url(self, request_token):
        """
        Returns the url redirect to Evernote's login page
        
        @param request_token
        The oauth token from the temporary credentials
        """
        return EvernoteOAuth.AUTHORIZE_URL + "?oauth_token=%s" % request_token
    
