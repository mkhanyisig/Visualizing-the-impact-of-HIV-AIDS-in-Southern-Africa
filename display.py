# Skeleton Tk interface example
# Written by Bruce Maxwell
# Modified by Stephanie Taylor
# Further modified and used by Mkhanyisi Gamedze
# CS 251
# Spring 2015

import Tkinter as tk
import tkFont as tkf
import math
import random
import os
import Dialog as dialog
import view
import numpy as np
import data
import tkFileDialog
import scipy.stats
import analysis
import tkSimpleDialog
import csv
import classify_naivebaye

# create a class to build and manage the display
class DisplayApp:

	# initialize the object
	def __init__(self, width, height):
		
		
		# new View object 
		self.v=view.view()
		
		# creating axes matrices, with start and end points
		self.axes=np.matrix([[0,0,0,1],[1,0,0,1],[0,0,0,1],[0,1,0,1],[0,0,0,1],[0,0,1,1]])
		
		
			
		# scaling text to notify user
		self.txt = "Scaling: Default"
		self.regtxt="Regression data : None "
		
		# list that stores axis lines
		self.lines=[]
		
		self.datafile=None
		
		# create a tk object, which is the root window
		self.root = tk.Tk()

		# width and height of the window
		self.initDx = width
		self.initDy = height
		self.scale=1

		# set up the geometry for the window
		self.root.geometry( "%dx%d+50+30" % (self.initDx, self.initDy) )

		# set the title of the window
		self.root.title("Mkhanyisi TK lab project")

		# set the maximum size of the window for resizing
		self.root.maxsize( 1600, 900 )

		# setup the menus, caling method below
		self.buildMenus()

		# build the controls, caling method below
		self.buildControls()

		# build the Canvas, caling method below
		self.buildCanvas()

		# bring the window to the front (TK method)
		self.root.lift()

		# - do idle events here to get actual canvas size
		self.root.update_idletasks()

		# now we can ask the size of the canvas
		print self.canvas.winfo_geometry()

		# set up the key bindings
		self.setBindings()
		""" Class fields"""
		# set up the application state
		self.objects = [] # list of data objects that will be drawn in the canvas # empty list
		self.data = None # will hold the raw data someday.
		self.baseClick = None # used to keep track of mouse movement
		self.xp=0
		self.yp=0
		
		# change axes labels
		self.xx="X"
		self.yx="Y"
		self.zx="Z"

		#Axes labels
		self.labelX = tk.Label(self.canvas, text=self.xx)
		self.labelY = tk.Label(self.canvas, text=self.yx)
		self.labelZ = tk.Label(self.canvas, text=self.zx)
		
		
		
		
		
		self.b3scale=float(1)
	
		# build + update axes
		self.buildAxes()
		
		self.clone=None
		
		# new data object to read-in the given CSV file
		self.D=data.Data("data-simple.csv")
		
		self.result=[]
		
		# default shape
		self.shape="circle"
		
		# default color axis option
		self.colorX="Red-Green"
		
		# add line graphical object associated with regression
		self.line=None
		self.RegObjects=[]
		self.endpoints=None
	
		# boolean to indicate whether user has built points or not
		self.build=False
		self.built=False
	
		# initially set the PCAdata value to None
		self.pcadata=None
		
		# PCAs dicionary
		self.PCAdict={}
		self.PCAdataD={}
		
		self.clust=False
		
		self.countries=["Swaziland", "Zimbabwe","Zambia","South Africa", "Namibia", "Mozambique", "Malawi", "madagascar", "Lesotho", "Botswana", "Angola"]
		
	
		

	# reset method
	def resetV(self):
	
		print "reset #########################"
		
		self.clearData()
		self.line=None
		
		# creating axes matrices, with start and end points
		self.axes=np.matrix([[0,0,0,1],[1,0,0,1],[0,0,0,1],[0,1,0,1],[0,0,0,1],[0,0,1,1]])
		
		# add line graphical object associated with regression
		self.line=None
		self.RegObjects=[]
		self.endpoints=None
		
		self.v.resetV()
		self.updateAxes()
			
		# scaling text to notify user
		strng = "Scaling: Default"
		self.scaleframe.config(text=strng)
	
		# reset booleans
		self.build=False
		self.built=False

	# build axes method
	def buildAxes(self):
		
		#build the view
		vtm=self.v.build()
		#print "...	 vtm \n",vtm
		#  transposes the axis points so each point is a column, 
		# multiplies it by the VTM, and then takes the transpose so that the pts matrix has the axis endpoints as rows again
		
		
		pts = (vtm * (self.axes.transpose())).transpose()
		#print "...	 pts  \n",pts
		
		self.pts=pts # pts field
		#print "pts:	   \n", pts
		
		l=self.canvas.create_line(pts[0,0], pts[0,1],pts[1,0], pts[1,1],fill="red") 
		self.lines.append(l)
		l=self.canvas.create_line(pts[2,0], pts[2,1],pts[3,0], pts[3,1],fill="blue")
		self.lines.append(l)
		l=self.canvas.create_line(pts[4,0], pts[4,1],pts[5,0], pts[5,1],fill="green")
		self.lines.append(l)
		# print "number of lines:	 ", len(self.lines)
		
		
		
		#make labels for the axes
		self.labelX.place(x=pts[1,0],y=pts[1,1])
		self.labelY.place(x=pts[3,0],y=pts[3,1])
		self.labelZ.place(x=pts[5,0],y=pts[5,1])
		#print "**   y :",pts[1,1],"    **  x: ",pts[1,0]
		self.labels=[]
		
		self.labels.append(self.labelX)
		self.labels.append(self.labelY)
		self.labels.append(self.labelZ)
		
		self.colors=['yellow','gold','darkgreen','black','blue','purple','magenta','gray54','red','saddlebrown','rosy brown','bisque4','OrangeRed4']
			# build legend
		
		
		self.countries=["Swaziland", "Zimbabwe","Zambia","South Africa", "Namibia", "Mozambique", "Malawi", "madagascar", "Lesotho", "Botswana", "Angola"]
		
	
			
		ix=1
		xi=int(900) # width x-position
		yi=66 # height y-position
		for country in self.countries:
			c=tk.Label(self.canvas,text=self.countries[ix-1])
			c.place(x=xi,y=yi)
			#print "color  :",self.colors[ix-1]
			point=self.canvas.create_oval(xi+10,yi+10,xi-10,yi-10,fill=self.colors[ix-1],outline="")
			yi+=40
			ix+=1
			
		
		
		
		
		
		
	def updateAxes(self):
		self.canvas.delete(self.line)
		
		for line in self.lines: # remove lines from display
			self.canvas.delete(line)
		
		# delete all labels
		for label in self.labels:
			self.canvas.delete(label)
			label.destroy()
			
		
		
		vtm=self.v.build()
		
		pts = (vtm * self.axes.transpose()).transpose()
		self.pts=pts # pts field
		
		self.lst=self.pts.tolist()


		if len(self.lines)>2:
			self.lines[0]=self.canvas.create_line(pts[0,0], pts[0,1],pts[1,0], pts[1,1],fill="red")
			self.lines[1]=self.canvas.create_line(pts[2,0], pts[2,1],pts[3,0], pts[3,1],fill="blue")
			self.lines[2]=self.canvas.create_line(pts[4,0], pts[4,1],pts[5,0], pts[5,1],fill="green")
		
			if self.line!=None:
				mycolor = '#%02x%02x%02x' % (255, 0, 100)
				self.line=self.canvas.create_line(self.lst[6][0], self.lst[6][1],self.lst[7][0],self.lst[7][1], fill=mycolor)
				
				self.labelL = tk.Label(self.canvas, text=self.ltxt)
				self.labelL.place(x=self.lst[7][0],y=self.lst[7][1])
				self.labels.append(self.labelL)
			
			

		#reconfigure Axes labels
		self.labelX = tk.Label(self.canvas, text=self.xx)
		self.labelY = tk.Label(self.canvas, text=self.yx)
		self.labelZ = tk.Label(self.canvas, text=self.zx)

		#make labels for the axes
		self.labelX.place(x=pts[1,0],y=pts[1,1])
		self.labelY.place(x=pts[3,0],y=pts[3,1])
		self.labelZ.place(x=pts[5,0],y=pts[5,1]+5)
		#print "**   y :",pts[1,1],"    **  x: ",pts[1,0]
		
		self.labels.append(self.labelX)
		self.labels.append(self.labelY)
		self.labels.append(self.labelZ)

	#
	def buildMenus(self):
		
		# create a new menu
		menu = tk.Menu(self.root)

		# set the root menu to our new menu
		self.root.config(menu = menu)

		# create a variable to hold the individual menus
		menulist = []

		# create a file menu
		filemenu = tk.Menu( menu )
		menu.add_cascade( label = "File", menu = filemenu )
		menulist.append(filemenu)

		# create another menu for kicks
		cmdmenu = tk.Menu( menu )
		menu.add_cascade( label = "Command", menu = cmdmenu )
		menulist.append(cmdmenu)

		# menu text for the elements
		# the first sublist is the set of items for the file menu
		# the second sublist is the set of items for the option menu
		menutext = [ [ '-', 'Clear	 \xE2\x8C\x98', 'Quit	\xE2\x8C\x98-Q' ],
					 [ 'Command 1', '-', '-' ] ]

		# menu callback functions (note that some are left blank,
		# so that you can add functions there if you want).
		# the first sublist is the set of callback functions for the file menu
		# the second sublist is the set of callback functions for the option menu
		menucmd = [ [None, self.clearData, self.handleQuit],
					[self.handleMenuCmd1, None, None] ]
		
		# build the menu elements and callbacks
		for i in range( len( menulist ) ):
			for j in range( len( menutext[i]) ):
				if menutext[i][j] != '-':
					menulist[i].add_command( label = menutext[i][j], command=menucmd[i][j] )
				else:
					menulist[i].add_separator()

	# create the canvas object
	def buildCanvas(self):
		self.canvas = tk.Canvas( self.root, width=self.initDx, height=self.initDy )
		self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
		return

	# build a frame and put controls in it
	def buildControls(self):

		### Control ###
		# make a control frame on the right
		rightcntlframe = tk.Frame(self.root)
		rightcntlframe.pack(side=tk.RIGHT, padx=2, pady=2, fill=tk.Y)

		# make a separator frame
		sep = tk.Frame( self.root, height=self.initDy, width=2, bd=1, relief=tk.SUNKEN )
		sep.pack( side=tk.RIGHT, padx = 2, pady = 2, fill=tk.Y)

		# use a label to set the size of the right panel
		label = tk.Label( rightcntlframe, text="*Control Panel*", width=20 )
		label.pack( side=tk.TOP, pady=10 )
		
		# open file
		Rst = tk.Button( rightcntlframe, text="Open CSV File",
						  command=self.handleOpen )
		Rst.pack(side=tk.TOP)	 # default side is top

		
		
		# create scaling status bar
		self.scaleframe = tk.Label(rightcntlframe, text=self.txt, anchor=tk.W, state=tk.ACTIVE)
		self.scaleframe.pack(side=tk.BOTTOM, fill=tk.X)
		
		
		
		# option menu for the shape of the plotted data
		
		label = tk.Label( rightcntlframe, text="select shape", width=20 )
		label.pack( side=tk.TOP, pady=10 )
		
		
		self.var = tk.StringVar(rightcntlframe)
		self.var.set("circle") # initial value

		option = tk.OptionMenu(rightcntlframe, self.var, "circle", "square")
		option.pack()
		
		
		# option menu for the color axis of the plotted data
		
		label = tk.Label( rightcntlframe, text="Select Color axis option", width=20 )
		label.pack( side=tk.TOP, pady=10 )
		
		
		self.varC = tk.StringVar(rightcntlframe)
		self.varC.set("Red-Green") # initial value

		option = tk.OptionMenu(rightcntlframe, self.varC, "Red-Green", "Blue-yellow")
		option.pack()
		
		
		Rdata = tk.Button( rightcntlframe, text="PCA analysis",command=self.PCAanalysis )
		Rdata.pack(side=tk.TOP)
		
		
		#make a listbox for dislpaying the PCA's
		self.listbox = tk.Listbox(rightcntlframe,height=4)
		
		self.listbox.activate(0)
		self.listbox.pack(side=tk.TOP)
		
		#makes a button to plot the listbox
		self.buttonl = tk.Button( rightcntlframe, text="Plot Selected PCA",command=self.plotPCA)
		self.buttonl.pack(side=tk.TOP)	# default side is top
		
		#b = tk.Button(rightcntlframe, text="Delete",command=self.listbox.delete(self.listbox.curselection()))
		
		# make a button to delete the selected PCA
		self.delbutton = tk.Button( rightcntlframe, text="Delete Selected PCA",command=self.deletePCA )
		self.delbutton.pack(side=tk.TOP)
		
		
		# make a button to delete the selected PCA
		self.delbutton = tk.Button( rightcntlframe, text="view selected PCA",command=self.viewPCA )
		self.delbutton.pack(side=tk.TOP)
		
		
		Rdata = tk.Button( rightcntlframe, text="PlotData",
						  command=self.handlePlotData )
		Rdata.pack(side=tk.TOP)	 # default side is top
		
		Rdata = tk.Button( rightcntlframe, text="Cluster Analysis",
						  command=self.clusterAnalysis )
		Rdata.pack(side=tk.TOP)	 # default side is top
		
		Rdata = tk.Button( rightcntlframe, text="Plot Cluster Data",
						  command=self.PlotCluster )
		Rdata.pack(side=tk.TOP)	 # default side is top
		
		Rdata = tk.Button( rightcntlframe, text="PCA + Cluster data",
						  command=self.pca_cluster )
		Rdata.pack(side=tk.TOP)	 # default side is top
		
		Rdata = tk.Button( rightcntlframe, text="XY -2D Linear regression",
						  command=self.handleLinearRegression )
		Rdata.pack(side=tk.TOP)	 # default side is top
		
		
		Rdata = tk.Button( rightcntlframe, text="confusion of train-test",
						  command=self.classify_data )
		Rdata.pack(side=tk.TOP)	 # default side is top
		
		self.rspeed = tk.Scale (rightcntlframe, label="Rotation speed",orient=tk.HORIZONTAL,from_=1,to=110)
		self.rspeed.set(100)
		self.rspeed.pack(side=tk.TOP)
		
		self.tspeed = tk.Scale (rightcntlframe, label="Translation speed",orient=tk.HORIZONTAL,from_=1,to=13)
		self.tspeed.set(1)
		self.tspeed.pack(side=tk.TOP)
			
		self.sspeed = tk.Scale (rightcntlframe, label="Scaling speed",orient=tk.HORIZONTAL,from_=1,to=10)
		self.sspeed.set(1)
		self.sspeed.pack(side=tk.TOP)
		
		Rdata = tk.Button( rightcntlframe, text="Save plot",command=self.save )
		Rdata.pack(side=tk.TOP)	 # default side is top
		
		
		Rdata = tk.Button( rightcntlframe, text="clear",command=self.clearData )
		Rdata.pack(side=tk.TOP)	 # default side is top
		
		Rst = tk.Button( rightcntlframe, text="reset",
						  command=self.resetV )
		Rst.pack(side=tk.TOP)	 # default side is top


		return

	def setBindings(self):
		# bind mouse motions to the canvas
		self.canvas.bind( '<Button-1>', self.handleMouseButton1 )
		self.canvas.bind( '<Control-Button-1>', self.handleMouseButton2 )
		self.canvas.bind( '<Button-2>', self.handleMouseButton2 )
		self.canvas.bind( '<B1-Motion>', self.handleMouseButton1Motion )
		self.canvas.bind( '<B2-Motion>', self.handleMouseButton2Motion )
		self.canvas.bind( '<Control-B1-Motion>', self.handleMouseButton2Motion )
		self.canvas.bind( '<Button-3>', self.handleMouseButton3 )
		self.canvas.bind( '<B3-Motion>', self.handleMouseButton3Motion )
		self.canvas.bind( '<ButtonRelease-3>', self.handleMouseButton3release )
		self.canvas.bind( '<Configure>', self.resize )
		

		# bind command sequences to the root window
		self.root.bind( '<Command-q>', self.handleQuit )
		self.root.bind( '<Command-n>', self.clearData )
		self.root.bind( '<Command-n>', self.clearData )
		self.root.bind( '<Command-r>', self.resetV ) # reset
		self.root.bind( '<Command-o>', self.handleOpen ) # open file

		#self.root.bind("<Return>", self.ok)

	def handleQuit(self, event=None):
		print 'Terminating'
		self.root.destroy()

	def handleButton1(self):
		print 'handling command button:', self.colorOption.get()
		
		for obj in self.objects:
		  self.canvas.itemconfig(obj, fill=self.colorOption.get() )
		  
	def handleMenuCmd1(self):
		print 'handling menu command 1'

	def handleMouseButton1(self, event):
		
		print 'handle mouse button 1: %d %d' % (event.x, event.y)
		self.baseClick = (event.x, event.y)
		self.baseClick1 = (event.x, event.y)

		
		self.xp=event.x
		self.yp=event.y
		
		#loc = self.canvas.coords(obj) # update the location of all objects in the self.objects list

	def handleMouseButton2(self, event):
		self.baseClick = (event.x, event.y)
		self.baseClick2=self.baseClick # as suggested
		self.clone=self.v.clone()
		#print '\n	handle mouse button 2: %d %d' % (event.x, event.y)," \n"
	
	def handleMouseButton3(self, event):
		#print "handling mouse button 3...."
		#base click for button 3 motion
		self.baseClick = (event.x, event.y)
		self.b3=self.baseClick
		self.b3extent=np.copy(self.v.extent)

	""" move axes"""
	# This is called if the first mouse button is being moved
	def handleMouseButton1Motion(self, event):
		# calculate the difference
		# Calculate the differential motion since the last time the function was called
		# Divide the differential motion (dx, dy) by the screen size (view X, view Y)
		diff = ( event.x - self.baseClick[0], event.y - self.baseClick[1] )
		self.dx=event.x - self.baseClick[0]
		self.dy=event.y - self.baseClick[1]
		
		# update my baseclick
		self.baseClick=(event.x , event.y)
			
		
		#print ".................................diff:"+str(diff)+"..... loc"+str(loc)

		# update base click
		self.baseClick = ( event.x, event.y )
		
		
		
		delta0=(float(diff[0])*self.tspeed.get())/self.v.screen[0,0]*self.v.extent[0,0]
		delta1=(float(diff[1])*self.tspeed.get())/self.v.screen[0,1]*self.v.extent[0,1]
		
		# update vrp
		self.v.vrp=self.v.vrp+delta0 *self.v.u + delta1 *self.v.vup
		
		self.updateAxes()
		self.updatePoints()
	
	"""	 scaling the axes """		
	def handleMouseButton2Motion(self, event):
		#print 'handle button 2 motion'
		
		delta0=(float((event.x-self.baseClick2[0])/(200*math.pi))*self.rspeed.get()/100)   # calculate the difference
		delta1 = (float(( event.y-self.baseClick2[1])/(200*math.pi))*self.rspeed.get()/100)
		
		# Clone the original View object and assign it to your standard view field
		self.v=self.clone 
		#print "v  :  ",self.v
		self.v.rotateVRC(delta0,delta1)
		#print "delta 0,1  :  ",delta0,delta1
		self.updateAxes()
		
		self.updatePoints()
	
	def handleMouseButton3release(self,event):
	   #print " mouse button 3 Release...."
	   self.b3extent=np.copy(self.v.extent)

	# needs work
	def handleMouseButton3Motion(self, event):
		#print "motion"
		self.baseclick3=(event.x,event.y) # change the baseclick value
		
		#print "Events, (x,y),	 :",event.x,"	 ",event.y
		
		self.b3diff=float(self.baseclick3[1]-self.b3[1]) # change in y is what matters
		self.b3scale=(self.b3scale+(self.b3diff/self.initDy))
		
		# string for display window
		self.txt="Scaling: "+str(1/self.b3scale)
		if self.regtxt=="Regression data : None ":
			fnl=self.txt
		else:
			fnl=self.txt+" /n "+self.regtxt
		self.scaleframe.config(text=fnl)
		
		# ensuring scale is between 0.1 and 3
		if self.b3scale < 0.1:
			self.b3scale=0.1
		if self.b3scale > 3:
			self.b3scale=3
		
		self.v.extent=self.b3scale*self.b3extent*self.sspeed.get()	 # scale axis
		self.b3scale=1 # restore scale to default
		
		self.updateAxes()
		self.updatePoints()

	########### new methods ##########
	
	# create 100 random data points on the frame
	def createRandomDataPoints( self, event=None ):
		
		"do nothing for this project, not used"
		h=self.initDy
		
		
			
			
				
				
			
			#print "creating point at	" +str(x)+"	   ,   "+str(y)

		print "number of Objects:  "+str(len(self.objects))
		
		#for obj in self.objects:  """ useless code """
		#	self.canvas.itemconfig(obj, fill=self.colorOption.get() )
				
	# Clear all data
	def clearData(self, event=None):
		print "clearing the screen"
		self.canvas.delete("all")
		self.objects=[] # new empty list

		# creating axes matrices, with start and end points
		self.axes=np.matrix([[0,0,0,1],[1,0,0,1],[0,0,0,1],[0,1,0,1],[0,0,0,1],[0,0,1,1]])
	
	# delete points under selection if you press "command-shift-mousebutton1"
	def delete(self, event=None):
	
		self.canvas.delete()

	# project 4 methods
	def handleOpen(self, event=None):
		
		
		
		# reset booleans
		self.build=False
		self.built=False
		
		self.axes=np.matrix([[0,0,0,1],[1,0,0,1],[0,0,0,1],[0,1,0,1],[0,0,0,1],[0,0,1,1]])
		
		self.line=None
		
		self.ltxt=""
		self.btxt="No line plotted yet"
		
		fn = tkFileDialog.askopenfilename( parent=self.root,
		title='Choose a data file', initialdir='.' )
		
		if fn=="	 ":
			return
		print "#*  fn niggga	#*",fn,"*# ######"
		
		self.datafile=fn
	 
		self.D=data.Data(fn)	# set the data object to hold this new file

			
	def PCAanalysis(self, event=None):
		# open dialog box if user has not selected data yet
		
		if self.D.get_headers()==[]:
			print "check again, your data has no numeric columns"
			return
		
		# Select a file which you do a PCA analysis on
		self.handleOpen()
		#self.pcadata = analysis.pca( self.D, self.D.get_headers(), True )	# no need for this line

		dial= PCABox( self.root,self.D.get_headers(), "Choose Axes for PCA analysis")
		
		# headers for PCA analysis
		result=dial.Result()
		
		if result==None:
			print "please select the columns for the PCA again"
		
		print "#*	selection result  :",result
		# name the analysis
		PCAname = tkSimpleDialog.askstring("String", "Name your analysis")
		# incase the user does not feel like typing
		if PCAname==None:
			PCAname="default"
		if PCAname=='':
			PCAname="default"
		# do PCA analysis for selected columns, returns PCAdata object
		self.pcadata = analysis.pca( self.D, result, False )
		#print "#* ", self.pcadata
		
		print "done with PCA"
		
		self.PCAname=PCAname+".csv"
		
		# create and write into a CSV file the result of the PCA and name the file using the name given
		with open(PCAname+'.csv', 'wb') as df:
			writer = csv.writer(df)

			# headers list, write onto first line of CSV file
			print "result  :", result
			
			list=[]
			l=[]
			for i in range(len(result)):
				l.append(result[i])
				i=i+1
			list.append(l)
			writer.writerows(list)
				
			
			# all the PCA data is numeric, add numeric types onto CSV
			#write the types(all "numeric")
			list=[]
			l=[]
			for i in range(len(result)):
				l.append("numeric")
				i=i+1
			list.append(l)
			writer.writerows(list)
			print "#*	 PCA data	:",self.pcadata
			#write the data for each row
			d=self.pcadata.get_Num_Matrix().transpose()
			print "shape  :",d.shape
			list=[]
			for i in range (0,d.shape[0],1):
				l=[]
				for j in range (0,d.shape[1],1):
					l.append(str(d[i,j]))
				list.append(l)
			writer.writerows(list)
			df.close() # done creating the CSV file

			
			print "done creating the CSV file"
		df.close
		
		#send the temp file to read, create all the necessary fields
		PCAinfo=self.pcadata # PCA data object
		self.listbox.insert(tk.END,PCAname)		   #add the PC name to our listbox
		
		# add these 
		self.PCAdict[PCAname]=self.pcadata # link name to the data object for PCA
		self.PCAdataD[PCAname]=PCAinfo	 
	
	
	def plotPCA(self, event=None):
		name=str((self.listbox.get(tk.ACTIVE)))
		print "you want to plot	  ",name
		self.D=self.PCAdataD[name]
		
		#	a handle plot specially for this case
		self.headers=self.D.get_headers()
		
		
		headers=self.headers # get first three columns and make them the x,y,z axes
		print "numeric headers length:_____		",len(headers)
		#print "*****************"
		if self.result==None:
			print "self.result is None"
			return
			
		
		#print "******************"
		self.headers=headers
		# get column data
		self.dataMatrix=self.D.get_data(headers).transpose()   # transpose matrix such that it gives column rows, to easily select XYZ values
		
		dial= DialogBox( self.root,self.headers, "Choose the axes")
		self.result=dial.Result()
		self.LRdata=self.result
		print "#*		  result   :",self.result
		if self.result==[]:
			print "terminate"
			return
		
		
		# change axes labels
	   
		self.xx="X- : "+self.result[0]
		self.yx="Y- : "+self.result[1]
		self.zx="size: "+self.result[2]+", Color:  "+self.result[3]
		
		
		self.buildPoints()
		
		self.updateAxes()
	
	
	def clusterAnalysis(self, event=None):
		
		clust=ClusterBox( self.root,self.D.get_headers(), "select headers for Cluster analysis and number of clusters")
		
		if clust.Result()==None:
			print "no selected result for cluster"
			return
		
		headers, k=clust.Result() # retrieve outcome 
		print "K1 :",k
		codebook, codes, error=analysis.kmeans(self.D, headers, k)
		
		data=self.D.get_data(headers)
		
		"""
		size=[]
		for i in range(len(codes)):
			g=np.matrix([1])
			size.append(g)
		# add a constant size column
		#size=np.matrix(size)
		data=self.D.add_datacolumn("size ","numeric",size,data)
		headers.append("size")
		"""
		# create column containing clustering codes
		column=[]
		column.append("Cluster ID")
		column.append("numeric")
		
		
		
		
		for code in codes:	# add cluster ID values in
			column.append(code)
			#print "type :",type(code)
		#print "column :", column	
		# add column to my data object
		print "before :", len(column[10])
		
		
		mtx=self.D.add_datacolumn(column[0],column[1],column[2:],data) # add Cluster ID data to matrix of selected headers
		
		print "**** done"
		# write in a csv file of the cluster data
		headers.append("Cluster ID")
		
		self.D.write("aclusteranalysis", headers)
		
		self.clust=True
		self.colors=['yellow','gold','darkgreen','black','blue','purple','magenta','gray54','red','saddlebrown','rosy brown','bisque4','OrangeRed4']
		
		
		
	def PlotCluster(self, event=None):
		
			self.clust=True # set clustered equal to true
			
			# read in csv file
			self.D=data.Data("aclusteranalysis.csv")
			
			# call plot data window
			self.handlePlotData()
			
	# extension method PCA+Cluster
	def pca_cluster(self, event=None):
		
		self.PCAanalysis()
		
		self.D=self.pcadata
		
		self.clusterAnalysis()
		
		self.handlePlotData()
	
	
	# select training set and test, then compute the confusion matrix
	def classify_data(self, event=None):
		
		
		
		print " Please select your train set File"
		train = tkFileDialog.askopenfilename( parent=self.root,
		title='Choose a TRAINING set data  file', initialdir='.' )
		
		print " Choose TEST set data file"
		
		test = tkFileDialog.askopenfilename( parent=self.root,
		title='Choose a test set data file', initialdir='.' )
		
		# choose files
		
		
		
		program=classify_naivebaye.classify_NB(train,test)
		
		print program.get_confusion()
		
		
		
		
	def deletePCA(self, event=None):
		name=str((self.listbox.get(tk.ACTIVE)))
		index=0
		for item in self.listbox.get(0,self.listbox.size()):
			if item==name:
				self.listbox.delete(index)
			index=index+1
		print "You deleted ",name
	
	def viewPCA(self):
		name=str((self.listbox.get(tk.ACTIVE)))
		if name=='':
			print 'you have not selected anything'
			return
		if name==None:
			print 'No name selected'
			return	  
		
		pdata=self.PCAdataD[name]	 # PCA data object with all the values we need
		
		# find number of rows and columns
		ncols=len(pdata.get_headers())
		nrows=pdata.get_Num_Matrix().shape[1]
		print "number of columns :",ncols
		print "number of rows	 :",nrows
		
		# build 
		top = tk.Toplevel()
		top.title("PCA analysis data")
		
		# first write in eigenvectors, eigenvalues and cumulative column headers
		b=tk.Label(top,text="Eigenvectors")
		b.grid(row=0,column=0)
		b=tk.Label(top,text="Eigenvalues")
		b.grid(row=0,column=1)
		b=tk.Label(top,text="Cumulative")
		b.grid(row=0,column=2)
		colindex=3
		#make grid of the titles for the columns
		
		# write in headers
		hd=pdata.get_data_headers().tolist()
		for element in hd[0]:			
			b=tk.Label(top,text=element)
			b.grid(row=0,column=colindex)
			colindex+=1
		
		# write in eigenvectors
		rowindex=1
		hd=pdata.get_newheaders().tolist()
		print "type headers :",type(hd),"	   ",hd
		for element in hd[0]:			
			b=tk.Label(top,text=element)
			b.grid(row=rowindex,column=0)
			rowindex+=1
			
			
		# write in eigenvalues
		rowindex=1
		hd=pdata.get_eigenvalues().tolist()
		print "type headers :",type(hd),"	   ",hd
		for element in hd[0]:			
			b=tk.Label(top,text=element)
			b.grid(row=rowindex,column=1)
			rowindex+=1
			
		# write in cumulative eigenvalues
		total=0
		hd=pdata.get_eigenvalues().tolist()
		print "type headers :",type(hd),"	   ",hd
		for element in hd[0]:
			total+= element		
		value=0		
		rowindex=1
		for element in hd[0]:
			value+= element 
			perc=value/total	
			b=tk.Label(top,text=perc)
			b.grid(row=rowindex,column=2)
			rowindex+=1
		
		
		
		mdata=pdata.get_eigenvectors()
		
		print "#* shape :",mdata.shape
		
		#print mdata
		
		for n in range(mdata.shape[0]):
			
			for m in range(mdata.shape[1]):
				
				v=n+1
				w=m+3
				
				x=mdata.item((m, n))
				
				
				
				b=tk.Label(top,text=x)
				b.grid(row=v,column=w)
		
		
	
	
	
	def handlePlotData(self, event=None):
		
		self.handleChooseAxes()
		
		
		if self.result==[]:
			print "terminate"
			return
			
		if self.result[-1]=="Country":
			self.clust=True
			
			
			
		self.buildPoints()
		
		self.updateAxes()
		
		
		
		print "plotting"
		
	def handleChooseAxes(self, event=None):
		self.headers=self.D.get_headers()
		
		
		headers=self.headers # get first three columns and make them the x,y,z axes
		print "numeric headers length:_____		",len(headers)
		#print "*****************"
		if self.result==None:
			print "self.result is None"
			return
			
		
		#print "******************"
		self.headers=headers
		# get column data
		self.dataMatrix=self.D.get_data(headers).transpose()   # transpose matrix such that it gives column rows, to easily select XYZ values
		
		dial= DialogBox( self.root,self.headers, "Choose the axes")
		self.result=dial.Result()
		self.LRdata=self.result
		print "#*		  result   :",self.result
		if self.result==[]:
			print "terminate"
			return
		
		
		# change axes labels
	   
		self.xx="X- : "+self.result[0]
		self.yx="Y- : "+self.result[1]
		self.zx="size: "+self.result[2]+", Color:  "+self.result[3]

	def buildPoints(self, event=None):
		# reset booleans
		self.build=False
		self.built=False
			
		
	
		self.line=None
		self.clearData() # clear canvas op objects, reset it

		self.shape=self.var.get()	# get variable value of option menu 
		self.colorX=self.varC.get()
		
		mtx=self.D.get_data(self.headers).transpose() # get matrix data for this matrix

		# create zeros list, and 1's list
		self.W=ones = np.asmatrix(np.ones( (mtx.shape[1]) ))
		zeros = np.asmatrix(np.zeros( (mtx.shape[1]) ))
		self.X=mtx[self.D.get_num(self.result[0])]
		self.Y=mtx[self.D.get_num(self.result[1])]
		
		#print "	 self.x ,  self.y  ",self.X,"\n \n \n	  ",self.Y
		self.Z=mtx[self.D.get_num(self.result[2])] # Z axis
		self.clrmtx=mtx[self.D.get_num(self.result[4])]	   # color axis
		print "category ",self.result[4]
		self.szx=mtx[self.D.get_num(self.result[3])]	   # size axis
		self.pointsMTX=np.concatenate((self.X,self.Y,self.Z), axis=0)
		column_max=np.matrix(self.pointsMTX.max(1))
		column_min=np.matrix(self.pointsMTX.min(1)) 
		range=column_max-column_min
		nomalized=(self.pointsMTX-column_min)/range
		nomalized=np.concatenate((nomalized,ones), axis=0) # add ones column
		self.pointsMTX=np.matrix(nomalized).transpose()
		
		# build vtm
		vtm=self.v.build()
		pts = (vtm * self.pointsMTX.transpose()).transpose()   # very important matrix
		
		
		
		# normalizing for color axis
			
		column_max=np.matrix(self.clrmtx.max())
		column_min=np.matrix(self.clrmtx.min())
		self.mx=float(column_max[0])
		self.mn=float(column_min[0])
		self.r=self.mx-self.mn
		
		# normalizing for size axis, this does not change
		column_max=np.matrix(self.Z.max())
		column_min=np.matrix(self.Z.min())
		self.mxs=float(column_max[0])
		self.mns=float(column_min[0])
		self.rs=self.mxs-self.mns
		
		
		
		pts=pts.transpose()
		self.zm=np.matrix(self.szx)
		
		# color axis parameters
		self.mn=self.zm.min()
		self.mx=self.zm.max()
		self.rs=self.mx-self.mn
		self.clr=np.matrix(self.clrmtx)
		self.mnc=self.clr.min()
		self.mxc=self.clr.max()
		self.rc=self.mxc-self.mnc
		
		self.mk=np.concatenate((pts,self.zm,self.clr), axis=0)

		self.points=pts.tolist()
		
		self.mk=self.mk.transpose()
		
	
		self.points=self.mk.tolist()
		
		#* create temporary fields to hold Z, color and size data
		self.sz=[]
		self.cl=[]
		self.zee=[]
		
		#print "points \n",self.points
			
		# draw the points onto the canvas
		for row in self.points: # self.ponts has rows which are 5 dimensional
			
			if len(row)>3:
				#print "*****************  row"
				x=float(row[0])
				y=float(row[1])
				z=float(row[2])
				
				size=((float(row[4])-self.mn)/self.rs)*5
				
				#print "color :",color
			
				# store temp values
				self.zee.append(z)
				
				
				# color ID
				if self.clust==True:
					print "length  :",len(row)
					print "  ID  ",int(row[5])
					color=self.colors[int(row[5])-1]
					print " color  :",color
					# all same size so
					size=5
					
				
					
				else:
					color=int(((float(row[5])-self.mnc)/self.rc)*255)%250
				# add to non-spatial lists for tranformations
				self.cl.append(color)
				self.sz.append(size)
				#print "color A:	 ",color
			else:
				#print "row values:	  ",row
				print "*****************   unsuccesful "
				return
			
			
			
				
			if self.clust==True:
					mycolor=color
			else:
				# using red-green color axis from Maxwell's notes, I calculate the colors
				if self.colorX=="Red-Green":
					mycolor = '#%02x%02x%02x' % (color, 0, 255-color)
				else:
					mycolor = '#%02x%02x%02x' % (255-color, 255-color, color)
				
			if self.shape=="circle":
				print "size :",size
				point=self.canvas.create_oval(x-size,y-size,x+size,y+size , fill=mycolor,outline="")
				self.objects.append(point)
			if self.shape=="square":
				point=self.canvas.create_rectangle(x-size,y-size,x+size,y+size , fill=mycolor,outline="")
				
				self.objects.append(point)
		
		
		ix=1
		xi=int(900) # width x-position
		yi=66 # height y-position
		for country in self.countries:
			c=tk.Label(self.canvas,text=self.countries[ix-1])
			c.place(x=xi,y=yi)
			print "color  :",self.colors[ix-1]
			point=self.canvas.create_oval(xi+10,yi+10,xi-10,yi-10,fill=self.colors[ix-1],outline="")
			yi+=40
			ix+=1

		self.sz=np.matrix(self.sz).transpose()
		self.cl=np.matrix(self.cl).transpose()
		self.zee=np.matrix(self.zee).transpose()
		#print "*********** \n self.zee:	 \n",self.zee,"\n ************"
		
		# make builpoints boolean true
		self.build=True
	
	def updatePoints(self):
		
	
		self.shape=self.var.get()	# get variable value of option menu 
		
		if len(self.objects) == 0:
			return
			
		for pt in self.objects: # remove points from display
			self.canvas.delete(pt)
		
		
		vtm=self.v.build()
		
		
		pts = (vtm * self.pointsMTX.transpose()).transpose()
		self.pts=pts # pts field
		pts=pts.transpose() # new points
		vxw=np.concatenate((self.zee,self.sz,self.cl), axis=1)
		#print "shape pts	vxw	 ",pts.shape,"	 ",vxw.shape
		pts=np.concatenate((pts,vxw.transpose()), axis=0).transpose()
		#print "*********** \n pts after:	 \n",pts.shape ,"\n ************"
		self.points=pts.tolist()
		
		
		for row in self.points:
			if len(row)>3:
				#print "*****************  row"
				x=float(row[0])
				y=float(row[1])
				size=row[-2]		# make y values color and size axis for fun
				#print "	   x:	",float(row[0])
				color=row[-1]
                #print "row:	 ",row
				
				
			
			else:
				#print "row values:	  ",row
				print "*****************   unsuccesful "
				return
		
		
			if self.clust==True:
				mycolor=color
				#print "color :",type(color),"		",color
				size=int(size)
				#print "size :",type(size),"			 ",size
			else:
				# using red-green color axis from Maxwell's notes, I calculate the colors
				if self.colorX=="Red-Green":
					mycolor = '#%02x%02x%02x' % (color, 0, 255-color)
				else:
					mycolor = '#%02x%02x%02x' % (255-color, 255-color, color)
			
			
			if self.shape=="circle":
				point=self.canvas.create_oval(x-size,y-size,x+size,y+size , fill=mycolor,outline="")
				self.objects.append(point)
			if self.shape=="square":
				point=self.canvas.create_rectangle(x-size,y-size,x+size,y+size , fill=mycolor,outline="")
				self.objects.append(point)

		
			
	def resize(self, event):
		h=float(self.initDy)
		
		if event.width>event.height:
			
			h=float(event.height)
			self.winscale=float(h/self.initDy)
			self.scale=self.winscale
			self.v.extent=self.v.extent/self.scale
			self.updateAxes()
			self.updatePoints()
			self.initDy=float(event.height)
			self.initDx=float(event.width)
			
		else:
			
			h=float(event.width)
			self.winscale=float(h/self.initDx)
			self.scale=self.winscale
			self.v.extent=self.v.extent/self.scale
			self.updateAxes()
			self.updatePoints()
			self.initDy=float(event.height)
			self.initDx=float(event.width)
			
	#### project 5 code 
	 
	def handleLinearRegression(self):
		
		if self.build==False:
			print "\n \n \n *******	 ERROR	 ********"
			print ">   please plot the data first, before building a regression"
			return
		
		if self.built==True:
			print "#*	 regression line aleardy built"
			return
				
		self.headers=self.D.get_headers()
		#print "#######		   headers:", self.headers
		# create x and y values list
		
		if self.headers==[]:
			print "your list is empty"
			return
			
		
		
		
		
		
		self.clearData()
		
		self.RegObjects=[]
		
		self.updateAxes()
		
		self.buildLinearRegression()
		
		self.built=True
		
		print "*********************** \n done building regression line"
		
	def buildLinearRegression(self):
		x=self.LRdata[0]
		y=self.LRdata[1]
		
		
		mtx=self.D.get_data(self.headers).transpose() # get matrix data for this matrix

		# create zeros list, and 1's list
		self.W=ones = np.asmatrix(np.ones( (mtx.shape[1]) ))
		zeros = np.asmatrix(np.zeros( (mtx.shape[1]) ))
		self.rawX=mtx[self.D.get_num(x)]
		self.rawY=mtx[self.D.get_num(y)]
		
		#print "raw X	 raw Y	:", self.rawX,"\n \n ",self.rawY
		
		
			
		
		
		# data analysis variables
		self.xmean=np.mean(self.rawX)
		#print "x mean:",self.xmean
		self.ymean=np.mean(self.rawY)
		#print "y mean:",self.ymean
		self.xstdev=np.std(self.rawX)
		#print "xstdev:",self.xstdev
		self.ystdev=np.std(self.rawY)
		#print "ystdev:",self.ystdev
		
		self.medx=float(np.median(self.rawX, axis=1, overwrite_input=False))
		#print "medx:",self.medx
		self.medy=float(np.median(self.rawY, axis=1, overwrite_input=False))
		self.analtxt="	\n mean [x,y] : ["+str(self.xmean)+" ,"+str(self.ymean)+"] \n stdev [x,y] :	 ["+str(self.xstdev)+", "+str(self.ystdev)+"] \n median [x,y]: [ "+str(self.medx)+", "+str(self.medy)+" ]"
		#print "see: ",self.analtxt
		
		
		
		

		# normalizing the columns
		self.X=self.normalize(self.rawX)
		self.Y=self.normalize(self.rawY)

		self.mk=np.concatenate((self.X,self.Y, zeros, self.W), axis=0)	# allvalues normalized
		
		self.pointsMTX=self.mk.transpose()
			
		vtm=self.v.build()
		pts=(vtm*self.pointsMTX.transpose()).transpose()
		#print "*********** \n pts:	 \n",pts,"\n ************"
		
		vxw=np.concatenate((self.zee,self.sz,self.cl), axis=1)
		
		#print "vxw: \n",vxw
		
		print "pts vxw shape  :",pts.shape,"	",vxw.shape
		
		pts=np.concatenate((pts.transpose(),vxw.transpose()), axis=0).transpose()
		print "*********** \n pts after:	 \n",pts.shape ,"\n ************"
		self.points=pts.tolist()
		
		#print "points \n",self.points
		
		
		#print "\n \n self.mk		\n",self.mk
		#print "max, min:	",self.mn,self.mx
		# draw points
		for row in self.points:
			if len(row)>3:
				#print "*****************  row"
				x=float(row[0])
				y=float(row[1])
				size=row[-2]		# make y values color and size axis for fun
				#print "	   x:	",float(row[0])
				color=row[-1]
				#print "color B:	 ",color
				
			else:
				#print "row values:	  ",row
				print "*****************   unsuccesful "
				return
			
			
			# using red-green color axis from Maxwell's notes, I calculate the colors
			if self.colorX=="Red-Green":
				mycolor = '#%02x%02x%02x' % (color, 0, 255-color)
			else:
				mycolor = '#%02x%02x%02x' % (255-color, 255-color, color)
			if self.shape=="circle":
				point=self.canvas.create_oval(x-size,y-size,x+size,y+size , fill=mycolor,outline="")
				self.objects.append(point)
			if self.shape=="square":
				point=self.canvas.create_rectangle(x-size,y-size,x+size,y+size , fill=mycolor,outline="")
				self.objects.append(point)


		# setup regression
		slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(self.rawX, self.rawY)
		#print scipy.stats.linregress(self.rawX, self.rawY)

		#regression line information for display
		self.regtxt="\nGradient="+str(slope)+"\n"+"Y intercept="+str(intercept)+"\n"+"R-value="+str(r_value)
		self.ltxt=" Y="+str(slope)+"x+ "+str(intercept)+"\n R^2 = "+str(r_value)
		self.btxt=self.ltxt+str(self.analtxt)
		
		fnl=self.txt+self.regtxt
		self.scaleframe.config(text=fnl)
		
		list=[]
		list.append(self.LRdata[0])
		list.append(self.LRdata[1])
		#print "list: ", list
		
		# find ranges
		rng=analysis.range(list, self.D)
		
		#print "range  : ",rng
				
		# normalized points
		ymxrng=rng[1][1]-rng[1][0]
		ymn=(((rng[0][0]*slope)+intercept)-rng[1][0])/(ymxrng)
		ymx=(((rng[0][1]*slope)+intercept)-rng[1][0])/(ymxrng)
		
		# matrix of endpoints for line
		ln=np.matrix([[0,ymn,0,1],[1,ymx,0,1]])
		#print "ln	 :",ln
		self.axes=np.concatenate((self.axes, ln), axis=0)
	
		# build vtm and then find final points
		vtm=self.v.build()
		self.lnpts=(vtm*ln.transpose()).transpose()
		
		#print "line points :",self.lnpts
		
		xy=self.lnpts.tolist()
		
		# create the best fit line
		mycolor = '#%02x%02x%02x' % (255, 0, 100)
		self.line=self.canvas.create_line(xy[0][0], xy[0][1],xy[1][0],xy[1][1], fill=mycolor)

		canvas_id = self.canvas.create_text(10, 10, anchor="nw")
		
		self.canvas.itemconfig(canvas_id, text="line data \n")
		self.canvas.insert(canvas_id, 12, self.btxt)

	# normalizes a row
	def normalize(self,row):
	
		column_matrix=row
		column_max=column_matrix.max()
		column_min=column_matrix.min()
		range=column_max-column_min
		nomalized=(column_matrix-column_min)/range
		return nomalized

	def save(self):
		self.canvas.postscript(file="file1.ps", colormode='color')
		print "#*	Your canvas was saved as 'file1.ps'	 "
		return

	def main(self):
		print 'Entering main loop'
		self.root.mainloop()

