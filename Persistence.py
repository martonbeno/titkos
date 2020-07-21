

def load_map_matrix(filename):	
	ret = []
	with open(filename, 'r', encoding='utf-8') as f:
		line = f.readline().strip()
		while line:
			ret.append(line.split())
			line = f.readline().strip()
	
	return list(zip(*ret))