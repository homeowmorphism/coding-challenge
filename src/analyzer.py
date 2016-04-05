#!/usr/bin/python
from __future__ import division
import datetime
from collections import deque 

import reader

def refaddvertex(vref,vertices):
	nv = len(vertices) #number of vertices
	if nv > 1:
		for vertex in vertices:
			if vertex in vref:
				vref[vertex] = vref[vertex] + nv - 1
			else:
				vref[vertex] = nv - 1	

def refdeletevertex(vref,vertices):
	nv = len(vertices)
	if nv > 1:
		for vertex in vertices:
			if vertex in vref:
				vref[vertex] = vref[vertex] - nv + 1
				if vref[vertex] == 0:
					vref.pop(vertex, None)
				elif vref[vertex] < 0:
				#	print 'error in counting vertex was found'
					vref.pop(vertex, None)
			#else:
			#	print 'could not find vertex to delete'

def outoftime(Q,t):
	t1 = Q[-1][0]
	return t1 > t

def old(Q,t):
	t1 = Q[-1][0]
	return t1 - t > datetime.timedelta(seconds = 60)

def fixoutoftime(Q,t,vertices,vref):
	t0 = Q[0][0]
	if t <= t0:
		Q.appendleft((t,vertices))
		refaddvertex(vref,vertices)
	else:
		P = deque()
		while t < Q[-1][0]:
			P.appendleft(Q.pop())
		Q.append((t,vertices))
		refaddvertex(vref,vertices)

		while P:
			Q.append(P.popleft())

def refresh(Q,t,vertices,vref):
	if Q:
		t0 = Q[0][0]
		if t - t0 > datetime.timedelta(seconds = 60): 
			old_vertices =  Q.popleft()[1]
			refdeletevertex(vref,old_vertices)
	if len(vertices) > 1:
		Q.append((t,vertices))
		refaddvertex(vref,vertices)

def calc_avg(vref):
	n = len(vref)
	s = 0
	for vertex in vref:
		s = s + vref[vertex]
	if n == 0:
		return '0.00'
	else:
		return ("%.2f" %(s/n))

def analyze(data): #data list of tuples (time,[hashtags])
	output = open('./tweet_output/output.txt', 'w')
	Q = deque() #linked list that stores info
	vref = {} #vertex ref count 

	for i in range(len(data)):
		t = data[i][0]
		vertices = data[i][1]

		if Q and outoftime(Q,t):
			if old(Q,t):
				pass
			else:
				fixoutoftime(Q,t,vertices,vref)
		else:
			refresh(Q,t,vertices,vref)

		output.write(calc_avg(vref) + '\n')

