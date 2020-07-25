from Activatable import *

class Door(Activatable):
	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height, (128,128,128))
		self.is_solid = True
	
	def activate(self):
		self.is_solid = False
		self.color = (192,192,192)
		
	def deactivate(self):
		self.is_solid = True
		self.color = (128,128,128)