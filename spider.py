#-*- coding: UTF-8 -*-
from diaryPage import DiaryPage
from userPage import UserPage
from constants import DIARY_URL, PEOPLE_URL


def start():
    ''''
    user_no = 100149027
    user_url = PEOPLE_URL + str(user_no)
    user = UserPage(user_url)

    username, userid = user.get_username_and_id()
    joindate = user.get_joindate()
    description = user.get_description()
    icon_img_url, icon_img = user.get_icon_img()
    notebooks = user.get_notebooks()
    '''

    diary_no = 8792545
    diary_url = DIARY_URL + str(diary_no)
    diary = DiaryPage(diary_url)

    notebook_id, notebook_name = diary.get_notebook_id_name()
    time, content, img, img_url = diary.get_diary_body()
    username, userid = diary.get_username_and_id()
    date = diary.get_diary_date()
    comments = diary.get_comments()

if __name__ == '__main__':
    start()
