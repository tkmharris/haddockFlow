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

########## HADOCK #########

def report_error(err_msg):
    mastodon.status_post(err_msg, visibility='direct')

def haddockise(str):
    try:
        return '%s%s!' % (str[0].upper(), str[1:])
    except IndexError:
        raise ValueError('Cannot Haddockise an empty string')

def toot_ML_phrase(unused, used, err_msg):

    # get phrase to toot, remove it from unused phrases
    with open(unused, 'r+') as phrase_file:
        phrases = phrase_file.readlines()
        # if no phrases left, report it and ignore rest of function
        if len(phrases) == 0:
            report_error(err_msg)
            return
        phrase_to_toot = random.choice(phrases)
        phrases.remove(phrase_to_toot)
        phrase_to_toot = phrase_to_toot.rstrip()
        phrase_file.seek(0)
        phrase_file.truncate()
        for str in phrases:
            phrase_file.write(str)
        phrase_file.close()

    # toot phrase
    mastodon.toot(haddockise(phrase_to_toot))

    # add tooted phrase to used phrases
    with open(used, 'a') as used_phrase_file:
        used_phrase_file.write(phrase_to_toot)
        used_phrase_file.write('\n')
        used_phrase_file.close()

    # affirm success in console
    print "Blistering barnacles! I've done a toot"

########## MAIN ###########

if __name__=='__main__':

    # user to report errors to
    USER = '@tomharris@mastodon.social'
    # probability we toot a 'special' phrase
    PROB_SPECIAL = 0.1
    # error messages
    REGULAR_ERR = "%s Blistering barnacles! I'm out of regular words to toot" % USER
    SPECIAL_ERR = "%s Thundering typhoons! I'm out of regular words to toot" % USER

    # set up error log
    logging.basicConfig(filename='log/haddockFlow.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger=logging.getLogger(__name__)

    # main action
    try:
        # create actual API instance
        mastodon = Mastodon(
            access_token = 'cred/pytooter_usercred.secret',
            api_base_url = 'https://botsin.space'
        )

        # choose regular or special phrase and toot it
        if random.random() > PROB_SPECIAL:
            toot_ML_phrase('lexicons/regularWords.txt', 'lexicons/usedRegularWords.txt', REGULAR_ERR)
        else:
            toot_ML_phrase('lexicons/specialWords.txt', 'lexicons/usedSpecialWords.txt', SPECIAL_ERR)

    except:
        # log error
        report_error("%s Something's wrong, check the log" % USER)
        logger.error(sys.exc_info())
