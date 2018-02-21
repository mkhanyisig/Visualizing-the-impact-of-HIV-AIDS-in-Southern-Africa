#Mkhanyisi Gamedze
# CS 251 - Spring 2017
# project 6

import csv
import sys
import numpy as np
import analysis
import random as rand
import os


class Data:

	# initialize the object
	def __init__(self, filename = None):
		

		# fields
		
		#
		# create and initialize fields for the class
		self.raw_headers=[] # (list of all headers)
		self.raw_types=[] # (list of all types)
		self.num_data=[]  # (list of lists of all data, for numeric types. Each row is a list of strings)
		self.row_data=[]  # (list of lists of all data. Each row is a list of strings)
		self.header2raw={}	# (dictionary mapping header string to index of column in raw data)
		self.matrix_data=np.matrix([]) # matrix that  holds all our raw data
		self.matrix_dataNum=np.matrix([]) # matrix that	 holds all our raw data
		self.header2matrix={} # 
		self.type2num={}
		self.nonNum=[] #  same role as header 2 matrix, but for all num-types
		self.header2rowNum={}	# (dictionary mapping header string to index of column in only Numeric data)
		self.header2matrixNum={} #	map headers to matrix data for numeric final data 

		# if filename is not None
		if filename!=None:
			# call self.read(filename)
			self.filename=filename
			self.read()
		else:
			print " Error: the filename you entered does not exist"
			return


	def read(self):
		dataFile= file(self.filename,"rU")
		lines=dataFile.readlines()
		dataFile.close()
		data=csv.reader(lines) # contains all the lines of the CSV file
		self.row_headers=data.next() # moves to first raw and returns those values
		self.row_types=data.next() # second row is the types, so getting the next row should give us the types from the CSV file
		self.matrixAll=[]
		#print " raw headers:  ", self.row_headers
		self.raw_rows=[] # list of lists that will contain	all the raw rows, not selective of types 
		self.rows=[] # lists of lists contains the rows of only the numeric types
		
		#  create dictionary for the raw data types, please excuse the confusing naming of variables. The code works
		for i in range(len(self.row_types)):
			self.type2num[i]= self.row_types[i]
		
		# create a matrix that supports even non-Numeric type
		for item in data: # item is the specific row list, containing all the strings in the row
			list=[] 
			for i in range(len(item)):
				list.append(item[i])		
			self.row_data.append(item)
			self.raw_rows.append(list)
			self.matrixAll.append(list) # add to the matrix that contains all the raw data, not selective of types
			# print "1 works"
		
		# I duplicate the code at the top, as my second forloop below could not work without doing this, for the only numeric data
		dataFile= file(self.filename, "rU")
		lines=dataFile.readlines()
		dataFile.close()
		data=csv.reader(lines) # contains all the lines of the CSV file
		self.raw_headers=data.next() # moves to first raw and returns those values
		self.raw_types=data.next() # second row is the types, so getting the next row should give us the types from the CSV file
		self.matrix=[]
		""" Second forloop builds matrix of only numeric data """
		
		for item in data: # item is the specific row list, containing all the strings in the row
			list=[] 
			for i in range(len(item)):
				try:	
					x=float(item[i]) # cast to float and then append
					list.append(x)
				except ValueError:
					#print "Not a float, Row ",i
					self.nonNum.append(i)
			self.num_data.append(list) # add the list to the list-of-lists
			self.rows.append(list) # list of the Numeric data values by	 rows
			self.matrix.append(list)
			
			
		#print "There are ", len(self.nonNum)," columns with non-Numeric data types, which we need to eliminate", self.nonNum
		
		m=0
		
		
		
		self.raw_types=[]
		self.raw_headers=[]
		
		#print "	   <row types>	 ",self.row_types 
		print "Non numeric column headers"
		#print " types",self.row_types
		for type in range(len(self.row_types)):
			
			if self.row_types[type]=="numeric" : # add that column data to both the headers list and the types list
				#print " numeric type exists",	type
				self.raw_types.append(self.row_types[type])
				self.raw_headers.append(self.row_headers[type])
			elif self.row_types[type]==' numeric' : # add that column data to both the headers list and the types list
				#print " numeric type exists",	type
				self.raw_types.append(self.row_types[type])
				self.raw_headers.append(self.row_headers[type])
			
			else : # remove it from both the headers list and the types list
				# do nothing
				#print "#*	",self.row_headers[type]
				pass
		
		
		
		
		self.matrix_data=np.matrix(np.matrix(self.matrixAll))
		self.matrix_dataNum=np.matrix(self.matrix)
		
		#create dictionaries for the raw and row data
		# Enter all the data types here 
		for j in range(len(self.row_headers)):
			self.header2raw[self.row_headers[j]]=j
			self.header2matrix[self.row_headers[j]]=j
		
		# only numeric types here	
		for j in range(len(self.raw_headers)):
			self.header2rowNum[self.raw_headers[j]]=j
			self.header2matrixNum[self.raw_headers[j]]=j
			
		print "####### done creating data object and reading in values"
	
	# already did something similar in my previous project, so slight modification of that	
	def write(self, filename, headers=None):
	
		if headers==None:
			headers=self.raw_headers
		#create a temporary csv file that holds the data
		print "#* shape :",self.matrix_dataNum.shape
		with open(filename+'.csv', 'wb') as f:
			writer = csv.writer(f)

			#write in my headers
			list=[]
			list.append(headers)
			writer.writerows(list)

			#write in the types
			types=[]
			values=[]
			for item in headers:
				index=0
				for head in self.get_raw_headers():
					if item==head:
						types.append(self.get_raw_type()[index])
						column=[]
						for i in range (len(self.row_data)-1):
							v=self.matrix_dataNum[i].tolist()
							values.append(v[0])
					index+=1
			
			
			list=[]
			list.append(types)
			writer.writerows(list)
			writer.writerows(values) # write in all the rows

		f.close()
			
	# accessor methods
	
	""" access Raw data"""
	def get_raw_headers(self):	 # returns a list of all of the headers.
		return self.row_headers
	
	def get_raw_type(self): # returns a list of all of the types.
		return	self.row_types
	
	def get_raw_num_columns(self): # returns the number of columns in the raw data set
		return len(self.row_headers) # this row contains all the headers, and so its length should give the total number of columns
	
	def get_raw_num_rows(self):	 # returns the number of rows in the data set. This should be identical to the number of rows in the numeric data, so you can get away with writing just one function for this purpose.
		return	len(self.row_data) # self.raw_data is the list of lists of all our data, and so this should give the total number of rows
		
	def get_raw_row(self, Rindex): # returns a row of data (the type is list) given a row index (int).
		
		return self.raw_rows[Rindex]
		
	def get_raw_value(self, Rindex, column_header ): #	takes a row index (an int) and column header (a string) and returns the raw data at that location. (The return type will be a string)
		return self.row_data[Rindex][self.header2raw[column_header]]
	
	def printMatrix(self):
		print self.matrix_data
	
	""" access numeric Row data"""
	
	def get_headers(self):	  # (list of headers of columns with numeric data)
		return self.raw_headers
		
	def get_type(self):	  # (list of headers of columns with numeric data)
		return self.raw_types
		
	def get_num_columns(self): # returns the number of columns of numeric data
		return len(self.raw_headers)
		
	def get_num_rows(self): # should return same value as get_raw_num_rows()
		return len(self.row_data)
		
	def get_row(self, Rindex):	# take a row index and returns a row of numeric data
		return self.rows[Rindex]
	
	def get_value(self, Rindex, column_header ):   # takes a row index (int) and column header (string) and returns the data in the numeric matrix.
		return self.num_data[Rindex][self.header2rowNum[column_header]] 
	
	def get_num(self,column_header ):	# takes a column header (string) and returns the column number
		return self.header2rowNum[column_header]
	
	def get_data(self, headers):  
		""" At a minimum, this should take a list of columns headers and return a 
		matrix with the data for all rows but just the specified columns. 
		It is optional to also allow the caller to specify a specific set of rows."""
		#excuse the many 
		# build list of headers
		positions=[]
		#print "headers :",headers
		for i in range(len(headers)):
			if headers[i] in self.header2rowNum.keys(): 
				positions.append(self.header2rowNum[headers[i]]) # buil up a list of the positions to be selected
			else:
				pass
		column_data=[]
		matrix=[]
		print "len :",len(positions)
		v=self.matrix_dataNum
		v=v.tolist()
		
		for position in positions:	 # collect all column from each row, build up matrix and the return it
			#print "position:  ",position
			for row in v:
				if position>=len(row):
					return
				
				#print row
				
				#print "	  :",position,"	  ",len(row),"     ",row
				column_data.append(row[position])
			matrix.append(column_data)	
			column_data=[] # make the list empty again, for second position
		print len(matrix[0])
		if len(matrix[0])<=1:
			result=np.matrix(matrix[0])
		else:
			result=np.matrix(matrix)
		
		result.transpose() 
		result=result.getT()
		
		return result

	
		
	def print_Num_Matrix(self):
		print self.matrix_dataNum
		
	def get_Num_Matrix(self):	# returns matrix with data in rows 
		return self.matrix_dataNum.transpose()
		
	####### Extensions ####
	
	def add_column(self, data):
		"""
		print "\n \n intial headers list:  \n ",self.raw_headers
		print "\n types: \n ",self.raw_types
		print "\n \n The matrix intially:  \n",self.matrix_data
		print "\n \n your list of columns: \n  ",self.matrixAll
		"""
		# add header to raw headers list
		self.row_headers.append(data[0])
		# add type to raw types list
		self.row_types.append(data[1])

		""" add to numeric data if numeric"""
		if type=="numeric":	 
			# add header to headers list
			self.raw_headers.append(data[0])
			# add type to types list
			self.raw_types.append(data[1])
			
			
	# taks in header, type and list of values to be added to the original numeric data matrix
	def add_datacolumn(self,header ,type,  list, original):
		
		self.row_types.append(type)
		self.row_headers.append(header)
		if type=="numeric":	 #""" add to numeric data """
			print "**  adding numeric column"
			
			self.matrix_dataNum=original.tolist()
			
			print "size original :",len(self.matrix_dataNum[0])
			
			length=len(self.matrix_dataNum[0]) # find out the number of columns
			
			print "number  of columns of the matrix: ",length
			print "list length ", len(self.matrix_dataNum)
			
			
			# add values to matrix data
			for i in range(len(self.matrix_dataNum)):
				#print "your i:	  ",i
				self.matrix_dataNum[i].append(list[i].item(0)) # add element to each row
				
			
			
			
			
			self.matrix_dataNum=np.matrix(self.matrix_dataNum)
			print "***	shape : ",self.matrix_dataNum.shape
			
			return self.matrix_dataNum
			
	def add_datacolumnB(self, header, type, list):
		"""
		print "\n \n intial headers list:  \n ",self.raw_headers
		print "\n types: \n ",self.raw_types
		print "\n \n The matrix intially:  \n",self.matrix_data
		print "\n \n your list of columns: \n  ",self.matrixAll
		"""
		# add header to raw headers list
		self.row_headers.append(header)
		# add type to raw types list
		self.row_types.append(type)
		#print "column :", list
		
		if type=="numeric":	 #""" add to numeric data """
			print "**  adding numeric column"
			# add header to headers list
			self.raw_headers.append(header)
			# add type to types list
			self.header2rowNum[header]=(len(self.raw_headers)-1)
			
			self.matrix_dataNum=self.matrix_dataNum.tolist()
			
			length=len(self.matrix_dataNum[0]) # find out the number of rows
			
			print "number  of columns of the matrix: ",length
			print "list length ", len(self.matrix_dataNum)
			#print "** type :", type(self.matrix_dataNum[0])
			
			# add values to matrix data
			for i in range(len(self.matrix_dataNum)):
				#print "your i:	  ",i
				self.matrix_dataNum[i].append(list[i].item(0)) # add element to each row
				#print self.matrix_dataNum[i]
				
				
			
			
			self.matrix_dataNum=np.matrix(self.matrix_dataNum)
			print "***	shape : ",self.matrix_dataNum.shape
			

