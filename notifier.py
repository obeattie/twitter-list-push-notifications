#!/usr/bin/env python
import json
import oauth2 as oauth
import os
import sys
import urllib

from config import \
    CONSUMER_KEY, \
    CONSUMER_SECRET, \
    ACCESS_TOKEN, \
    ACCESS_TOKEN_SECRET, \
    PUSH_TOKEN, \
    USERNAME, \
    LIST_ID, \
    ACTION_URL

DATA_FILE_PATH = 'data.json'

# Get or initialise the 'database'
if os.path.exists(DATA_FILE_PATH):
    with open(DATA_FILE_PATH, 'r') as f:
        _data = json.load(f)
else:
    _data = {}
# Merge with defaults
data = {
    'latest_id': None,
}
data.update(_data)

# Configure httplib with the credentials
oauth_consumer = oauth.Consumer(
    key=CONSUMER_KEY,
    secret=CONSUMER_SECRET
)
oauth_token = oauth.Token(
    key=ACCESS_TOKEN,
    secret=ACCESS_TOKEN_SECRET
)
h = oauth.Client(oauth_consumer, oauth_token)

def _fetch_url(url, *args, **kwargs):
    """Fetch a url from Twitter, returning the decoded JSON. Proxies arguments to the HTTP
       client."""
    headers = {}
    
    try:
        headers, response = h.request(url, *args, **kwargs)
        return json.loads(response)
    except Exception:
        # If Twitter's behaving badly, try again in 5 seconds
        if headers.get('status', None) in ('502', '503'):
            print '    !! Twitter returned a %s for %s. Backing off for 5s and retrying.' % (
                headers['status'],
                url
            )
            time.sleep(5)
            print '    ...going again'
            return _fetch_url(url, *args, **kwargs)
        else:
            raise

def fetch_new_tweet():
    """Returns a new Tweet, if there is a newer one."""
    url = 'http://api.twitter.com/1/%s/lists/%s/statuses.json' % (USERNAME, LIST_ID)
    if data['latest_id']:
        url = url + '?' + urllib.urlencode({
            'since_id': data['latest_id']
        })
    
    response = _fetch_url(url, method='GET')
    return (response.pop(1) if response else None)

def push_tweet(tweet):
    r = urllib.urlopen(
        url='https://www.appnotifications.com/account/notifications.json',
        data=urllib.urlencode((
            ('user_credentials', PUSH_TOKEN),
            ('notification[message]', '@%s: %s' % (tweet['user']['screen_name'], tweet['text'])),
            ('notification[title]', u'@%s/%s' % (USERNAME, LIST_ID)),
            ('notification[message_level]', '1'),
            ('notification[action_loc_key]', 'View'),
            ('notification[run_command]', ACTION_URL),
            ('notification[sound]', '3.caf'),
        ))
    )
    assert (r.getcode() == 200) # Check for success

def save_data():
    with open(DATA_FILE_PATH, 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    # Do the thang
    print 'Fetching tweets...'
    tweet = fetch_new_tweet()
    if tweet:
        print 'Pushing new tweet...'
        data['latest_id'] = tweet['id']
        push_tweet(tweet)
        save_data()
    else:
        print '    Nothing new!'
    # Exit successfully
    sys.exit(0)
