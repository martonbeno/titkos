from Object import *

class Activator(Object):
	def __init__(self, x, y, width, height, id, activated_color, deactivated_color):
		super().__init__(x, y, width, height, deactivated_color)
		self.is_active = False
		self.activatables = []
		self.id = id
		self.activated_color = activated_color
		self.deactivated_color = deactivated_color
		
	def activate(self):
		self.is_active = True
		self.color = self.activated_color
	
	def deactivate(self):
		self.is_active = False
		self.color = self.deactivated_color
		
	def add_activatable(self, activatable):
		self.activatables.append(activatable)
		activatable.activators.append(self)