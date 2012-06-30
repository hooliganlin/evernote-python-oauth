evernote-python-oauth
=====================

Python OAuth script inspired by this github gist: https://gist.github.com/1866753
This script uses the Python OAuth library by simplegeo (https://github.com/simplegeo/python-oauth2/)

This simple script should first be edited with your Evernote consumer key, consumer secret token, and your custom callback url on your server to handle Evernote's OAuth's service. Once the temporary key is retrieved, you can run the script again to get the actual authorization token with the following command:

python evernote_oauth_test.py [temporary token] [verifier] [signature_method]

Enjoy!