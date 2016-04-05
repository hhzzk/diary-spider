Introduction
=====
A spider to get user information and diary from timepill.net<br>

Totally 3 threads, userSpider used to get user information, outedateDiarySpider used to get outedate diary and<br> 
realtimeDiarySpider used to get new diary <br>

This project was written for learning python

Python libs used in this project:
----
* [requests](http://requests-docs-cn.readthedocs.org/zh_CN/latest/index.html)
* [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html)
* [pymongo](http://api.mongodb.org/python/current/)

Database
---
The project use mongoDB, installation method [Install MongoDB](http://docs.mongodb.org/manual/installation/)

Note
---
数据在存入mongoDB时进行了b64encode编码,所以使用是需要b64decode解码
