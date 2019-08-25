import os

BASE_URL = 'https://www.patreon.com/rss/topflighttimemachine?auth='
AUTH_STRING = 'mS--Fe5i4b3IHiy54p540--WuO5bwI5u'
USER_DIR = os.path.expanduser('~')
EPISODE_FOLDER = os.path.join(USER_DIR, 'projects', 'IronFilings', 'IFS-Episodes')
EPISODES_FILE = 'ifs-episodes.txt'
DB = os.path.join(EPISODE_FOLDER, 'ifs-episodes-db.sqlite3')
