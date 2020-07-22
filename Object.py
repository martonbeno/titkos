class Object:
	def __init__(self, x, y, width, height, color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.corners = [(x,y), (x+width,y), (x+width, y+height), (x, y+height)]
		self.color = color
		self.is_solid = True
		self.is_killer = False
	
	def get_corners(self):
		return [(self.x, self.y), (self.x+self.width-1, self.y), (self.x+self.width-1, self.y+self.height-1), (self.x, self.y+self.height-1)]
	
	def is_point_inside(self, x, y):
		return self.x < x < self.x + self.width and self.y < y < self.y + self.height
	
	def collides(self, other):
		if any(self.is_point_inside(*corner) for corner in other.get_corners()):
			return True
		if any(other.is_point_inside(*corner) for corner in self.get_corners()):
			return True
		return False