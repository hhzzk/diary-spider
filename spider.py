#-*- coding: UTF-8 -*-
from random import randint
from time import sleep

from diaryPage import DiaryPage
from userPage import UserPage
from constants import DIARY_URL, PEOPLE_URL, ERROR_MAX, \
                      user_min, user_mid, user_mid2
from logger import dlogger as logger
from pymongo import MongoClient
from base64 import b64encode, b64decode

user_error_count = 0

def randomSleep():
    sleep(randint(40,100))

#database init
client = MongoClient('localhost', 27017)
db_diarySpider = client.diarySpider
coll_user = db_diarySpider['coll_user']
coll_diary = db_diarySpider['coll_diary']


def userSpider():
    global user_error_count
    user_no = user_min
    while 1 :
        if user_no < user_mid2 and user_no > user_mid:
            user_no = user_mid2
            continue

        # If too much error, then sleep 1 hour
        if user_error_count > ERROR_MAX:
            logger.warning("Error count over the max value!!!")
            user_no = user_no - ERROR_MAX
            sleep(3600)
            continue

        if coll_user.find_one({"userid" : str(user_no)}):
            user_no = user_no + 1
            continue

        try:
            user_url = PEOPLE_URL + str(user_no)
            user = UserPage(user_url)
            if user.status_code != 200:
                logger.error("Get url error, url is " + user_url)
                user_no = user_no + 1
                user_error_count = user_error_count + 1
                randomSleep()
                continue

            username, userid = user.get_username_and_id()
            joindate = user.get_joindate()
            description = user.get_description()
            if description:
               description =  b64encode(description)
            icon_img_url, icon_img = user.get_icon_img()
            notebooks = user.get_notebooks()

            # Insert into database
            post = {"username"     : username, \
                    "userid"       : userid, \
                    "joindate"     : joindate, \
                    "description"  : description, \
                    "icon_img_url" : b64encode(icon_img_url), \
                    "icon_img"     : b64encode(icon_img), \
                    "notebooks"    : notebooks
                    }
            coll_user.insert(post)

            user_error_count = 0

        except:
            logger.error("Get user information error, user number is " + str(user_no))
            user_error_count = user_error_count + 1

        user_no = user_no + 1
        randomSleep()

def diarySpider():
    diary_no = 8792545
    diary_url = DIARY_URL + str(diary_no)
    diary = DiaryPage(diary_url)

    notebook_id, notebook_name = diary.get_notebook_id_name()
    time, content, img, img_url = diary.get_diary_body()
    username, userid = diary.get_username_and_id()
    date = diary.get_diary_date()
    comments = diary.get_comments()

def start():
    userSpider()
    #diarySpider()

if __name__ == '__main__':
    start()
