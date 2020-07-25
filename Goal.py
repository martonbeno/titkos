from Button import *

class Goal(Button):
	def __init__(self, x, y, width, height, player):
		super().__init__(x, y, width, height, player.id)
		self.player = player
		self.color = player.color
		self.activated_color = player.color
		self.deactivated_color = player.color