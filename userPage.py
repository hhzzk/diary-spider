#-*- coding: UTF-8 -*-

import re
import os
import requests

import constants
from page import Page
from qiniuApi import push_file
from logger import dlogger as logger

class UserPage(Page):

    def get_joindate(self):
        # Get user join date
        user_info = self.soup.find('div', attrs={'class':'sidebar-item user-info'})
        if not user_info:
            logger.error("Get user info error, url is " + self.url)
            return None

        # 2013-08-16 加入
        try:
            joindate = user_info.p.string[:10]
            logger.info("Get join date " + joindate)
        except:
            logger.error("Get join date error, url is " + self.url)
            return None

        return joindate

    def get_description(self):
        # Get user description
        description = None
        user_info = self.soup.find('div', attrs={'class':'sidebar-item user-info'})
        if not user_info:
            logger.error("Get user info error, url is " + self.url)
            return None

        description = user_info.pre.string
        if description:
            description = description.encode("utf-8")
            logger.info("Get user description " + description)

        return description

    def get_icon_img(self):
        # Get user icon image
        icon_img_info = self.soup.find('img', class_='bigicon')
        if not icon_img_info:
            logger.error("Get icon image line error, url is " + self.url)
            return ()

        try:
            icon_img_url = icon_img_info['src']
        except:
            logger.error("Get icon image url error, info is " + icon_img_info)
            return ()
        logger.info("Get icon image url " + icon_img_url)

        ret = requests.get(icon_img_url)
        if ret.status_code != 200:
            logger.error("Get icon image request error, url is " + icon_img_url)
            return ()

        icon_name = icon_img_url.split('/')[-1].split('?')[0]
        icon_name = 'icon_' + icon_name

        with open(icon_name, 'wb') as file_object:
            file_object.write(ret.content)

        ret = push_file(icon_name)
        os.remove(icon_name)

        if ret:
            logger.info("Push icon image successfully, icon is " + icon_name)
            return icon_name

        logger.error("Push icon image error, icon is " + icon_name)
        return None

    def get_notebooks(self):
        # Get user notebooks id
        notebooks = []
        notebooks_info = self.soup.find_all('div', class_='notebook')
        if not notebooks_info:
            logger.info("The notebooks info is null")
            return notebooks

        try:
            for notebook in notebooks_info:
                # /notebook/550953
                notebook_url = notebook.a['href']
                notebook = notebook_url[10:]
                logger.info("Get notebook id " + notebook)
                notebooks.append(notebook)
        except:
            logger.error("Get notebooks error, url is " + self.url)
            return ()

        return notebooks

