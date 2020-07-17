class Object:
	def __init__(self, x, y, width, height, color):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.corners = [(x,y), (x+width,y), (x+width, y+height), (x, y+height)]
		self.color = color
		self.is_solid = True
	
	def get_corners(self):
		return [(self.x, self.y), (self.x+self.width, self.y), (self.x+self.width, self.y+self.height), (self.x, self.y+self.height)]
	
	def is_point_inside(self, x, y):
		return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
	
	def collides(self, other):
		if any(self.is_point_inside(*corner) for corner in other.get_corners()):
			return True
		if any(other.is_point_inside(*corner) for corner in self.get_corners()):
			return True
		return False

class Wall(Object):
	def __init__(self, x, y, width, height):
		super().__init__(x, y, width, height, (0,0,0))

class Button(Object):
	def __init__(self, x, y, width, height, id):
		super().__init__(x, y, width, height, (128,128,128))
		self.id = id
		self.is_pushed = False
		self.is_solid = False
	
	def push(self):
		self.is_pushed = True
		self.color = (0,255,0)
	
	def release(self):
		self.is_pushed = False
		self.color = (128,128,128)

class Door(Object):
	def __init__(self, x, y, width, height, id):
		super().__init__(x, y, width, height, (128,128,128))
		self.id = id
		self.is_solid = True
	
	def open(self):
		self.is_solid = False
		self.color = (192,192,192)
		
	def close(self):
		self.is_solid = True
		self.color = (128,128,128)

class Player(Object):
	def __init__(self, x, y, size, speed, color):
		super().__init__(x, y, size, size, color)
		self.size = size
		self.speed = speed
		self.is_solid = False
	
	def move(self, dir):
		if dir == "up":
			self.y -= self.speed
		if dir == "right":
			self.x += self.speed
		if dir == "down":
			self.y += self.speed
		if dir == "left":
			self.x -= self.speed

class Model:
	def __init__(self):
		self.width = 500
		self.height = 500
		self.block_size = 10
		self.p0 = Player(10,10, 10, .5, (255,0,0))
		self.p1 = Player(100,100, 10, .5, (0,0,255))
		self.players = [self.p0, self.p1]
		self.init()
	
	def init(self):
		self.walls = []
		self.buttons = []
		self.doors = []
	
	def load_map(self, mtx):
		self.init()
		for i, line in enumerate(mtx):
			for j, elem in enumerate(line):
				code = elem[0]
				try:
					id = int(elem[1:])
				except:
					pass
				
				if code == 'N':
					pass
				if code == 'W':
					self.add_wall(i*self.block_size, j*self.block_size, self.block_size, self.block_size)
				if code == 'B':
					self.add_button(i*self.block_size, j*self.block_size, self.block_size, self.block_size, id)
				if code == 'D':
					self.add_door(i*self.block_size, j*self.block_size, self.block_size, self.block_size, id) #@todo nem 1, hanem máshogy kell reprezentálni
	
	def add_wall(self, x, y, width, height):
		self.walls.append(Wall(x, y, width, height))
		
	def add_button(self, x, y, width, height, id=None):
		if id is None:
			id = max(self.buttons, key=lambda b:b.id) if self.buttons else 0
		self.buttons.append(Button(x, y, width, height, id))
	
	def add_door(self, x, y, width, height, id=None):
		if id is None:
			id = max(self.doors, key=lambda b:b.id) if self.doors else 0
		self.doors.append(Door(x, y, width, height, id))
	
	def get_objects(self):
		return self.buttons + self.doors + self.players + self.walls
	
	def move_player(self, player_code, dir):
		player = self.players[player_code]
		old_pos = player.x, player.y
		player.move(dir)
		
		#ha nem ütközik fallal
		if not any(player.collides(o) for o in self.get_objects() if o.is_solid):
			pass
		else:
			player.x, player.y = old_pos
		
		self.update_buttons()
		self.update_doors()
	
	def update_buttons(self):
		for button in self.buttons:
			if any(player.collides(button) for player in self.players):
				button.push()
			else:
				button.release()
	
	def update_doors(self):
		for door in self.doors:
			for button in filter(lambda x:x.id == door.id, self.buttons):
				if button.is_pushed:
					door.open()
					break
			else:
				door.close()











