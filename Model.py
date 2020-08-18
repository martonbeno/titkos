from Object import *
from Door import *
from Goal import *
from Player import *
from Button import *
from Wall import *
from Portal import *
from Switch import *

class Model:
	def __init__(self):
		self.width = 500
		self.height = 500
		self.block_size = 10
		self.p0 = Player(50,10, 10, 1, (255,0,0), 0)
		self.p1 = Player(50,50, 10, 1, (0,0,255), 1)
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
		self.switches = []
		self.doors = []
		self.goals = []
		self.portals = []
		self.activators = []
		self.activatables = []
	
	def get_field_of_view_objects(self, player_id):
		return self.players[player_id].field_of_view.get_objects(self.get_objects())
	
	def load_map(self, d_list):
		self.init()
		for d in d_list:
			field = d['field']
			code = field[0]
			try:
				id = int(field[1:])
			except:
				pass
			
			x = d['x'] * self.block_size
			y = d['y'] * self.block_size
			width = d['width'] * self.block_size
			height = d['height'] * self.block_size
			
			if code == 'N':
				pass
			if code == 'W':
				self.add_wall(x, y, width, height)
			if code == 'B':
				self.add_button(x, y, width, height, id)
			if code == 'S':
				self.players[id].x = self.players[id].start_x = x
				self.players[id].y = self.players[id].start_y = y
			if code == 'G':
				self.add_goal(x, y, width, height, id)
			if code == 'P':
				self.add_passable_wall(x, y, width, height, id)
			if code == 'K':
				self.add_killer_wall(x, y, width, height)
			if code == 'O':
				self.add_switch(x, y, width, height, id)
		
		for d in d_list:
			field = d['field']
			code = field[0]
			try:
				id = int(field[1:])
			except:
				pass
			
			x = d['x'] * self.block_size
			y = d['y'] * self.block_size
			width = d['width'] * self.block_size
			height = d['height'] * self.block_size
			
			if code == 'D':
				self.add_door(x, y, width, height, id)
	
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
		
	def add_button(self, x, y, width, height, id):
		button = Button(x, y, width, height, id)
		self.buttons.append(button)
		self.activators.append(button)
		
	def add_switch(self, x, y, width, height, id):
		switch = Switch(x, y, width, height, id)
		self.switches.append(switch)
		self.activators.append(switch)
	
	def add_door(self, x, y, width, height, id):
		door = Door(x, y, width, height)
		self.doors.append(door)
		self.activatables.append(door)
		for ac in self.activators:
			if ac.id == id:
				ac.add_activatable(door)
	
	def add_goal(self, x, y, width, height, player_id):
		self.goals.append(Goal(x, y, width, height, self.players[player_id]))
		
	def add_portal(self, x, y, width, height, id):
		self.portals.append(Portal(x, y, width, height, id))
	
	def get_objects(self):
		return self.goals + self.buttons + self.doors + self.walls + self.killer_walls + self.portals + self.switches + self.players
	
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
			
		for portal in self.portals:
			if player.collides(portal) and portal.is_active:
				for portal2 in self.portals:
					if portal2.id == portal.id and portal2 != portal:
						player.x = portal2.x
						player.y = portal2.y
						portal2.is_active = False
						
		self.update_buttons()
		self.update_portals()
		self.update_activatables()
	
	def use_player(self, player_id):
		self.update_switches(self.players[player_id])
		self.players[player_id].use()
		self.update_activatables()
	
	def kill_players(self):
		for player in self.players:
			player.kill()
	
	def update_buttons(self):
		for button in self.buttons:
			if any(player.collides(button) for player in self.players):
				button.activate()
			else:
				button.deactivate()
		
		for goal in self.goals:
			if goal.player.collides(goal):
				goal.activate()
			else:
				goal.deactivate()

	def update_switches(self, player):
		player.switches.clear()
		for switch in self.switches:
			if player.collides(switch):
				player.switches.append(switch)
		
	def update_portals(self):
		for portal in self.portals:
			if not any(player.collides(portal) for player in self.players):
				portal.is_active = True
				
	def update_activatables(self):
		for ac in self.activatables:
			ac.refresh_state()
	
	def is_winning(self):
		for player in self.players:
			for goal in filter(lambda x:x.player == player, self.goals):
				if goal.is_pushed:
					break
			else:
				return False
		return True









