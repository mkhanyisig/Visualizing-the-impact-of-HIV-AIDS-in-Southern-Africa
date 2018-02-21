#Mkhanyisi Gamedze
# CS 251 - Spring 2017
# project 3

import csv
import sys
import numpy as np
import math
import random as rand

class view:

	# initialize the object
	def __init__(self):
		self.vrp=np.matrix([0.5, 0.5, 1])
		self.vpn=np.matrix( [0, 0, -1])
		self.vup=np.matrix( [0, 1, 0])
		self.u=np.matrix([-1, 0, 0])
		self.extent=np.matrix([1, 1, 1])
		self.screen=np.matrix( [400, 400])
		self.offset=np.matrix([100,100])
		
	
	def resetV(self):
		self.vrp=np.matrix([0.5, 0.5, 1])
		self.vpn=np.matrix( [0, 0, -1])
		self.vup=np.matrix( [0, 1, 0])
		self.u=np.matrix([-1, 0, 0])
		self.extent=np.matrix([1, 1, 1])
		self.screen=np.matrix( [400, 400])
		self.offset=np.matrix([100,100])
	
	
	# uses the current viewing parameters to return a view matrix
	def build(self):
		
		vtm = np.identity( 4, float )
		
		t1 = np.matrix( [[1, 0, 0, -self.vrp[0, 0]],
					[0, 1, 0, -self.vrp[0, 1]],
					[0, 0, 1, -self.vrp[0, 2]],
					[0, 0, 0, 1] ] )
					
		vtm = t1 * vtm
		
		#  Calculate the view reference axes tu, tvup, tvpn.
		tu=np.cross(self.vup,self.vpn)
		tvup=np.cross(self.vpn, tu)
		tvpn=self.vpn
		
		# convert to the fields
		self.u=self.normalize(tu)
		self.vup=self.normalize(tvup)
		self.vpn=self.normalize(tvpn)
		
		# align the axes
		r1 = np.matrix( [[ self.u[0, 0], self.u[0, 1], self.u[0, 2], 0.0 ],
					[ self.vup[0, 0], self.vup[0, 1], self.vup[0, 2], 0.0 ],
					[ self.vpn[0, 0], self.vpn[0, 1], self.vpn[0, 2], 0.0 ],
					[ 0.0, 0.0, 0.0, 1.0 ] ] )

		vtm = r1 * vtm
		
		
		#  Translate the lower left corner of the view space to the origin
        #vtm = T( 0.5*self.extent[0], 0.5*self.extent[1], 0 ) * vtm
		
		t2=np.matrix([[1,0,0, 0.5*self.extent[0,0]],
						[0,1,0,0.5*self.extent[0,1]],
						[0,0,1,0],
						[0,0,0,1]])
						
		vtm= t2*vtm
		
		x=np.matrix([[-self.screen[0,0]/self.extent[0,0],0,0,0],
					[0,-self.screen[0,1]/self.extent[0,1],0,0],
					[0,0, 1/self.extent[0,2],0],
					[0,0,0,1]])
					
		vtm= x* vtm
		
		t3=np.matrix([[1,0,0,self.screen[0,0]+self.offset[0,0]],
					[0,1,0,self.screen[0,1]+self.offset[0,1]],
					[0,0, 1,0],
					[0,0,0,1]])
					
		vtm= t3*vtm
		
		return vtm
   
	# takes in 3x3 matrix and returns normalized matrix 
	def normalize(self, v):
		
		# get items from matrix and enter them onto these temporary fields
		Vnorm=np.matrix(np.zeros(3))
	
		length = math.sqrt( v[0,0]*v[0,0] + v[0,1]*v[0,1] + v[0,2]*v[0,2] )
		Vnorm[0,0] = v[0,0] / length
		Vnorm[0,1] = v[0,1] / length
		Vnorm[0,2] = v[0,2] / length
		
		return Vnorm
		
	#	 clone method for your View object that makes a duplicate View object and returns it	
	def clone(self):
		
		# create new object, copy all fields and return it
		c=view()
		
		#copy all fields
		c.vrp=self.vrp
		c.vpn=self.vpn
		c.vup=self.vup
		c.u=self.u
		c.extent=self.extent
		c.screen=self.screen
		c.offset=self.offset
		print "###   done cloning"
		return	c
		
	def rotateVRC(self,rotVUP,rotU):
		# Make a translation matrix to move the point ( VRP + VPN * extent[Z] * 0.5 ) to the origin
		v=np.identity(4)
		m=self.vrp + (self.vpn * self.extent[0,2] * 0.5)

		t1 = np.matrix([[1,0,0,-m[0,0]],
				[0,1,0,-m[0,1]],
				[0,0,1,-m[0,2]],
				[0,0,0,1]])
					
		# Make an axis alignment matrix Rxyz using u, vup and vpn
		Rxyz = np.matrix( [[self.u[0,0], self.u[0,1], self.u[0,2], 0.0],
					[self.vup[0,0], self.vup[0,1], self.vup[0,2], 0.0],
					[self.vpn[0,0], self.vpn[0,1], self.vpn[0,2], 0.0],
					[0, 0, 0, 1]])
						
		# Make a rotation matrix about the Y axis by the VUP angle
		r1 = np.matrix([[math.cos(rotVUP), 0, math.sin(rotVUP), 0],
				[0, 1, 0, 0],
				[-math.sin(rotVUP), 0, math.cos(rotVUP), 0],
				[0, 0, 0, 1]])
		
		# Make a rotation matrix about the X axis by the U angle
		r2 = np.matrix([[1, 0, 0, 0],
				[0, math.cos(rotU), -math.sin(rotU), 0],
				[0, math.sin(rotU), math.cos(rotU), 0],
				[0, 0, 0, 1]])


		#Make a translation matrix that has the opposite translation from step 1

		t2=np.linalg.inv(t1)

		#make tvrc
		tvrc = np.matrix( [[self.vrp[0,0], self.vrp[0,1], self.vrp[0,2], 1.0],
						[self.u[0,0], self.u[0,1], self.u[0,2], 0.0],
						[self.vup[0,0], self.vup[0,1], self.vup[0,2], 0.0],
						[self.vpn[0,0], self.vpn[0,1], self.vpn[0,2], 0.0]])

		tvrc = (t2*Rxyz.transpose()*r2*r1*Rxyz*t1*tvrc.transpose()).transpose()
		self.mat4angle=tvrc #matrix to find angle

		#copy the values back after normalizing

		self.vrp = tvrc[0,:3]
		self.u = self.normalize(tvrc[1,:3])
		self.vup = self.normalize(tvrc[2,:3])
		self.vpn = self.normalize(tvrc[3,:3])
		return tvrc
		
						
		
						
		
		
				

		
		
		
		
	
		
		