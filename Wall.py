from Object import *

class Wall(Object):
	def __init__(self, x, y, width, height, color=(0,0,0), is_killer=False, pass_id=None): #pass_ids: ezek a játékosok át tudnak menni rajta
		super().__init__(x, y, width, height, color)
		self.is_killer = is_killer
		self.is_solid = not is_killer
		if is_killer:
			self.color = (200, 100, 0)
		self.pass_id = pass_id