#########

class Dialog(tk.Toplevel):
	
	def __init__(self, parent,headers ,title = None):
		
				
		# headers field, for options
		self.headers=headers
		
		tk.Toplevel.__init__(self, parent)
		self.transient(parent)
		
		if title:
			self.title(title)
		
		self.parent = parent
		
		self.result = None
		
		body = tk.Frame(self)
		self.initial_focus = self.body(body)
		body.pack(padx=5, pady=5)
		
		self.buttonbox()
		
		self.grab_set()
		
		if not self.initial_focus:
			self.initial_focus = self
		
		
		self.protocol("WM_DELETE_WINDOW", self.cancel)
		
		self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
								  parent.winfo_rooty()+50))
			
		self.initial_focus.focus_set()	
		self.wait_window(self)

	#
	# construction hooks


	def body(self, master):
		# create dialog body.  return widget that should have
		# initial focus.  this method should be overridden

		pass

	def buttonbox(self):
		# add standard button box. override if you don't want the
		# standard buttons

		box = tk.Frame(self)
			
		# listbox
		#tk.Listbox(master, selectmode=tk.SINGLE, exportselection=0)
		
		x=tk.Label(box,text="Select: X ", state=tk.ACTIVE)
		x.pack(side=tk.LEFT)
		
		
		self.xHeader=tk.StringVar(box)
		self.xHeader.set(self.headers[0])
		xMenu=tk.OptionMenu(box, self.xHeader, *self.headers)
		xMenu.pack(side=tk.LEFT)
		
		###
		x=tk.Label(box,text="Y", state=tk.ACTIVE)
		x.pack(side=tk.LEFT)
		
		
		self.yHeader=tk.StringVar(box)
		self.yHeader.set(self.headers[1])
		yMenu=tk.OptionMenu(box, self.yHeader, *self.headers)
		yMenu.pack(side=tk.LEFT)
		
		###
		x=tk.Label(box,text="Z", state=tk.ACTIVE)
		x.pack(side=tk.LEFT)
				
				
		self.zHeader=tk.StringVar(box)
		self.zHeader.set(self.headers[1])
		yMenu=tk.OptionMenu(box, self.zHeader, *self.headers)
		yMenu.pack(side=tk.LEFT)
		
		###
		x=tk.Label(box,text="size", state=tk.ACTIVE)
		x.pack(side=tk.LEFT)
		
		
		self.sHeader=tk.StringVar(box)
		self.sHeader.set(self.headers[0])
		cMenu=tk.OptionMenu(box, self.sHeader, *self.headers)
		cMenu.pack(side=tk.LEFT)

		###
		x=tk.Label(box,text="color", state=tk.ACTIVE)
		x.pack(side=tk.LEFT)

		self.cHeader=tk.StringVar(box)
		self.cHeader.set(self.headers[0])
		cMenu=tk.OptionMenu(box, self.cHeader, *self.headers)
		cMenu.pack(side=tk.LEFT)

		
		
		
		#button

		n = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
		n.pack(side=tk.LEFT, padx=5, pady=5)
		w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=tk.LEFT, padx=5, pady=5)
		
		
		self.bind("<Return>", self.ok)
		self.bind("<Escape>", self.cancel)

		box.pack()
		
	
		#####		return 1 # override

	
	def ok(self, event=None):
		
		
		
		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return
		
		self.result=[self.xHeader.get(),self.yHeader.get(),self.zHeader.get(),self.sHeader.get(),self.cHeader.get()]
		
		
		print "selection:	 ",self.result
		
		self.withdraw()
		self.update_idletasks()

		self.apply()

		self.cancel()
	
	
	
		

		
		
		

	def cancel(self, event=None):
		
		# put focus back to the parent window
		#self.parent.focus_set()
		self.result=[self.xHeader.get(),self.yHeader.get(),self.zHeader.get(),self.sHeader.get(),self.cHeader.get()]
		self.destroy()

	#
	# command hooks

	def validate(self):

		return 1 # override

	def apply(self):

		pass # override


