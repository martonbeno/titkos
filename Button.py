from Activator import *

class Button(Activator):
	def __init__(self, x, y, width, height, id=None):
		super().__init__(x, y, width, height, id, (0,255,0), (128,128,128))
		self.is_solid = False