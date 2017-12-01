
from collections import OrderedDict
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
from numpy import array

def make_wan_img(section,type_list):
	nArray = make_img_arr(section)
	nArray2 = np.zeros(nArray.shape)
	for i in range(len(nArray)):
		for j in range(len(nArray)):
			for tnum in type_list:
				lst = tnum.split('_')
				if len(lst)==3 and  (int(lst[0])==i and int(lst[1])==j):
					nArray2[i][j] = nArray[i][j]
					# print(lst,i,j,len(nArray),nArray)
	print(type_list)
	colorscheme = 'Reds'
	fig = plt.figure()
	fig.suptitle(section)
	plt.xlabel("first word's cluster")
	plt.ylabel("second word's cluster")
	plt.imshow(nArray2, cmap=colorscheme)
	plt.colorbar()
	plt.show()
	plt.savefig('static/'+colorscheme+section+'_WANcencored.png')
	plt.close()

	return

def make_img_arr(section):
	with open('database/'+section+'/type_statistics.json') as f:
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

	nArray = array(res)

	return nArray

def make_img(section):
	nArray = make_img_arr(section)
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
	# for colorscheme in colors:
	colorscheme = 'Reds'
	fig = plt.figure()
	fig.suptitle(section)
	plt.xlabel("first word's cluster")
	plt.ylabel("second word's cluster")
	plt.imshow(nArray, cmap=colorscheme)
	plt.colorbar()
	plt.show()
	plt.savefig('static/'+colorscheme+section+'.png')
	plt.close()
	return


