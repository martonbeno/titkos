from Object import *

class Portal(Object):
	def __init__(self, x, y, width, height, id=None):
		super().__init__(x, y, width, height, (150, 0, 255))
		self.id = id
		self.is_active = True
		self.is_solid = False