# inherits the data objec
class PCAData(Data):
	
	# initialize the object
	def __init__(self,headers,pdata,evals,evecs,means):
		# fields
		print "Begin PCA analysis:	 "
		self.eigenvalues=evals
		#print self.eigenvalues
		self.eigenvectors=evecs
		#print "*****	eigen vectors:	",self.eigenvectors
		self.mean=means
		#print self.mean
		self.headers=headers
		self.raw_headers=headers
		#print self.headers
		
		self.pdata=pdata
		#print self.pdata
		self.raw_data=pdata.tolist()
		#print "#........#"
		
		
		
		
		
		
		# create a temporary csv file to hold the PCA data, so it can be put onto the Data instance
		with open('apcatemp.csv', 'wb') as df:
			writer = csv.writer(df)

			
			""" first create headers of PCA and then write onto csv file"""
			#change raw_headers to Pdata0+i
			self.raw_headers=[]
			for i in range(0,len(self.headers)):
				st="PCAdata0"+str(i)
				self.raw_headers.append(st)
			self.headers=self.raw_headers
			
			# headers list
			list=[]
			list.append(self.headers)
			
			writer.writerows(list)
				
			""" add numeric PCAdata types"""
			# all projected data should be numeric, add numeric types onto CSV
			#write the types(all "numeric")
			list=[]
			l=[]
			for i in range(len(self.headers)):
				l.append("numeric")
				i=i+1
			list.append(l)

			writer.writerows(list)
			
			
			"""	write the data for each row """
			list=[]
			print " shape evec :",self.eigenvectors.shape
			print "shape pdata  :",self.pdata.shape
			for i in range (0,self.pdata.shape[0],1):
				l=[]
				for j in range (0,self.pdata.shape[1],1):
					l.append(str(self.pdata[i,j]))
				list.append(l)
			writer.writerows(list)
			df.close() # done creating the CSV file

			#send the temp file to read, create all the necessary fields
			Data.__init__(self,filename="apcatemp.csv")
		
		#os.remove("temporary.csv") #delete the temporary file
		
		#change raw_headers to Pdata0+i
		self.raw_headers=[]
		for i in range(0,len(self.headers)):
			st="PCAdata0"+str(i)
			self.raw_headers.append(st)
		self.headers=self.raw_headers
		
		# update headers dictionary
		for j in range(len(self.row_headers)):
			self.header2raw[self.row_headers[j]]=j
			self.header2matrix[self.row_headers[j]]=j
		
		
		
		# only numeric types here	
		for j in range(len(self.raw_headers)):
			self.header2rowNum[self.raw_headers[j]]=j
			self.header2matrixNum[self.raw_headers[j]]=j
			
		
		
			
	def get_eigenvalues(self):
		return np.asmatrix(self.eigenvalues)
	def get_eigenvectors(self):
		return np.asmatrix(self.eigenvectors)
	def get_data_means(self):
		return np.asmatrix(self.mean)
	def get_data_headers(self):
		return np.asmatrix(self.headers)
	def get_headers(self):
		return self.headers	
	
	def get_newheaders(self):
		return np.asmatrix(self.raw_headers)
	def get_data(self,headers):
		return self.pdata
		
		
	def add_datacolumn(self,header ,type,  list, original):
		
		self.row_types.append(type)
		self.row_headers.append(header)
		self.headers.append(header)
		self.header2rowNum[header]=-1
		if type=="numeric":	 #""" add to numeric data """
			print "**  adding numeric column"
			
			self.matrix_dataNum=original.tolist()
			
			print "size original :",len(self.matrix_dataNum[0])
			
			length=len(self.matrix_dataNum[0]) # find out the number of columns
			
			print "number  of columns of the matrix: ",length
			print "list length ", len(self.matrix_dataNum)
			
			
			# add values to matrix data
			for i in range(len(self.matrix_dataNum)):
				#print "your i:	  ",i
				self.matrix_dataNum[i].append(list[i].item(0)) # add element to each row
				
			
			
			
			
			self.matrix_dataNum=np.matrix(self.matrix_dataNum)
			print "***	shape : ",self.matrix_dataNum.shape
			
			return self.matrix_dataNum


		
		









	

		
		
		
		
		
		
			
		
		
		
			