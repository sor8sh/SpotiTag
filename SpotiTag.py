import requests
import json
from pathlib import Path
from datetime import datetime


class SpotiTag:
    def __init__(self, token, tag, output_dir='./output', write=True):
        self.token = token
        self.tag = tag
        self.write = write

        # Output directories
        self.output_dir = '{}/{}_{}/'.format(output_dir, self.tag, datetime.today().strftime('%Y-%m-%d'))
        self.playlists_dir = self.output_dir + '{}_playlists.json'.format(self.tag)
        self.songs_dir = '{}{}_songs.json'.format(self.output_dir, self.tag)
        self.ranked_dir = '{}{}_ranked.txt'.format(self.output_dir, self.tag)

    def get_playlists(self):
        scope = 'playlist'
        url = 'https://api.spotify.com/v1/search?q={}&type={}&limit=50&offset={}'.format(
            self.tag.replace(' ', '+'), scope, 0)
        playlists = []

        while url is not None:
            response = requests.get(
                url,
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer {}'.format(self.token)
                }
            ).json()

            if response.keys() == {'error'}:
                if response['error']['status'] == 401:
                    print(response['error']['message'])
                break
            print(url)

            playlists.extend(response['playlists']['items'])
            url = response['playlists']['next']

        if self.write:
            with open(self.playlists_dir, 'w') as f:
                json.dump(playlists, f)

    def get_songs(self, total_dict, playlist_url):
        url = playlist_url + '/tracks'

        local_songs = set()
        while url is not None:
            response = requests.get(
                url,
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer {}'.format(self.token)
                }
            ).json()

            if response == {'error': {'status': 404, 'message': 'Not found.'}}:
                break
            if 'items' not in response.keys():
                continue

            for i in range(len(response['items'])):
                if response['items'][i]['track'] is None:
                    continue

                title = response['items'][i]['track']['name']
                title_id = response['items'][i]['track']['name'].split('-')[0].replace(' ', '')
                artists, artists_id = [], ''
                for artist in response['items'][i]['track']['artists']:
                    artists.append(artist['name'])
                    artists_id += artist['name']
                record_id = '{}-{}'.format(title_id, artists_id)

                if record_id in local_songs:
                    continue
                local_songs.add(record_id)

                if record_id not in total_dict.keys():
                    try:
                        cover = response['items'][i]['track']['album']['images'][0]
                    except IndexError:
                        cover = ''

                    total_dict[record_id] = {
                        'Title': title,
                        'Artists': artists,
                        'Cover': cover,
                        'Count': 1
                    }
                else:
                    total_dict[record_id]['Count'] += 1

            url = response['next']
        return total_dict

    def songs_wrapper(self):
        with open(self.playlists_dir, 'r') as f:
            playlists = json.load(f)

            total_dict = {}
            i, i_max = 1, len(playlists)
            for playlist in playlists:
                print('{}/{}:'.format(i, i_max), playlist['name'])
                total_dict = self.get_songs(total_dict, playlist['href'])
                i += 1

        with open(self.songs_dir, 'w') as f:
            json.dump(total_dict, f)

    def ranker(self):
        with open(self.songs_dir, 'r') as f:
            songs = json.load(f)

            ranked = []
            for s in songs.keys():
                song = songs[s]
                ranked.append((
                    song['Count'],
                    song['Title'],
                    song['Artists'],
                    # song['Cover']
                ))

        ranked.sort(key=lambda tup: tup[0], reverse=True)
        with open(self.ranked_dir, 'w') as f:
            for r in ranked:
                f.write('Count: {} - Title: {} - Artists: {}\n'.format(r[0], r[1], r[2]))

    def run(self):
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        self.get_playlists()
        self.songs_wrapper()
        self.ranker()
