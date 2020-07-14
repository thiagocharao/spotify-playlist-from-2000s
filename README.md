# spotify-playlist-from-2000s

## Context
It was early 2000s when I started downoading songs (of course I bought them all), years passed until Spotify showed up. I started using it and there was a pretty cool feature to import all my local library, so I did, at first I thought it would do a match to their own library, turns out it did not. I had to change PC and all my beloved songs were gone, except for the playlist I created which I called "All my songs", it stayed there for years now with 7,534 songs METADATA with no use at all! 

## Problem
How do I make Spotify read this metadata and Match them into actual tracks on their collection so I can enjoy them again? :D

## Solution
1. Get the list of tracks from this dead playlist
2. Get what interests me (Track name, artist and album)
3. THE FUN PART - Match them all (most of them)
    - Run a query to find candidates based on the Track Name
    - Get ratio result between candidate's track name and my playlist track's name
    - Do the same for the artist's name
    - Get the average of them two any ratio average above 0.3 is a good enough match because lot's of my songes did not have Artist field populated but they were present on the tracks name
    - Get candidate's track popularity
    - Store the highest score
    - Move to b until all candidates are scored, the one with the highest score wins as a **MATCH** :D 
4. Store the Matched ones and the ones I could not match :(
5. Get a list of spotify URI for each match eg: spotify:track:0pqnGHJpmpxLKifKRmU6WP
6. create chunks of 100s due to the APIs limit
7. POST them to my brand new playlist :D

## Results
My new playlist: https://open.spotify.com/playlist/5Ob7com0xkQNXt48HcTPmO?si=5QgYcOq-RlqawD3OLqGWCQ

Dead playlist: https://open.spotify.com/playlist/0UKmQJJmXskgC40T4gaFtm?si=yl4f1ioMS_aQG-kMHhAAEA

From **7534** tracks
- **6689** tracks matched
- **845** tracks not matched

As for the not matches I still have some faith that doing some teaks on the code I can find some more matches :D

## NOTES
I also thought of using SequenceMatcher from difflib that uses Ratcliff/Obershelp algorithm which computes the doubled number of matching characters divided by the total number of characters in the two strings.

But the results were good so I did not give it a try.
