import re

def load_map_matrix(filename):	
	ret = []
	with open(filename, 'r', encoding='utf-8') as f:
		line = f.readline().strip()
		while line:
			ret.append(line.split())
			line = f.readline().strip()
		
	return ret

def map_to_dicts(filename):
	mtx = load_map_matrix(filename)
	mtx = list(zip(*mtx))
	n, m = len(mtx), len(mtx[0])
	skip_index = set()
	ret = []
	
	for i in range(n):
		for j in range(m):
			if (i,j) in skip_index:
				continue
			
			if mtx[i][j] != 'N':
				act = mtx[i][j]
				k = i
				k = 0
				o = j
				o = 0
				while j+o < m and mtx[i+k][j+o] == act:
					o += 1
				o -= 1
				while i+k < n and all(mtx[i+k][p] == act for p in range(j, j+o+1)):
					k += 1
				k -= 1
				for ii in range(i,i+k+1):
					for jj in range(j, j+o+1):
						skip_index.add((ii,jj))
				ret.append({'field':act, 'x':i, 'y':j, 'height':o+1, 'width':k+1})
	
	return ret