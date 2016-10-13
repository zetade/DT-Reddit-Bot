# DolarTodayBot v1.0
import praw
import HTMLParser
import datetime
import time
import requests


class DT_Bot(object):

    def __init__(self):
        self.username = raw_input('Reddit Username: ')
        self.password = raw_input('Reddit Password: ')
        self.subreddit = raw_input('Subreddit: ')
        self.userAgent = 'DolarTodayB v1.0'

    def scrape(self):
        w = requests.get('https://s3.amazonaws.com/dolartoday/data.json')
        data = w.json()
        dolar = str(data['USD']['dolartoday'])
        return dolar

    def create_sidebar(self):
        # To fix character glitch when grabbing the sidebar
        h = HTMLParser.HTMLParser()
        # Initialize PRAW and login
        r = praw.Reddit(user_agent=self.userAgent)
        r.login(self.username, self.password, disable_warning='True')
        # Grab the sidebar template from the wiki
        sidebar = r.get_subreddit(self.subreddit).get_wiki_page('edit_sidebar').content_md
        # Create list from sidebar by splitting at ***
        sidebar_list = sidebar.split('$$$')
        # Sidebar with updated tables - +lucky_guess+sidebar_list[6]
        sidebar = (sidebar_list[0] + precio_final + sidebar_list[2])
        # Fix characters in sidebar
        sidebar = h.unescape(sidebar)
        return sidebar

    def update_reddit(self):
        # Initialize PRAW and login
        r = praw.Reddit(user_agent=self.userAgent)
        r.login(self.username, self.password, disable_warning='True')
        # Grab the current settings
        settings = r.get_subreddit(self.subreddit).get_settings()
        # Update the sidebar
        settings['description'] = sidebar
        settings = r.get_subreddit(self.subreddit).update_settings(description=settings['description'])


dtb = DT_Bot()

while(True):
    print 'Checking price...'
    precio_final = dtb.scrape()
    print 'Grabbing Sidebar Template...'
    sidebar = dtb.create_sidebar()
    print 'Updating Sidebar...'
    dtb.update_reddit()
    print 'Sidebar Updated: '+datetime.datetime.now().strftime('%b %d, %Y at %I:%M%p')
    print 'Sleeping... \n'
    time.sleep(10)
