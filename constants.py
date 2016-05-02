# Define regular expression
# Used to get related string

# Log configuration
LOGS            = '/var/log/'
OLD_LOGS        = '/var/log.old/'
LOG_NAME        = 'diary'
LOG_FILE        = 'diarySpider.log'
LOG_BACKUP_COUNT      = 20
MAX_LOG_SIZE          = 1024 * 1024 * 5

DIARY_URL = 'https://timepill.net/diary/'
PEOPLE_URL = 'https://timepill.net/people/'
HOME_URL = 'http://www.timepill.net/'

USER_ID_MIN = 13
USER_ID_MID = 25050
USER_ID_MID2 = 100022210

DIARY_ID_MIN = 30

HAVE_NOT_OUTDATE = '<pre class="content">\xe6\x97\xa5\xe8\xae\xb0\xe6\x9c\xac\xe5\xb0\x9a\xe6\x9c\xaa\xe8\xbf\x87\xe6\x9c\x9f\xef\xbc\x8c\xe4\xb8\x8d\xe8\x83\xbd\xe6\x9f\xa5\xe7\x9c\x8b\xe4\xb9\x8b\xe5\x89\x8d\xe7\x9a\x84\xe6\x97\xa5\xe8\xae\xb0\xe5\x86\x85\xe5\xae\xb9\xe3\x80\x82</pre>'

