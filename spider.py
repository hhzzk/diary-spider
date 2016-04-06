#-*- coding: UTF-8 -*-
from random import randint
from time import sleep
from pymongo import MongoClient
from base64 import b64encode, b64decode
from  multiprocessing import Process

from diaryPage import DiaryPage
from userPage import UserPage
from page import get_newest_diary_no
from logger import dlogger as logger
from constants import DIARY_URL, PEOPLE_URL, ERROR_MAX, \
                      user_min, user_mid, user_mid2, \
                      HAVE_NOT_OUTDATE, current_diary_no, \
                      diary_min

user_error_count = 0

def randomSleep(min, max):
    sleep(randint(min, max))

# Database init
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

        # If too mang error, sleep 1 hour
        if user_error_count > ERROR_MAX:
            logger.warning("Error count over the max value!!!")
            user_no = user_no - ERROR_MAX
            sleep(3600)
            continue

        if coll_user.find_one({"userid" : str(user_no)}):
            logger.info("This user exist, user number is " + str(user_no))
            user_no = user_no + 1
            continue

        try:
            user_url = PEOPLE_URL + str(user_no)
            user = UserPage(user_url)
            if user.status_code != 200:
                logger.error("Get url error, url is " + user_url)
                user_no = user_no + 1
                user_error_count = user_error_count + 1
                randomSleep(40, 100)
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

            logger.info("Get user information successfully, user number is " + str(user_no))
            user_error_count = 0

        except:
            logger.error("Get user information error, user number is " + str(user_no))
            user_error_count = user_error_count + 1

        user_no = user_no + 1
        randomSleep(40, 100)

def diary_into_database(diary_no, diary):
    time, content, img, img_url = diary.get_diary_body()
    if content == HAVE_NOT_OUTDATE:
        post = {"diaryid" : str(diary_no), \
                "status"  : str(1)
               }
        coll_diary.insert(post)
        return True

    if img:
        img = b64encode(img)
    if img_url:
        img_url = b64encode(img_url)
    notebook_id, notebook_name = diary.get_notebook_id_name()
    username, userid = diary.get_username_and_id()
    date = diary.get_diary_date()
    comments = diary.get_comments()

    post = {"diaryid"      : str(diary_no), \
            "notebookid"   : notebook_id, \
            "notebookname" : notebook_name, \
            "content"      : content, \
            "img"          : img, \
            "img_url"      : img_url, \
            "userid"       : userid, \
            "username"     : username, \
            "create_date"  : date, \
            "create_time"  : time, \
            "comments"     : comments, \
            "status"       : str(0)
            }
    coll_diary.insert(post)

    return True


def realtimeDiarySpider():
    diary_no = current_diary_no
    newest_diary_no = get_newest_diary_no()
    while 1:

        if coll_user.find_one({"diaryid" : str(diary_no)}):
            diary_no = diary_no + 1
            continue

        diary_url = DIARY_URL + str(diary_no)
        diary = DiaryPage(diary_url)
        if diary.status_code == 200:
            try:
                diary_into_database(diary_no, diary)
                logger.info("Get diary information successfully, diary number is " + str(diary_no))
                diary_no = diary_no + 1

            except:
                logger.error("Get diary information error, diary number is " + str(diary_no))
                diary_no = diary_no + 1

        elif diary.status_code == 404:
            post = {"diaryid" : str(diary_no), \
                    "status"  : str(2)
                   }
            coll_diary.insert(post)

            logger.error("Get url error, status code is 404, url is " + diary_url)
            if diary_no <= newest_diary_no:
                diary_no = diary_no + 1
            else:
                newest_diary_no = get_newest_diary_no()

        randomSleep(10, 20)




def start():
    # Create subthread and run
    userSpider()
    #Process(target=userSpider, args=()).start()
    #Process(target=realtimeDiarySpider, args=()).start()

if __name__ == '__main__':
    start()
