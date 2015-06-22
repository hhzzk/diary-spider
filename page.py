import re
import requests
from bs4 import BeautifulSoup

from constants import *
from logger import dlogger as logger

def get_string(regex, string):
    ret = re.findall(regex, string)
    if ret:
        return ret

    return None

class Page(object):
    def __init__(self, url):
        page = requests.get(url);
        import pdb
        pdb.set_trace()
        if page.status_code != 200:
            logger.error("Get url error, url is " + url)
            return None

        self.soup = BeautifulSoup(page.text)
        self.content = page.content;
        self.url = url

    def get_username_and_id(self):
        # Get user id and user name
        user_info = self.soup.find('div', attrs={'class':'sidebar-item user-info'})
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


