import requests
import requests_cache
import json
from lxml import html

def get_song_file(file_url):
	temp_file = "gd_temp_file.ogg"

	r = requests.get(file_url, stream=True)
	if r.status_code == 200:
		with open(temp_file, 'wb') as fd:
			for chunk in r.iter_content(chunk_size=128):
				fd.write(chunk)

		return SongDecoder(temp_file)

	print("Request failed with status code: %s" % r.status_code)

def get_song_links(concert_url):
	print("Requesting resource at: %s" % concert_url)
	r = requests.get(concert_url)
	if r.status_code == 200:
		etree = html.fromstring(r.text)
		recording_tags = etree.findall('.//div[@itemtype=\'http://schema.org/MusicRecording\']')
		concert_identifier = concert_url.split('/')[-1].split('.')[0]

		print("Parsing track data")

		return (
			{
				'concert_identifier': concert_identifier,
				'track_number': i + 1,
				'track_name': recording_tag.find('.//meta[@itemprop=\'name\']').attrib['content'],
				'track_urls': {
					'mp3': next((track_url for track_url in _track_urls(recording_tag) if '.mp3' in track_url), ['']),
					'ogg': next((track_url for track_url in _track_urls(recording_tag) if '.ogg' in track_url), [''])
				}
			} for i, recording_tag in enumerate(recording_tags)
		)

		print("Couldn't find any script tags with song data.")
	print("Request failed with status code: %s" % r.status_code)
	return ()

def download_song_files(files_generator):
	removed_characters = '/'
	translation_table = dict.fromkeys(map(ord, removed_characters), None)

	for file_data in files_generator:
		print('downloading %s' % file_data['track_name'])
		file_url = file_data['track_urls']['ogg']
		local_file_name = "data/%s-%s.%s" % (
			file_data['concert_identifier'],
			'-'.join(file_data['track_name'].translate(translation_table).split(' ')),
			'ogg'
		)
		print('saving to %s' % local_file_name)

		r = requests.get(file_url, stream=True)
		if r.status_code == 200:
			with open(local_file_name, 'wb') as fd:
				for chunk in r.iter_content(chunk_size=128):
					fd.write(chunk)


def _track_urls(recording_tag):
	return (
		media_link.attrib['href']
		for media_link in recording_tag.findall('.//link[@itemprop=\'associatedMedia\']')
	)

if (__name__ == '__main__'):
	concert_urls = [
		'https://archive.org/details/gd73-02-15.sbd.hall.1580.sbeok.shnf/gd73-02-15d1t02.shn',
		'https://archive.org/details/gd73-02-15.sbd.hall.1580.sbeok.shnf',
		'https://archive.org/details/gd87-04-03.sennme80.clark-miller.24898.sbeok.shnf',
		'https://archive.org/details/gd77-05-08.sbd.hicks.4982.sbeok.shnf',
		'https://archive.org/details/gd77-05-07.sbd.eaton.wizard.26085.sbeok.shnf',
		'https://archive.org/details/gd1977-05-08.shure57.stevenson.29303.flac16',
		'https://archive.org/details/gd77-02-26.sbd.alphadog.9752.sbeok.shnf',
		'https://archive.org/details/gd77-05-08.maizner.hicks.5002.sbeok.shnf',
		'https://archive.org/details/gd70-05-15.early-late.sbd.97.sbeok.shnf',
		'https://archive.org/details/gd71-08-06.aud.bertrando.yerys.129.sbeok.shnf',
	]

	for concert_url in concert_urls:
		song_link_data = get_song_links(concert_url)
		download_song_files(song_link_data)

	# print(song_link_data)

	# for song_datum in song_link_data:
	# 	song_url = song_datum['track_urls']['ogg']
	# 	decoded_song_file = get_song_file(song_url)

	# 	# Generator of song chunks 10 seconds long.
	# 	song_chunks = decoded_song_file.get_song_chunks()

	# 	for song_chunk in song_chunks:
	# 		input_data = song_chunk[:-1]
	# 		output_data = song_chunk[-1]





