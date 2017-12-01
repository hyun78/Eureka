
from collections import OrderedDict
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
from numpy import array


with open('type_statistics.json') as f:
	q = json.load(f,object_pairs_hook=OrderedDict)

t1 = q[0][2]
t2 = q[1][2]
t3 = q[2][2]
res = np.zeros([31,31])

for k1 in t1.keys():
	tmp1= [int(i) for i in k1.split('_')][:2]
	res[tmp1[0]][tmp1[1]] +=int(t1[k1][0])

for k2 in t2.keys():
	tmp1= [int(i) for i in k2.split('_')][:2]
	res[tmp1[0]][tmp1[1]] +=int(t2[k2][0])

for k3 in t3.keys():
	tmp1= [int(i) for i in k3.split('_')][:2]
	res[tmp1[0]][tmp1[1]] +=int(t3[k3][0])

# f = open('res.txt','w')
# for i in range(31):
# 	for j in range(31):
# 		f.write(str(res[i][j])+"\t")
# 	f.write("\n")

# f.close()


# M = 5000
# myList = [random.randrange(1200,5500)  for i in range(0,M)]

# #Convert to 50 x 100 list
# n = 50
# newList = [myList[i:i+n] for i in range(0, len(myList), n)]

#Convert to 50 x 100 numpy array
# nArray = array(newList)


nArray = array(res)
#a11=nArray.reshape(50,100)
print(nArray)
colors = ['brg','viridis','plasma','inferno','magma','Greys','Purples','Blues','Greens','Oranges','Reds','YlOrBr','YlOrRd','OrRd','PuRd','RdPu','BuPu','GnBu','PuBu','YlGnBu',
			'PuBuGn','BuGn','YlGn','binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic','Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c', 'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']
for colorscheme in colors:
	fig = plt.figure()
	fig.suptitle('GAME_ARCADE')
	plt.xlabel('X-Axis')
	plt.ylabel('Y-Axis')
	plt.imshow(nArray, cmap=colorscheme)
	plt.colorbar()
	plt.show()
	plt.savefig(colorscheme+'foo.png')
	plt.close()


