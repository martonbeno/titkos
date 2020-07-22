from Button import *

class Goal(Button):
	def __init__(self, x, y, width, height, player):
		super().__init__(x, y, width, height, )
		self.player = player
		self.color = player.color
		self.released_color = player.color
		self.pushed_color = player.color