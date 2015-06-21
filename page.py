import re
import requests
from bs4 import BeautifulSoup

import constants

def get_string(regex, string)
    ret = re.findall(regex, string)
    if ret:
        return ret

    return None

class Page(object):
    def __init__(self, url):
        page = requests.get(url);
        if page.status_code != 200:
            logger.info("Get url error, url is " + url)
            return False

        self.soup = BeautifulSoup(page.text)
        self.content = page.conten;
        self.url = url

    def get_username_and_id(self):
        # Get user name id and user name
        line = get_string(REG_USERNAME_L, self.content)
        if not line:
            logger.info("Get username id line error, url is " + self.url)
            return False

        temp = get_string(REG_USERNAMEID, line[0])
        if not temp:
            logger.info("Get username id error, url is " + self.url)
            return False

        username_id = temp[0][1:]
        username, num = re.subn(HTML_LABLE, '', line[0])

       return username, username_id

    def get_notebookIDs(self):
        # Get user notebooks id
        notebookids = []
        lines = get_string(REG_NOTEBOOKIDS_L, self.content)
        if not lines:
            logger.info("Get notebook id lines error, url is " + self.url)
            return False

        for line in lines:
            temp = get_string(REG_NOTEBOOKID, line)
            if not line:
                logger.info("Get notebook id line error, url is " + self.url)
                return False

            notebookids.append(temp[0])

        return notebookids

    def get_diary_date(self):

        try:
            date_html = self.soup.find('div', attrs={'class':'sidebar-item title-date'})
            month_day = date_html.string.strip()
            year = date_html.find('span').string
        except:
            logger.info("Get diary date error, url is " + self.url)
            return False

        date = year+month_day
        return date




