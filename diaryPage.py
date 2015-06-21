import re
import requests
from bs4 import BeautifulSoup

import constants

class DiaryPage(userPage):
    def __init__(self, url):


    def get_notebook_name(self):
        # Get notebook name
        line = get_string(REG_NOTEBOOK_NAME_L, self.content)
        if not line:
            logger.info("Get notebook name line error, url is " + self.url)
            return False

        notebook_name, num = re.subn(HTML_LABLE, '', line[0])

        return notebook_name

    def get_diary_body(self):
        # Get diary create time, content and image if exist
        body = soup.find('div', attrs={'class':'body body-no-icon'})

        try:
            # Find create time use div and class
            time = body.find('div', class_='title').string.strip()

            # Find image and content
            temp = body.find('pre', class_='content').string
            if (imge = temp.find('img')):
                img_url = imge['src']
                ret = request.get(img_url)
                if ret != 200
                    logger.info("Get imge error, url is " + img_url)
                    return False
                img = ret.content
                content = temp.contents[1]
            else
                img = None
                content = temp.contents[0]
        except:
            logger.info("Get create time, content and image error, url is " + self.url)
            return False

        return time, content, img

    def get_diary_comments(self):
        # Get comments
        comments_html = soup.find_all('div', class_='comments')
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


