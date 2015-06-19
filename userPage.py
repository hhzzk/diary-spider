import re
import requests

import constants

def get_string(regex, string)
    ret = re.findall(regex, string)
    if ret:
        return ret

    return None

class UserPage(userPage):
    def __init__(self, url):


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

    def get_icon_img(self):
        # Get use icon image
        line = get_string(REG_ICON_IMG_L, self.content)
        if not line:
            logger.info("Get icon image line error, url is " + self.url)
            return False

        try:
            icon_img_url = line[0].splite('"')[3]
        except:
            logger.info("Get icon image url error, line is " + line[0])
            return False

        ret = requests.get(icon_img_url)
        if ret.status_code != 200:
            logger.info("Get icon image request error, url is " + icon_img_url)
            return False

        icon_img = ret.content

        return icon_img

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

