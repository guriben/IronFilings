import requests
import bs4
import os

from ifs.settings import AUTH_STRING, BASE_URL, EPISODE_FOLDER, EPISODES_FILE
from ifs.utils import list_saved


def get_episodes():
    """
    get the RSS XML and parse it into a list of episode dictionaries
    :return: list of episode dictionaries [{'title': title, 'url': url_to_mp3}]
    :raises: Connection Error
    """
    _url = BASE_URL + AUTH_STRING
    _episodes = []
    try:
        _request = requests.get(url=_url)
        if _request.status_code == requests.codes.ok:
            _xml = _request.text
            _soup = bs4.BeautifulSoup(_xml, 'lxml')
            _posts = _soup.find_all('item')
            for _post in _posts:
                _title = _post.find('title').text
                _mp3_link = _post.find('enclosure')['url']
                _synopsis = _post.find('description')
                _episodes.append({'title': _title,
                                  'synopsis': _synopsis,
                                  'link': _mp3_link})
    except ConnectionError as connection_error:
        print(connection_error)
    return _episodes


def save_episode(title, link):
    """
    get the MP3 for the episode title, save it to disk and update the file
    :param title: title of the episode
    :param link: url of the MP3 with whatever token is required in GET request
    """
    saved_title = title.replace('_', '/')
    if os.path.exists(os.path.join(EPISODE_FOLDER, '{}.mp3'.format(saved_title))):
        print('Apparently got "{}" already.'.format(title))
    else:
        try:
            print('Getting: ', title)
            _mp3 = requests.get(url=link)
            with open(os.path.join(EPISODE_FOLDER, '{}.mp3'.format(saved_title)), 'wb') as _ep:
                print('Saving MP3')
                _ep.write(_mp3.content)
                with open(os.path.join(EPISODE_FOLDER, EPISODES_FILE), 'a') as _f:
                    _f.write('{}\n'.format(title))
                    print('List updated')
        except FileNotFoundError:
            print('Could not write: {}'.format(title))


def get_new_episodes():
    """
    check if there are any new episodes and get them if necessary
    """
    saved_episodes = list_saved(by_dir=True)
    print('Library has        : {} episodes'.format(len(saved_episodes)))
    available_episodes = get_episodes()
    print('Available episodes : {}'.format(len(available_episodes)))
    if len(saved_episodes) < len(available_episodes):
        for episode in saved_episodes:
            episode.replace('/', '_')
        ifs_episodes = [e for e in saved_episodes if e not in available_episodes]
        print('Trying to get  : {} new episodes'.format(len(ifs_episodes) - len(saved_episodes)))
        for episode in ifs_episodes:
            if not os.path.exists(os.path.join(EPISODE_FOLDER,
                                               '{}.mp3'.format(episode['title']))):
                save_episode(episode['title'], episode['link'])
    else:
        print('No new episodes.')
        exit(0)
    print('Done!')


if __name__ == '__main__':
    """ run as script """
    get_new_episodes()
