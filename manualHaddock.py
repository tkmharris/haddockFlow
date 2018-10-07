import random
import sys
import logging
from mastodon import Mastodon

############ SETUP ################

## Done on 2018-10-07 -- tkmh

# Register app - only once!
'''
Mastodon.create_app(
     'pytooterapp',
     api_base_url = 'https://botsin.space',
     to_file = 'cred/pytooter_clientcred.secret'
)
'''

# Log in - either every time, or use persisted
'''
mastodon = Mastodon(
    client_id = 'cred/pytooter_clientcred.secret',
    api_base_url = 'https://botsin.space'
)
mastodon.log_in(
    USERNAME,
    PASSWORD,
    to_file = 'cred/pytooter_usercred.secret'
)
'''

if __name__=='__main__':


    # create actual API instance
    mastodon = Mastodon(
        access_token = 'cred/pytooter_usercred.secret',
        api_base_url = 'https://botsin.space'
    )

    status = raw_input('enter toot: \n')
    mastodon.toot(status)
