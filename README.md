####Introduction

&emsp;&emsp;A spider to get user information and diary from timepill.net<br>
&emsp;&emsp;Totally 3 threads, userSpider used to get user information, outedateDiarySpider used to get outedate diary and<br> 
&emsp;&emsp;realtimeDiarySpider used to get new diary <br>
&emsp;&emsp;This project was written for learning python

***

####Python lib used in this project:

* [requests](http://requests-docs-cn.readthedocs.org/zh_CN/latest/index.html)
* [Beautiful Soup 4](http://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html)
* [pymongo](http://api.mongodb.org/python/current/)

***
####Note
数据在存入mongoDB时进行了b64encode编码,所以使用是需要b64decode解码
