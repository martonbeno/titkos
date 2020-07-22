import tkinter as tk
from tkinter.filedialog import askopenfilename
import re
from Persistence import *

def color(code):
	letter = code[0]
	if len(code) > 1:
		number = code[1:]
	
		if letter == 'S':
			if number == '0':
				return "red"
			if number == '1':
				return "blue"
		if letter == 'P':
			if number == '0':
				return "indian red"
			if number == '1':
				return "steel blue"
		if letter == 'G':
			if number == '0':
				return "red4"
			if number == '1':
				return "blue4"
	
	color = {	'N':"white",
				'W':"black",
				'B':"green",
				'D':"gray",
				'K':"orange"
			}
	return color[letter]

class Mapeditor:
	def __init__(self):
		cell_size = 10
		toolkit_size = 50

		width = 50
		height = 50
		self.mtx = [[0 for _ in range(50)] for _ in range(50)]
		self.active = 'N'


		root = tk.Tk()
		root.geometry("1000x600")
		toolkit = tk.Frame(master=root, width=cell_size*width, height=toolkit_size, bg="gray")
		
		nothing_button = tk.Button(master=toolkit, text="nothing", command=lambda:self.set_active('N'))
		
		self.spawn_id = tk.StringVar()
		self.spawn_id.set('0')
		spawn_button = tk.Button(master=toolkit, text="spawn", command=lambda:self.set_active('S'))
		spawn_id_field = tk.Entry(master=toolkit, textvariable=self.spawn_id)
		
		wall_button = tk.Button(master=toolkit, text="wall", command=lambda:self.set_active('W'))
		
		killer_wall_button = tk.Button(master=toolkit, text="killer_wall", command=lambda:self.set_active('K'))
		
		self.passable_wall_id = tk.StringVar()
		self.passable_wall_id.set('0')
		passable_wall_button = tk.Button(master=toolkit, text="passable wall", command=lambda:self.set_active('P'))
		passable_wall_id_field = tk.Entry(master=toolkit, textvariable=self.passable_wall_id)
		
		self.button_id = tk.StringVar()
		self.button_id.set('1')
		button_button = tk.Button(master=toolkit, text="button", command=lambda:self.set_active('B'))
		button_id_field = tk.Entry(master=toolkit, textvariable=self.button_id)
		
		self.door_id = tk.StringVar()
		self.door_id.set('1')
		door_button = tk.Button(master=toolkit, text="door", command=lambda:self.set_active('D'))
		door_id_field = tk.Entry(master=toolkit, textvariable=self.door_id)
		
		self.goal_id = tk.StringVar()
		self.goal_id.set('0')
		goal_button = tk.Button(master=toolkit, text="goal", command=lambda:self.set_active('G'))
		goal_id_field = tk.Entry(master=toolkit, textvariable=self.goal_id)
		
		
		undo_button = tk.Button(master=toolkit, text="undo", command=self.undo)
		
		self.export_filename = tk.StringVar()
		export_button = tk.Button(master=toolkit, text="export", command=self.export)
		export_field = tk.Entry(master=toolkit, textvariable=self.export_filename)
		
		load_button = tk.Button(master=toolkit, text="import", command=lambda:self.load(askopenfilename()))
		
		debug_button = tk.Button(master=toolkit, text="debug", command=self.debug)
		
		
		
		
		
		nothing_button.grid(column=0, row=0)
		
		spawn_button.grid(column=0, row=1)
		spawn_id_field.grid(column=1, row=1)
		
		wall_button.grid(column=0, row=2)
		
		killer_wall_button.grid(column=1, row=2)
		
		passable_wall_button.grid(column=0, row=3)
		passable_wall_id_field.grid(column=1, row=3)
		
		button_button.grid(column=0, row=4)
		button_id_field.grid(column=1, row=4)
		
		door_button.grid(column=0, row=5)
		door_id_field.grid(column=1, row=5)
		
		goal_button.grid(column=0, row=6)
		goal_id_field.grid(column=1, row=6)
		
		undo_button.grid(column=0, row=10)
		
		export_button.grid(column=0, row=11)
		export_field.grid(column=1, row=11)
		
		load_button.grid(column=0, row=12)
		
		
		debug_button.grid(column=0, row=13)
		


		self.canvas = tk.Canvas(master=root, width=cell_size*width, height=cell_size*height)
		canvas = self.canvas

		for i in range(width):
			canvas.create_line(i*cell_size, 0, i*cell_size, height*cell_size)
		for i in range(height):
			canvas.create_line(0, i*cell_size, width*cell_size, i*cell_size)
		
		canvas.bind("<Button-1>", lambda e:self.mouse_down(e))
		canvas.bind("<ButtonRelease-1>", lambda e:self.mouse_up(e))
		canvas.bind("<Motion>", lambda e: self.mouse_move(e))
		
		
		self.cell_size = cell_size
		self.width = width
		self.height = height
		self.is_mouse_down = False
		self.last_draws = []
		
		for i in range(width):
			for j in range(height):
				self.draw_rec(i, j, 'N')
				
		toolkit.grid(column=0, row=0)
		canvas.grid(column=1, row=0)
		root.mainloop()
	
	def debug(self):
		print(self.button_id.get())
	
	def undo(self):
		if not self.last_draws:
			return
		for (x,y), c in self.last_draws.pop(-1).items():
			self.draw_rec(x,y,c)
	
	def set_active(self, n):
		self.active = n
	
	def mouse_down(self, e):
		self.is_mouse_down = True
		self.last_draws.append(dict())
		self.draw(e.x, e.y)
		
	def mouse_up(self, e):
		self.is_mouse_down = False
	
	def mouse_move(self, e):
		if self.is_mouse_down:
			self.draw(e.x, e.y)
	
	def draw_rec(self, x, y, c):
		cell_size = self.cell_size
		self.canvas.create_rectangle(x*cell_size, y*cell_size, (x+1)*cell_size, (y+1)*cell_size, fill=color(c))
		old_c = self.mtx[y][x]
		self.mtx[y][x] = c
		return old_c
	
	def draw(self, x, y):
		cell_size = self.cell_size
		i = x//cell_size
		j = y//cell_size
		
		cell_code = self.active
		if self.active == 'B':
			cell_code += str(self.button_id.get())
		if self.active == 'D':
			cell_code += str(self.door_id.get())
		if self.active == 'P':
			cell_code += str(self.passable_wall_id.get())
		if self.active == 'S':
			cell_code += str(self.spawn_id.get())
			for k, row in enumerate(self.mtx):
				for m, elem in enumerate(row):
					if elem == cell_code:
						self.draw_rec(m, k, 'N')
		if self.active == 'G':
			cell_code += str(self.goal_id.get())
		
		old_c = self.draw_rec(i, j, cell_code)
		if (i,j) not in self.last_draws[-1]:
			self.last_draws[-1][(i,j)] = old_c
	
	def export(self):
		filename = self.export_filename.get() + '.map'
		if filename == '':
			filename = 'untitled.map'
		with open(filename, 'w+', encoding='utf-8') as f:
			for line in self.mtx:
				f.write(' '.join(map(str, line)))
				f.write('\n')
				
	def load(self, filename):
		self.mtx = load_map_matrix(filename)
		for j, line in enumerate(self.mtx):
			for i, elem in enumerate(line):
				self.draw_rec(i, j, self.mtx[j][i])
	
if __name__ == "__main__":
	mp = Mapeditor()