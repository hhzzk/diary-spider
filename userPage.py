import re
import requests

import constants


def get_string(regex, string)
    ret = re.findall(regex, string)
    if ret:
        return ret

    return None

class UserPage(Page):
    def __init__(self, url):

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

    def get_joindate(self):
        # Get user join date
        line = get_string(REG_JOINDATE_L, self.content)
        if not line:
            logger.info("Get join date line error, url is " + self.url)
            return False

        temp = get_string(REG_JOINDATE, self.content)
        if not temp:
            logger.info("Get join date error, url is " + self.url)
            return False

        joindate = temp[0]

        return joindate

    def get_description(self):
        # Get user description
        line = get_string(REG_DESCRIPTION_L, self.content)
        if not line:
            logger.info("Get description line error, url is " + self.url)
            return False

        description = re.subn(HTML_LABLE, '', line)

        return description


