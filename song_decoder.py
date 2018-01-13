from pydub import AudioSegment

class SongDecoder:
	def __init__(self, song_file):
		self.song_data = AudioSegment.from_ogg(song_file)

	def get_byte_array(self, start_time=0, seconds=10):
		return bytearray(self.song_data[start_time:seconds*1000].raw_data)

	def get_song_chunks(self, seconds=10):
		start_times = int((len(self.song_data) / 1000) - seconds)

		return (
			self.get_byte_array(start_time=start, seconds=seconds)
			for start in range(start_times)
		)
