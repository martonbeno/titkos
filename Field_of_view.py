from Rectangle import *

class Field_of_view(Rectangle):
	def __init__(self, width, height, player):
		self.width = width
		self.height = height
		self.player = player
		self.update_coordinates()
	
	def update_coordinates(self):
		center_x, center_y = self.player.get_center_point()
		self.x = center_x - self.width//2
		self.y = center_y - self.height//2
	
	def get_objects(self, objects, with_frame=False):
		# visible_objets = [self.intersect(o) for o in objects if self.collides(o)]
		visible_objets = []
		for o in objects:
			intersection = self.intersect(o)
			if intersection is not None:
				visible_objets.append(intersection)
		
		if with_frame:
			margin = 5
			visible_objets.append(Rectangle(self.x, self.y, self.width, margin, (0,0,0)))
			visible_objets.append(Rectangle(self.x+self.width-margin, self.y, margin, self.height, (0,0,0)))
			visible_objets.append(Rectangle(self.x, self.y+self.height-margin, self.width, margin, (0,0,0)))
			visible_objets.append(Rectangle(self.x, self.y, margin, self.height, (0,0,0)))
		
		return visible_objets
	
	def intersect(self, other):
		if self.contains(other):
			return other
		if not self.collides(other):
			return None
		
		self.update_coordinates()
		
		left = max(self.x, other.x)
		right = min(self.x+self.width, other.x+other.width)
		top = max(self.y, other.y)
		bottom = min(self.y+self.height, other.y+other.height)
		
		return Rectangle(left-self.x, top-self.y, right-left, bottom-top, other.color)





















