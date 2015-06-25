#!/bin/bash

ps -aux | grep spider.py > .diarySpider.proc_check.temp

if grep -q "sudo python spider.py" .diarySpider.proc_check.temp
then
    exit
else
    sudo python spider.py &
fi

