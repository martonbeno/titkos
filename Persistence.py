

def load_map_matrix(filename):	
	ret = []
	with open(filename, 'r', encoding='utf-8') as f:
		line = f.readline().strip()
		while line:
			ret.append(line.split())
			line = f.readline().strip()
	
	return list(zip(*ret))

mtx = [
		[0,0,0,0,0,0],
		[0,0,0,0,0,0],
		[0,1,1,1,1,0],
		[0,1,1,1,1,0],
		[0,1,1,1,1,0],
		[0,0,0,0,0,0]
]

def get_rectangle(mtx, x, y, c):
	i = x
	j = y
	
	while mtx[i][y] == c:
		i += 1
		print(i)
		
	
	print(x,i, y,j)
	# return (x,y,i,j)

print(get_rectangle(mtx, 2, 1, 1))