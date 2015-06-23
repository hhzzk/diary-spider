#-*- coding: UTF-8 -*-
from random import randint
from time import sleep
from pymongo import MongoClient
from base64 import b64encode, b64decode

from diaryPage import DiaryPage
from userPage import UserPage
from page import get_newest_diary_no
from logger import dlogger as logger
from constants import DIARY_URL, PEOPLE_URL, ERROR_MAX, \
                      user_min, user_mid, user_mid2

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

            logger.error("Get user information successfully, user number is " + str(user_no))
            user_error_count = 0

        except:
            logger.error("Get user information error, user number is " + str(user_no))
            user_error_count = user_error_count + 1

        user_no = user_no + 1
        randomSleep()

def diarySpider():
    #diary_no = diary_min
    import pdb
    pdb.set_trace()
    diary_no = 50
    newest_diary_no = get_newest_diary_no()
    while 1:

        if coll_diary.find_one({"diaryid" : str(diary_no)}):
            diary_no = diary_no + 1
            continue

        diary_url = DIARY_URL + str(diary_no)
        diary = DiaryPage(diary_url)
        if diary.status_code == 200:
            try:
                notebook_id, notebook_name = diary.get_notebook_id_name()
                time, content, img, img_url = diary.get_diary_body()
                if img:
                    img = b64encode(img)
                if img_url:
                    img_url = b64encode(img_url)
                username, userid = diary.get_username_and_id()
                date = diary.get_diary_date()
                comments = diary.get_comments()

                post = {"diaryid"      : str(diary_no), \
                        "notebookid"   : notebook_id, \
                        "notebookname" : notebook_name, \
                        "context"      : context, \
                        "img"          : img, \
                        "img_url"      : img_url, \
                        "userid"       : userid, \
                        "username"     : username, \
                        "create_date"  : date, \
                        "create_time"  : time, \
                        "comments"     : comments
                        }
                coll_diary.insert(post)
                logger.info("Get diary information successfully, diary number is " + str(diary_no))
                diary_no = diary_no + 1

            except:
                logger.error("Get diary information error, diary number is " + str(diary_no))
                diary_no = diary_no + 1

        elif diary.status_code == 403:
            logger.error("Get url error, status code is 403, url is " + diary_url)
            if diary_no <= newest_diary_no:
                diary_no = diary_no + 1
            else:
                newest_diary_no = get_newest_diary_no()

        #randomSleep()

def start():
    #userSpider()
    diarySpider()

if __name__ == '__main__':
    start()
