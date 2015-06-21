# Define regular expression
# Used to get related string

REG_USERNAMEID_L = r'<h2 class="title"><a href="/people/".*'
REG_USERNAMEID = r'/[0-9]{1-10}'
HTML_LABLE = r'<[^>]*>'
REG_JOINDATE_L = r'<p>\d{4}-\d{2}-\d{2} \xe5\x8a\xa0\xe5\x85\xa5</p>'
REG_JOINDATE = r'\d{4}-\d{2}-\d{2}'
REG_DESCRIPTION_L = r'<pre >.*</pre>'
REG_ICON_IMG_L = r'<img class="bigicon" .*>'
REG_NOTEBOOKIDS_L = r'<a class="cov" href="/notebook/.*|<a class="add" href="/notebook/.*'
REG_NOTEBOOK = r'\d{1-10}'
REG_NOTEBOOK_NAME_L = r'<a class="add" href="/notebook/.*'

# Log configuration
LOGS            = '/var/log/'
OLD_LOGS        = '/var/log.old/'
LOG_NAME        = 'diary'
LOG_FILE        = 'diarySpider.log'
LOG_BACKUP_COUNT      = 20
MAX_LOG_SIZE          = 1024 * 1024 * 5


