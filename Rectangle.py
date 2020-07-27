class Rectangle:
	def __init__(self, x, y, width, height, color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color
	
	def __str__(self):
		return f"{type(self)}:\tx={self.x}\ty={self.y}\twidth={self.width}\theight={self.height}\tcolor={self.color}"
	
	def get_center_point(self):
		return self.x+self.width//2, self.y+self.height//2
	
	#order: top right, top left, bottom left, bottom right
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
	
	def contains(self, other):
		return all(self.is_point_inside(*corner) for corner in self.get_corners())
		




