#########
	
class DialogBox(Dialog):
	
	
	
	# I do not override bidy here, all listbox code in dialog box

	# variables X and Y are the y-co-ordinates distribution selected 
	def apply(self):
		
		print " you just clicked " # or something

	def Result(self):
		
		#print "done		", self.result[0],"		and ",self.result[1] 
		return self.result

class PCABox(Dialog):
	
	def buttonbox(self):
		box = tk.Frame(self)
		
		
		
		self.var = []

		for header in self.headers:
			q=tk.IntVar()
			self.var.append(q )
			c = tk.Checkbutton(box, text=header, variable=self.var[-1])
			c.pack()
			
		
		print "#*	  loop done"
	
		w = tk.Button(box, text="OK", width=10, command=self.ok)
		w.pack(side=tk.BOTTOM, padx=5, pady=5)
		w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=tk.BOTTOM, padx=5, pady=5)

		box.pack()
	
	def Result(self):
	
		print "your result	:",self.result
		return self.result

	def cancel(self, event=None):
		print "Cancelled"
		# put focus back to the parent window
		#self.parent.focus_set()
		self.result=None
		self.destroy()

	def ok(self, event=None):
	
	
		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return
		
		
		
		
		
		
		#result is all the ticked checkboxes
		index=0
		index=0
		self.result=[]
		for header in self.headers:
			if self.var[index].get()==1:
				#return all the ticked headers
				self.result.append(header)
			index=index+1
		print "selection:	 ",self.result
		self.destroy()
		
		
