A simple Python script (to be run as a cron job) that sends push notifications to your iPhone whenever a new update is posted to a specific list

Dependencies
------------

* oauth2 from http://github.com/simplegeo/python-oauth2
* Python >= 2.6
* The "Push" app installed on your iPhone (from http://itunes.apple.com/app/push-3-0/id350973572)

Instructions
------------

1.  Get your Push API key from your iPhone:
    
    1. Open the Push App
    2. Press the Cog icon in the lower left
    3. Go to Other Services > API
    4. Tap the Cog icon in the lower left (again)
    5. Tap "Receive your API Token"
    6. Email the token to yourself

2.  Register a new application at http://dev.twitter.com/, which is needed to make
    authenticated requests.

3.  Create a new file in the same directory as the script called `config.py` (use
    the `config.py.example` template provided), and fill the required information.
    
    `USERNAME` is the username of the list you wish to follow's owner,
    `LIST_ID` is pretty self-explanatory…
    
    The Twitter keys are found in your application's settings, the first two on
    the Application Details page, and the second two on the "My Access Token" page)
    
    `ACTION_URL` is the URL you wish your iPhone to open whenever you tap 'View'
    on the notification. Many clients have their own URL scheme, for instance, to
    open:
    
    * Twitter for iPhone, enter: `tweetie://`
    * Tweetbot, enter: `tweetbot://`

4.  Run the script like so:
    
        python notifier.py

5.  You will receive a notification on your phone whenever a new status is available.

You may wish to setup a cron job to run automatically at an interval of your choice.

A notification is only sent if a new status is posted since the last run. Only the
latest status will be sent if multiple updates have been posted since the last run.
