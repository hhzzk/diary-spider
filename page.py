import re
import requests

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
