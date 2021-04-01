
from sense_hat import SenseHat


class Sensors:

	sense = SenseHat()
	w = [150, 150, 150]
	r = [255, 0, 0] # high power, 3 pts
	g = [0, 255, 0] # low power, 1 pts
	b = [0, 0, 255] # mid power, 2 pts
	e = [0, 0, 0]
	
	def __init__(self):
		pass


	def getTemp(self):
		temp = self.sense.get_temperature()
		return temp

	def getHumidity(self):
		hum = self.sense.get_humidity()
		return hum

	def setPowerLevel(self, level):
		if level == b"high":
			r = self.r
			e = self.e

			highImage = [
			e, r, e, e, e, e, r, e,
			e, r, e, e, e, e, r, e,
			e, r, e, e, e, e, r, e,
			e, r, r, r, r, r, r, e,
			e, r, e, e, e, e, r, e,
			e, r, e, e, e, e, r, e,
			e, r, e, e, e, e, r, e,
			e, r, e, e, e, e, r, e
			]
			self.sense.set_pixels(highImage)
		if level == b"medium":
			b = self.b
			e= self.e
			mediumImage = [
			b, e, e, e, e, e, b, e,
			b, b, e, e, e, b, b, e,
			b, e, b, e, b, e, b, e,
			b, e, b, e, b, e, b, e,
			b, e, b, e, b, e, b, e,
			b, e, e, b, e, e, b, e,
			b, e, e, e, e, e, b, e,
			b, e, e, e, e, e, b, e
			]
			self.sense.set_pixels(mediumImage)

		if level == b"low":
			g = self.g
			e = self.e
			lowImage = [
			e, g, e, e, e, e, e, e,
			e, g, e, e, e, e, e, e,
			e, g, e, e, e, e, e, e,
			e, g, e, e, e, e, e, e,
			e, g, e, e, e, e, e, e,
			e, g, e, e, e, e, e, e,
			e, g, e, e, e, e, e, e,
			e, g, g, g, g, g, g, e
			]
			self.sense.set_pixels(lowImage)
			#self.sense.clear()

if "__main__" == __name__:
	sensors = Sensors()
	sensors.setPowerLevel("low")
	print(sensors.getTemp())
	print(sensors.getHumidity())




