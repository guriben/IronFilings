import requests
import bs4
import os

PATREON_RSS = 'https://www.patreon.com/rss/'
PODCAST = 'topflighttimemachine'
GET = '?auth='
AUTH_STRING = 'mS--Fe5i4b3IHiy54p540--WuO5bwI5u'
USER_DIR = os.path.expanduser('~')
EPISODE_FOLDER = os.path.join(USER_DIR, 'projects', 'IronFilings', 'IFS-Episodes')
EPISODES_FILE = 'ifs-episodes.txt'


def get_episodes(url):
    """
    get the RSS XML and parse it into a list of episode dictionaries
    :param: url composed URL with authentication uuid
    :return: list of episode dictionaries [{'title': title, 'url': url_to_mp3}]
    :raises: Connection Error
    """
    _episodes = []
    try:
        _request = requests.get(url)
        if _request.status_code == requests.codes.ok:
            _xml = _request.text
            _soup = bs4.BeautifulSoup(_xml, 'lxml')
            _posts = _soup.find_all('item')
            for _post in _posts:
                _title = _post.find('title').text
                _mp3_link = _post.find('enclosure')['url']
                _synopsis = _post.find('description').text[3:-4]
                _episodes.append({'title': _title,
                                  'synopsis': _synopsis,
                                  'link': _mp3_link})
    except ConnectionError as connection_error:
        print(connection_error)
    return _episodes


def save_episode(episode):
    """
    get the MP3 for the episode title, save it to disk and update the file
    :param episode: episode dictionary
    """
    title = episode['title']
    synopsis = episode['synopsis']
    link = episode['link']
    if os.path.exists(os.path.join(EPISODE_FOLDER, '{}.mp3'.format(title))):
        print('Apparently got "{}" already.'.format(title))
    else:
        try:
            print('Getting: ', title)
            _mp3 = requests.get(url=link)
            with open(os.path.join(EPISODE_FOLDER, '{}.mp3'.format(title)), 'wb') as _ep:
                print('Saving MP3...')
                _ep.write(_mp3.content)
                with open(EPISODES_FILE, 'a') as _f:
                    _f.write('{}\t"{}"\n'.format(title, synopsis))
        except FileNotFoundError:
            print('Could not write: {}'.format(title))
        except ConnectionError:
            print('Could not get  : {}'.format(title))


def synchronise(url):
    """
    :param: the URL to the episode feed with GET user authentication
    check if there are any new episodes and get them if necessary
    """
    saved_episodes = []
    for file in os.listdir(EPISODE_FOLDER):
        saved_episodes.append(file[:-4])
    print('Library has        : {} episodes'.format(len(saved_episodes)))
    available_episodes = get_episodes(url)
    print('Available episodes : {}'.format(len(available_episodes)))
    if len(saved_episodes) < len(available_episodes):
        new_episodes = [e for e in available_episodes if e not in saved_episodes]
        print('Trying to get  : {} new episodes'.format(len(new_episodes)))
        for episode in new_episodes:
            if not os.path.exists(os.path.join(EPISODE_FOLDER, '{}.mp3'.format(episode['title']))):
                save_episode(episode)
    else:
        print('No new episodes.')
        exit(0)
    print('Done!')


if __name__ == '__main__':
    """ run as script """
    synchronise(PATREON_RSS + PODCAST + GET + AUTH_STRING)
