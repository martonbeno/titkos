import tkinter as tk
import re

def color(code):
	n = next(re.finditer(r'[A-Z]', code)).group(0)
	color = {	'N':"white",
				'W':"black",
				'B':"green",
				'D':"gray"
			}
	return color[n]

class Mapeditor:
	def __init__(self):
		cell_size = 10
		toolkit_size = 50

		width = 50
		height = 50
		self.mtx = [[0 for _ in range(50)] for _ in range(50)]
		self.active = 'N'


		root = tk.Tk()
		root.geometry(f"{cell_size*width}x{cell_size*height+toolkit_size}")
		toolkit = tk.Frame(master=root, width=cell_size*width, height=toolkit_size, bg="gray")
		
		b1 = tk.Button(master=toolkit, text="nothing", command=lambda:self.set_active('N'))
		
		b2 = tk.Button(master=toolkit, text="wall", command=lambda:self.set_active('W'))
		
		self.button_id = tk.StringVar()
		self.button_id.set('1')
		b3 = tk.Button(master=toolkit, text="button", command=lambda:self.set_active('B'))
		button_id_field = tk.Entry(master=toolkit, textvariable=self.button_id)
		
		self.door_id = tk.StringVar()
		self.door_id.set('1')
		b4 = tk.Button(master=toolkit, text="door", command=lambda:self.set_active('D'))
		door_id_field = tk.Entry(master=toolkit, textvariable=self.door_id)
		
		b5 = tk.Button(master=toolkit, text="undo", command=self.undo)
		
		b6 = tk.Button(master=toolkit, text="export", command=lambda:self.export("001.map"))
		
		b7 = tk.Button(master=toolkit, text="debug", command=self.debug)
		
		b1.grid(column=0, row=0)
		b2.grid(column=0, row=1)
		b3.grid(column=0, row=2)
		button_id_field.grid(column=1, row=2)
		b4.grid(column=0, row=3)
		door_id_field.grid(column=1, row=3)
		b5.grid(column=0, row=4)
		b6.grid(column=0, row=5)
		b7.grid(column=0, row=6)
		


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
				
		toolkit.pack()
		canvas.pack()
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
			assert re.match(r'^\d+$', self.button_id.get()), "szám kell legyen a mezőben"
			cell_code += str(self.button_id.get())
		if self.active == 'D':
			assert re.match(r'^\d+$', self.door_id.get()), "szám kell legyen a mezőben"
			cell_code += str(self.door_id.get())
		
		old_c = self.draw_rec(i, j, cell_code)
		if (i,j) not in self.last_draws[-1]:
			self.last_draws[-1][(i,j)] = old_c
	
	def export(self, filename):
		with open(filename, 'w+', encoding='utf-8') as f:
			for line in self.mtx:
				f.write(' '.join(map(str, line)))
				f.write('\n')
	
if __name__ == "__main__":
	mp = Mapeditor()