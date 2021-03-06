# https://pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
# import the necessary packages
import datetime
class FPS:
	def __init__(self, step=60, id=''):
		# store the start time, end time, and total number of frames
		# that were examined between the start and end intervals
		self._start = None
		self._end = None
		self._numFrames = 0
		self.step = step
		self.id = id
	def start(self):
		# start the timer
		self._start = datetime.datetime.now()
		self._numFrames = 0
		return self
	def stop(self):
		# stop the timer
		self._end = datetime.datetime.now()
	def update(self):
		# increment the total number of frames examined during the
		# start and end intervals
		self._numFrames += 1

		if (self._numFrames % self.step) == 0:
			self.stop()
			print(str(self.id) + '\tFPS: ' + str(self.fps()))
			self.start()

	def elapsed(self):
		# return the total number of seconds between the start and
		# end interval
		return (self._end - self._start).total_seconds() + (1/1000)
	def fps(self):
		# compute the (approximate) frames per second
		return self._numFrames / self.elapsed()
