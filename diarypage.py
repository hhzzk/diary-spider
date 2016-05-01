#-*- coding: UTF-8 -*-
from page import Page
from logger import dlogger as logger

class DiaryPage(Page):

    def get_notebook_id_name(self):
        # Get notebook name
        notebook_info = self.soup.find('a', class_='add')
        try:
            notebook_name = notebook_info.contents[0]
            notebook_url = notebook_info['href']
            #/notebook/549997
            notebook_id = notebook_url[10:]
            logger.info("Get notebook id " + notebook_id)
            logger.info("Get notebook name " + notebook_name)
        except:
            logger.error("Get notebook id and name error, url is " + self.url)
            return ()

        return notebook_id, notebook_name

    def get_diary_body(self):
        # Get diary create time, content and image if exist
        body = self.soup.find('div', attrs={'class':'body body-no-icon'})

        try:
            # Find create time use div and class
            time = body.div.string.strip()
            logger.info("Get diary create time " + time)

            # Find image and content
            image = body.pre.img
            if image and 'thumbnail' in image['class'] :
                img_url = image['src']
                logger.info("Get image url " + img_url)

            else:
                img_url = None
            content = body.pre.encode('utf-8')
            #logger.info("Get diary content " + content)

        except:
            logger.error("Get create time, content and image error, \
                    url is " + self.url)
            return ()

        return time, content, img_url

    def get_diary_date(self):

        try:
            date_info = self.soup.find('div', \
                    attrs={'class':'sidebar-item title-date'})
            month_day = date_info.contents[0].strip()
            year = date_info.span.string
        except:
            logger.error("Get diary date error, url is " + self.url)
            return False

        date = month_day+year
        logger.info("Get date " + date)
        return date

    def get_comments(self):
       # Get comments
        comments = []
        comments_info = self.soup.find_all('div', class_='comment')
        if not comments_info:
            logger.info("The comments info is null")
            return comments

        try:
            for comment in comments_info:
                who = comment.a['href'][8:]
                time = comment.div.div.contents[2].strip()
                comment_body = comment.pre.encode("utf-8")
                logger.info("Get comment |" + who + " | " + time)
                comment_list = (who, time, comment_body)
                comments.append(comment_list)
        except:
            logger.error("Get comments error, url is " + self.url)
            return False

        return comments




