import re
import requests
from bs4 import BeautifulSoup

from constants import *
from logger import dlogger as logger

def get_newest_diary_no():
    home = requests.get(HOME_URL)
    if home.status_code != 200:
        logger.error("Get home page error!!")
        return 0
    soup = BeautifulSoup(home.text)
    newest_info = soup.find('div', class_="bottom")
    # /diary/8797403
    newest_url = newest_info.a['href']
    if newest_url:
        newest = newest_url[7:]
        logger.info("Get newest diary no " + newest)
        return int(newest)

    return 0


class Page(object):
    def __init__(self, url):
        page = requests.get(url);

        self.soup = BeautifulSoup(page.text, "html5lib")
        self.content = page.content;
        self.url = url
        self.status_code = page.status_code

    def get_username_and_id(self):
        # Get user id and user name
        user_info = self.soup.find('div', \
                attrs={'class':'sidebar-item user-info'})
        if not user_info:
            logger.error("Get user info error, url is " + self.url)
            return ()

        username = user_info.h2.a.string
        logger.info("Get user name " + username)
        # '/people/100149027'
        user_url = user_info.h2.a['href']
        if not user_url:
            logger.error("Get user_url error, url is " + self.url)
            return ()
        userid = user_url[8:]
        logger.info("Get user id " + userid)

        return username, userid


