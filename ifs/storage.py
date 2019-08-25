import sqlite3

from ifs.settings import DB


def acquire(db_path=DB):
    """
    get a db cursor...generally used internally
    :param db_path: hopefully a SQLite string
    :return: db cursor
    """
    try:
        _connection = sqlite3.connect(db_path)
        _cursor = _connection.cursor()
        return _cursor
    except Exception as e:
        print(e)
        return None


def setup():
    """
    create table if needed
    :return:
    """
    _sql = "CREATE TABLE IF NOT EXISTS episodes (" \
           "id INTEGER PRIMARY KEY, " \
           "title STRING NOT NULL, " \
           "synopsis STRING, " \
           "published STRING);"
    _db = acquire()
    try:
        _db.execute(_sql)
        _db.commit()
        _db.save()
    except Exception as e:
        print(e)


def store(episode=None):
    """
    store the details of an episode
    :param episode: dictionary of details or defaults to test data
    """
    test_episode = {'title': 'test IFS 3', 'synopsis': 'test synopsis', 'published': 'some date'}
    if episode is None:
        episode = test_episode
        _title = episode['title']
        _synopsis = episode['synopsis']
        _published_date = episode['published']
        print('Store:', _title, _published_date)
        _sql = "INSERT INTO episodes (title, synopsis, published) VALUES (?, ?, ?);"
        _db = acquire()
        try:
            _db.execute(_sql, (_title, _synopsis, _published_date))
            _db.commit()
            _db.save()
        except Exception as e:
            print(e)


def list_episodes():
    """
    print the episodes in the DB
    :return:
    """
    _sql = "SELECT * FROM episodes;"
    _db = acquire()
    _results = _db.execute(_sql)
    for _result in _results.fetchall():
        print(_result)
