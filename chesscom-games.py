from codecs import open
from datetime import date
import os.path
import requests

def main(user, where):
    print("Downloading %s's games to %s:" % (user, where))
    for archive in get('http://api.chess.com/pub/player/%s/games/archives' % user)['archives']:
        download_archive(archive, where)

def download_archive(url, where):
    games = get(url)['games']
    d = date.fromtimestamp(games[0]['end_time'])
    y = d.year
    m = d.month
    filename = os.path.join(where, "%d-%02d.pgn" % (y, m))
    print('Starting work on %s...' % filename)
    with open(filename, 'w', encoding='utf-8') as output:
        for game in games:
            print(game['pgn'], file=output)
            print('', file=output)

def get(url):
    return requests.get(url).json()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Download a user's games from chess.com")
    parser.add_argument('user', metavar='USER', help='The user whose games we want')
    parser.add_argument('where', metavar='PATH', help='Where to create the PGN files',
            default=".", nargs='?')
    args = parser.parse_args()
    main(args.user, args.where)
