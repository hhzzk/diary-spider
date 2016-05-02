#-*- coding: UTF-8 -*-
import io
import os
import json
import requests
from time            import sleep
from random          import randint
from pymongo         import MongoClient
from multiprocessing import Process

from qiniu_api import push_file
from diarypage import DiaryPage
from userpage  import UserPage
from page      import get_newest_diary_no
from logger    import dlogger as logger
from constants import DIARY_URL, PEOPLE_URL, HAVE_NOT_OUTDATE, \
                      USER_ID_MIN, USER_ID_MID, USER_ID_MID2

def random_sleep(interval_min, interval_max):
    sleep(randint(interval_min, interval_max))

# Database init
MONGOCLIENT = MongoClient('localhost', 27017)
DB_DIARY_SPIDER = MONGOCLIENT.diarySpider
COLL_USER = DB_DIARY_SPIDER['coll_user']
COLL_DIARY = DB_DIARY_SPIDER['coll_diary']


def user_spider():
    user_id = USER_ID_MIN
    while 1:
        if user_id > USER_ID_MID:
            user_id = USER_ID_MID2
            continue

        if COLL_USER.find_one({"userid" : str(user_id)}):
            logger.info("This user exist, user number is " + str(user_id))
            user_id = user_id + 1
            continue

        try:
            user_url = PEOPLE_URL + str(user_id)
            user = UserPage(user_url)
            # User does not exist, status will be 1
            if user.status_code != 200:
                post = {"userid"       : str(user_id), \
                        "status"       : str(1)
                       }
                COLL_USER.insert(post)
                logger.error("Get url error, url is " + user_url)

                user_id = user_id + 1
                random_sleep(40, 100)
                continue

            username, userid = user.get_username_and_id()
            joindate = user.get_joindate()
            description = user.get_description()
            icon_img = user.get_icon_img()
            notebooks = user.get_notebooks()

            # Insert into database, status will be 0
            post = {"username"     : username, \
                    "userid"       : userid, \
                    "joindate"     : joindate, \
                    "description"  : description, \
                    "icon_img"     : icon_img, \
                    "notebooks"    : notebooks, \
                    "status"       : str(0)
                   }

            user_file = "user_" + str(user_id)
            with io.open(user_file, 'w', encoding='utf8') as json_file:
                post_string = json.dumps(post, ensure_ascii=False, \
                                         encoding='utf8')
                json_file.write(unicode(post_string))

            push_file(user_file)
            os.remove(user_file)

            COLL_USER.insert(post)

            logger.info("Get user information successfully, \
                    user number is " + str(user_id))

        except:
            logger.error("Get user information error, \
                    user number is " + str(user_id))

        user_id = user_id + 1
        random_sleep(40, 100)

def diary_into_database(diary_no, diary):
    time, content, img_url = diary.get_diary_body()
    if content == HAVE_NOT_OUTDATE:
        post = {"diaryid" : str(diary_no), \
                "status"  : str(1)
               }
        COLL_DIARY.insert(post)
        return True

    img_name = None
    if img_url:
        ret = requests.get(img_url)
        if ret.status_code == 200:
            img_name = 'diary_img_' + str(diary_no) + '_' + \
                       img_url.split('/')[-1]
            with open(img_name, 'wb') as file_object:
                file_object.write(ret.content)

            ret = push_file(img_name)
            os.remove(img_name)

            if ret:
                logger.info("Push dairy image successfully, \
                        image is " + img_name)
        else:
            logger.error("Get image error, url is " + img_url)

    notebook_id, notebook_name = diary.get_notebook_id_name()
    username, userid = diary.get_username_and_id()
    date = diary.get_diary_date()
    comments = diary.get_comments()

    post = {"diaryid"      : str(diary_no), \
            "notebookid"   : notebook_id, \
            "notebookname" : notebook_name, \
            "content"      : content, \
            "img"          : img_name, \
            "userid"       : userid, \
            "username"     : username, \
            "create_date"  : date, \
            "create_time"  : time, \
            "comments"     : comments, \
            "status"       : str(0)
           }

    diary_file = "diary_" + str(diary_no)
    with io.open(diary_file, 'w', encoding='utf8') as json_file:
        post_string = json.dumps(post, ensure_ascii=False, encoding='utf8')
        json_file.write(unicode(post_string))

    push_file(diary_file)
    os.remove(diary_file)
    COLL_DIARY.insert(post)

    return True

def old_diary_spider(diary_no):
    diary_no = diary_no

    while 1:
        if COLL_DIARY.find_one({"diaryid" : str(diary_no)}):
            logger.info("This diary is exist, number is " + str(diary_no))
            diary_no = diary_no - 1
            continue

        diary_url = DIARY_URL + str(diary_no)
        diary = DiaryPage(diary_url)
        if diary.status_code == 200:
            try:
                diary_into_database(diary_no, diary)
                logger.info("Get diary information successfully, \
                        diary number is " + str(diary_no))
                diary_no = diary_no - 1

            except:
                logger.error("Get diary information error, \
                        diary number is " + str(diary_no))
                diary_no = diary_no - 1

        elif diary.status_code == 404:
            post = {"diaryid" : str(diary_no), \
                    "status"  : str(2)
                   }
            COLL_DIARY.insert(post)

            logger.error("Get url error, url is " + diary_url)

        random_sleep(10, 30)


def realtime_diary_spider(diary_no):
    diary_no = diary_no

    while 1:
        if COLL_DIARY.find_one({"diaryid" : str(diary_no)}):
            logger.info("This diary is exist, number is " + str(diary_no))
            diary_no = diary_no + 1
            continue

        diary_url = DIARY_URL + str(diary_no)
        diary = DiaryPage(diary_url)
        if diary.status_code == 200:
            try:
                diary_into_database(diary_no, diary)
                logger.info("Get diary information successfully, \
                        diary number is " + str(diary_no))
                diary_no = diary_no + 1

            except:
                logger.error("Get diary information error, \
                        diary number is " + str(diary_no))
                diary_no = diary_no + 1

        elif diary.status_code == 404:
            post = {"diaryid" : str(diary_no), \
                    "status"  : str(2)
                   }
            COLL_DIARY.insert(post)

            logger.error("Get url error, url is " + diary_url)
            newest_diary_no = get_newest_diary_no()
            if diary_no < newest_diary_no:
                diary_no = diary_no + 1

        random_sleep(10, 30)

def start():
    # Create subthread and run
    Process(target=user_spider, args=()).start()

    newest_diary_no = get_newest_diary_no()
    Process(target=realtime_diary_spider, args=(newest_diary_no)).start()
    Process(target=old_diary_spider, args=(newest_diary_no-1)).start()

if __name__ == '__main__':
    start()
