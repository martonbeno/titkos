from Object import *

class Door(Object):
	def __init__(self, x, y, width, height, id):
		super().__init__(x, y, width, height, (128,128,128))
		self.id = id
		self.is_solid = True
	
	def open(self):
		self.is_solid = False
		self.color = (192,192,192)
		
	def close(self):
		self.is_solid = True
		self.color = (128,128,128)