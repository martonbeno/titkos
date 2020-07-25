from Activator import *

class Switch(Activator):
	def __init__(self, x, y, width, height, id=None):
		super().__init__(x, y, width, height, id, (0,255,0), (170,170,170))
		self.is_solid = False
		
	def toggle(self):
		if self.is_active:
			self.deactivate()
		else:
			self.activate()