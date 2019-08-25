import os
import ifs.storage as db
import ifs.settings as settings


def list_saved(by_dir=False, by_file=False, by_db=False):
    _saved = []
    if by_dir:
        print('Listing Episodes by MP3 file.')
        for _e in os.listdir(settings.EPISODE_FOLDER):
            _saved.append(_e[:-4])
    elif by_file:
        print('Listing Episodes from text file.')
        with open(settings.EPISODES_FILE, 'r', encoding='utf-8') as _f:
            for _e in _f.read().split('\n'):
                _saved.append(_e)
    elif by_db:
        print('Listing Episodes from SQLite DB.')
        _eps = db.list_episodes()
        if _eps is not None:
            for _e in _eps:
                _saved.append(_e)
        else:
            print('Could not do the DB thing.')
    return _saved


def filter_title(filter_word=None):
    _eps = list_saved(by_dir=True)
    for _ep in _eps:
        if _ep[-3:] == 'mp3':
            _ep = _ep[:-4]
            if filter_word is not None or '':
                if filter_word in _ep:
                    print(_ep)
            else:
                print(_ep)
