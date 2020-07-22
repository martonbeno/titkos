from Object import *

class Button(Object):
	def __init__(self, x, y, width, height, id=None):
		super().__init__(x, y, width, height, (128,128,128))
		self.id = id
		self.is_pushed = False
		self.is_solid = False
		self.released_color = self.color
		self.pushed_color = (0,255,0)
	
	def push(self):
		self.is_pushed = True
		self.color = self.pushed_color
	
	def release(self):
		self.is_pushed = False
		self.color = self.released_color