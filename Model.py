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
	def __init__(self, x, y, width, height, color=(0,0,0), is_killer=False, pass_id=None): #pass_ids: ezek a játékosok át tudnak menni rajta
		super().__init__(x, y, width, height, color)
		self.is_killer = is_killer
		self.is_solid = not is_killer
		if is_killer:
			self.color = (200, 100, 0)
		self.pass_id = pass_id

class Button(Object):
	def __init__(self, x, y, width, height, id=None):
		super().__init__(x, y, width, height, (128,128,128))
		self.id = id
		self.is_pushed = False
		self.is_solid = False
		self.released_color = self.color
		self.pushed_color = (0,255,0)
	
	def push(self):
		self.is_pushed = True
		self.color = self.pushed_color
	
	def release(self):
		self.is_pushed = False
		self.color = self.released_color

class Goal(Button):
	def __init__(self, x, y, width, height, player):
		super().__init__(x, y, width, height, )
		self.player = player
		self.color = player.color
		self.released_color = player.color
		self.pushed_color = player.color

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
		self.start_x = x
		self.start_y = y
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
	
	def kill(self):
		self.x = self.start_x
		self.y = self.start_y

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
		w1 = Wall(0, -10, self.width, 10)
		w2 = Wall(self.width, 0, 10, self.height)
		w3 = Wall(0, self.height, self.width, 10)
		w4 = Wall(-10, 0, 10, self.height)
		self.walls = [w1, w2, w3, w4]
		self.killer_walls = []
		self.buttons = []
		self.doors = []
		self.goals = []
	
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
				if code == 'S':
					self.players[id].x = self.players[id].start_x = i*self.block_size
					self.players[id].y = self.players[id].start_y = j*self.block_size
				if code == 'G':
					self.add_goal(i*self.block_size, j*self.block_size, self.block_size, self.block_size, id)
				if code == 'P':
					self.add_passable_wall(i*self.block_size, j*self.block_size, self.block_size, self.block_size, id)
				if code == 'K':
					self.add_killer_wall(i*self.block_size, j*self.block_size, self.block_size, self.block_size)
	
	def add_wall(self, x, y, width, height):
		self.walls.append(Wall(x, y, width, height))
	
	def add_passable_wall(self, x, y, width, height, pass_id):
		if pass_id == 0:
			color = (255, 170, 170)
		elif pass_id == 1:
			color = (170, 170, 255)
		self.walls.append(Wall(x, y, width, height, color, pass_id=pass_id))
	
	def add_killer_wall(self, x, y, width, height):
		self.killer_walls.append(Wall(x, y, width, height, is_killer=True))
		
	def add_button(self, x, y, width, height, id=None):
		if id is None:
			id = max(self.buttons, key=lambda b:b.id) if self.buttons else 0
		self.buttons.append(Button(x, y, width, height, id))
	
	def add_door(self, x, y, width, height, id=None):
		if id is None:
			id = max(self.doors, key=lambda b:b.id) if self.doors else 0
		self.doors.append(Door(x, y, width, height, id))
	
	def add_goal(self, x, y, width, height, player_id):
		self.goals.append(Goal(x, y, width, height, self.players[player_id]))
	
	def get_objects(self):
		return self.goals + self.buttons + self.doors + self.walls + self.killer_walls + self.players
	
	def move_player(self, player_id, dir):
		player = self.players[player_id]
		old_pos = player.x, player.y
		player.move(dir)
		
		can_move = True
		for o in filter(lambda x:player.collides(x), self.get_objects()):
			if isinstance(o, Wall) and o.is_solid and player_id != o.pass_id:
				can_move = False
				break
			elif not isinstance(o, Wall) and o.is_solid:
				can_move = False
				break
		
		if not can_move:
			player.x, player.y = old_pos
		
		#ha ütközik killer wall-lal
		if any(player.collides(wall) for wall in self.killer_walls):
			self.kill_players()
		
		self.update_buttons()
		self.update_doors()
	
	def kill_players(self):
		for player in self.players:
			player.kill()
	
	def update_buttons(self):
		for button in self.buttons:
			if any(player.collides(button) for player in self.players):
				button.push()
			else:
				button.release()
		
		for goal in self.goals:
			if goal.player.collides(goal):
				goal.push()
			else:
				goal.release()
	
	def update_doors(self):
		for door in self.doors:
			for button in filter(lambda x:x.id == door.id, self.buttons):
				if button.is_pushed:
					door.open()
					break
			else:
				door.close()
	
	def is_winning(self):
		for player in self.players:
			for goal in filter(lambda x:x.player == player, self.goals):
				if goal.is_pushed:
					break
			else:
				return False
		return True









