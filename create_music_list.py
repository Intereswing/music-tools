import os
import mutagen

player_abs_path = 'a:\\'

output_path = 'F:\\playlist_data'
if not os.path.exists(output_path):
    os.mkdir(output_path)

resource_path = 'F:\\'
if not os.path.exists(resource_path):
    os.mkdir(resource_path)
songs = os.listdir(resource_path)
albums = {}


for song_name in songs:
    # Pass directory.
    if '.' not in song_name:
        continue

    song_path = os.path.join(resource_path, song_name)
    song = mutagen.File(song_path)

    # Get track number and album name of the song.
    if song_name.split('.')[-1] == 'mp3':
        track_number = int(song['TRCK'].text[0])
        album = song['TALB'].text[0]
    elif song_name.split('.')[-1] == 'flac':
        track_number = int(song['tracknumber'][0])
        album = song['album'][0]
    else:
        raise RuntimeError('Unknown song format')

    if album not in albums:
        albums[album] = []
    albums[album].append([song_name, track_number])

# Write .m3u playlist to output_path.
for album in albums:
    albums[album] = sorted(albums[album], key=lambda x: x[1])
    with open(os.path.join(output_path, album + '.m3u'), 'w') as file:
        for track in albums[album]:
            file.write(player_abs_path + track[0] + '\n')
