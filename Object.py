from Rectangle import *

class Object(Rectangle):
	def __init__(self, x, y, width, height, color):
		super().__init__(x, y, width, height, color)
		self.is_solid = True
		self.is_killer = False