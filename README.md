# SpotiTag
 
Ranking songs on Spotify for a given word.

---

If it was possible to tag songs on Spotify (like hashtags on Instagram and Twitter), it would be interesting to know for each tag which songs are the highest in the world.

This tool will:
1. take a search key (tag) as input
2. get the top 1000 playlists on Spotify for that tag
3. rank all songs based on their presence in each playlist

---

To run this tool, you'll need to have an OAuth token from Spotify.
To get one, you should:
1. Go to [this link](https://developer.spotify.com/console/get-playlist-tracks/) on _Spotify for Developers_
2. Select `GET TOKEN` > `playlist-read-private` > `REQUEST TOKEN`
3. Copy your token from the `OAuth Token` field

---

### Sample outputs:
> Since the results can vary based on time, the output directory contains the date of the run.

#### Love
1. All of Me - Artists: ['John Legend']
2. Say You Won't Let Go - Artists: ['James Arthur']
3. Perfect - Artists: ['Ed Sheeran']

#### Gym
1. 'Till I Collapse - Artists: ['Eminem', 'Nate Dogg']
2. Legend - Artists: ['Tevvez']
3. FEEL NOTHING - Artists: ['The Plot In You']

#### Break Up
1. traitor - Artists: ['Olivia Rodrigo']
2. drivers license - Artists: ['Olivia Rodrigo']
3. you broke me first - Artists: ['Tate McRae']