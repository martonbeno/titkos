from Object import *
from Field_of_view import *

class Player(Object):
	def __init__(self, x, y, size, speed, color, id):
		super().__init__(x, y, size, size, color)
		self.start_x = x
		self.start_y = y
		self.size = size
		self.speed = speed
		self.is_solid = False
		self.id = id
		self.switches = []
		self.numb = False
		self.field_of_view = Field_of_view(200, 200, self)
	
	def move(self, dir, v=None):
		if self.numb:
			return
		if v==None:
			v = self.speed
		if dir == "up":
			self.y -= v
		if dir == "right":
			self.x += v
		if dir == "down":
			self.y += v
		if dir == "left":
			self.x -= v
		self.field_of_view.update_coordinates()
	
	def kill(self):
		self.x = self.start_x
		self.y = self.start_y
		
	def use(self):
		for sw in self.switches:
			sw.toggle()