class DialogBox(Dialog):
	
	
	
	# I do not override bidy here, all listbox code in dialog box

	# variables X and Y are the y-co-ordinates distribution selected 
	def apply(self):
		
		print " you just clicked " # or something

	def Result(self):
		
		#print "done		", self.result[0],"		and ",self.result[1] 
		return self.result

class ClusterBox(Dialog):
	
	def buttonbox(self):
		box = tk.Frame(self)

		self.var = []
		
		

		for header in self.headers:
			q=tk.IntVar()
			self.var.append(q )
			c = tk.Checkbutton(box, text=header, variable=self.var[-1])
			c.pack()
			
		# add scale for the number of clusters to create
		
		self.number=tk.StringVar(box)
		self.number.set(4)
		print "value : ", self.number.get()
		xMenu=tk.OptionMenu(box, self.number, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
		xMenu.pack()
		
		"""
		self.number = tk.Scale(box, from_=0, to=15, orient=tk.HORIZONTAL)
		self.number.set(2)
		self.number.pack()"""
	
		w = tk.Button(box, text="OK", width=10, command=self.ok)
		w.pack(side=tk.BOTTOM, padx=5, pady=5)
		w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
		w.pack(side=tk.BOTTOM, padx=5, pady=5)

		box.pack()
	
	def Result(self):
	
		print "your result	* :",self.result,"	 ", self.numclusters
		
		if self.result==None:
			return None
		
		return self.result, self.numclusters

	def cancel(self, event=None):
		print "Cancelled"
		# put focus back to the parent window
		#self.parent.focus_set()
		self.result=None
		self.destroy()

	def ok(self, event=None):
	
	
		if not self.validate():
			self.initial_focus.focus_set() # put focus back
			return
		
		
		
		
		
		
		#result is all the ticked checkboxes
		index=0
		index=0
		self.result=[]
		for header in self.headers:
			if self.var[index].get()==1:
				#return all the ticked headers
				self.result.append(header)
			index=index+1
		print "value *:",self.number.get()
		x=int(self.number.get()) # cast string to int
		print "value *:",x
		self.numclusters=x
		print self.numclusters
		
		#print "selection:	 ",self.result
		self.destroy()



if __name__ == "__main__":
	dapp = DisplayApp(1200, 675)
	dapp.main()


