from tracks import search_tracks, get_tracks, Source, dump, add_to_playlist, get_tracks_uris, chunks, NOT_MATCHED_FILE, MATCHED_FILE, TRACKS_FILE

playlist = '5Ob7com0xkQNXt48HcTPmO'
source = Source.FILE

######## RETRIEVING TRACKS FROM PLAYLIST
print('Retrieving tracks from {}'.format(source))
tracks = get_tracks(source, NOT_MATCHED_FILE)

print('Saving tracks file')
dump(tracks, TRACKS_FILE)



######## MATCHING TRACKS WITH SPOTIFY 
print('Matching tracks')
matched, not_mached = search_tracks(tracks)
# matched = get_tracks(source, NOT_MATCHED_FILE)
# not_mached = get_tracks(source, NOT_MATCHED_FILE)

print('Saving matched tracks file')
dump(matched, MATCHED_FILE)

print('Saving NOT matched tracks file')
dump(not_mached, NOT_MATCHED_FILE)



######## ADDING MATCHES TO PLAYLIST
print('Generate list of tracks uris chunked by 100')
chuncked_tracks_uris = chunks(get_tracks_uris(matched), 100)

for tracks_uris in chuncked_tracks_uris:
    print('Adding {} tracks to playlist {}'.format(len(tracks_uris), playlist))
    if add_to_playlist(playlist, tracks_uris):
        print('Success!')
    else:  
        print('Failed!')