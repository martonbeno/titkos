from Object import *

class Activatable(Object):
	def __init__(self, x, y, width, height, color):
		super().__init__(x, y, width, height, color)
		self.activators = []
		
	def refresh_state(self):
		if any(ac.is_active	for ac in self.activators):
			self.activate()
		else:
			self.deactivate()
		
	def activate(self):
		pass
		
	def deactivate(self):
		pass