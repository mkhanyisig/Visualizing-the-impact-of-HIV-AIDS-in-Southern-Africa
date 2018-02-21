# Template by Bruce Maxwell
# Spring 2015
# CS 251 Project 8
#
# Classifier class and child definitions

import sys
import data
import analysis as an
import numpy as np
import math
import analysis
import scipy.cluster.vq as vq
import scipy


class Classifier:

	def __init__(self, type):
		'''The parent Classifier class stores only a single field: the type of
		the classifier.	 A string makes the most sense.

		'''
		self._type = type

	def type(self, newtype = None):
		'''Set or get the type with this function'''
		if newtype != None:
			self._type = newtype
		return self._type

	def confusion_matrix( self, truecats, classcats ):
		'''Takes in two Nx1 matrices of zero-index numeric categories and
		computes the confusion matrix. The rows represent true
		categories, and the columns represent the classifier output.

		'''
		print "***** true :",truecats.shape
		print "***** class :",classcats.shape
		
		t=truecats.tolist()
		c=classcats.tolist()
		print " lengths   :",truecats.shape,"     ",len(t)
		
		print " shape ",len(t)
		print "	 shape 2 ",len(c)
		
		# concatenate both matrices then find the reduced unique matrice
		all_cats=[] 
		bc=[]
		for cat in truecats:  
			all_cats.append(int(cat[0,0]))  
		for c_cat in classcats:	 
			all_cats.append(int(c_cat[0,0]))
			bc.append(c_cat[0,0])

		# get unique list of cats, eliminate duplicates
		all_cats=np.unique(all_cats).tolist()
		b=np.unique(bc).tolist()
		#print " unique",all_cats
		#print " ####    class cat unique",b,"#####"
		
		# number of categories
		num_cats=len(all_cats)
		print "number of categories   :",num_cats

		#confusion matrix
		matrix=np.zeros((num_cats,num_cats))
	
		#confusion matrix
		ix=0
		for l in truecats:
			row=all_cats.index(l[0,0])
			if ix>=len(c):
				return
			else:
				l2=c[ix]
				#print l2
				column=all_cats.index(l2[0])
				#print column
				matrix[row,column]+=1
				ix+=1

		""" # wrong, but I almost had it with it
		for i in range(len(truecats)):
			#print i
			if t[i][0]==c[i][0]:
				ix=all_cats.index(truecats[i][0])
				#print "t[i][0] ",t[i][0],"     c[i][0]",c[i][0]
				matrix[ix,ix]+=1
				
			else:
				ix=all_cats.index(t[i][0])
				#print "t[i][0] ",t[i][0],"     c[i][0]",c[i][0]
				iy=all_cats.index(c[i][0])
				matrix[ix,iy]+=1"""

		return matrix


	def confusion_matrix_str( self, cmtx ):
		'''Takes in a confusion matrix and returns a string suitable for printing.'''
		# using project 7 inspiration from classifier.py
		
		s= "\nConfusion Matrix for	Classifier:\n"
		s+='\n'
		s+='%10s'%("Actual->")
		for i in range(len(cmtx)):	# add category column headers for first line
			s += '%10s' % ("Class "+str(i))
		
		# add class details and probabilities from confusion matrix
		for i in range(len(cmtx)):	# write out each row of the confusion matrix
			s+='\n'
			s += '%10s' % ("Class "+str(i))
			for value in cmtx[i]: # write out all the elements of the row
				s+='%10d'% value
		return s
		
		

		

	def __str__(self):
		'''Converts a classifier object to a string.  Prints out the type.'''
		return str(self._type)



class NaiveBayes(Classifier):
	'''NaiveBayes implements a simple NaiveBayes classifier using a
	Gaussian distribution as the pdf.

	'''

	def __init__(self, dataObj=None, headers=[], categories=None):
		'''Takes in a Data object with N points, a set of F headers, and a
		matrix of categories, one category label for each data point.'''

		# call the parent init with the type
		Classifier.__init__(self, 'Naive Bayes Classifier')
		
		# store the headers used for classification
		self.headers=headers
		# number of classes and number of features
		self.num_classes=0
		self.num_features=0
		# original class labels
		self.class_labels=[] # empty list
		# unique data for the Naive Bayes: means, variances, scales (empty)
		self.mean=[]
		self.vars=[]
		self.scales=[]
		# if given data,
		if dataObj!=None:
			# call the build function
			self.build(dataObj.get_Num_Matrix(),categories)
		self.class_means=None


	def build( self, A, categories ):
		'''Builds the classifier give the data points in A and the categories'''
		
		# figure out how many categories there are and get the mapping (np.unique)
		unique, mapping = np.unique( np.array(categories.transpose()), return_inverse=True)
		
		# create the matrices for the means, vars, and scales
		self.num_classes=len(unique) # number of unique classes/categories
		self.num_features=A.shape[1] # number of columns in data matrix
		self.class_labels=unique # unique categories
		num_rows=A.shape[0]
		
		# the output matrices will be categories (C) x features (F)
		matrix=np.zeros((self.num_classes,self.num_features))
		self.means=matrix
		self.vars=matrix
		self.scales=matrix # same dimensions
		
		# compute the means/vars/scales for each class
		row_values=[] # row data for each category
		valuesnumpy=[]
		print " total categories ",categories.shape
		print "self.num_classes	   ",self.num_classes
		print " features  ",self.num_features
		print " number of rows	",num_rows
		
		for i in range(self.num_classes):
			row_values.append([]) # contains category row data
			valuesnumpy.append([]) # initially fill with None object, as a filler
			
		for i in range(num_rows): # add row values to numpy matrix
			class_mapping=mapping[i] #returns class category
			get_row=A[i,:]
			row_values[class_mapping].append(get_row) # 
		
		self.class_means=[]
		self.class_vars=[]
		self.class_scales=[]
		
		#print "valuesnumpy	   :",valuesnumpy
		for class_index,label in enumerate(unique): # break it into index, category
			#print len(row_values[0])
			valuesnumpy[ class_index]=row_values[ class_index]
			category_data= A[(unique[mapping] == label),:]
			#compute the means/vars/scales for each class
			mean=np.mean(valuesnumpy[class_index], axis=0)
			var=np.var(category_data, axis=0,ddof=1)
			scale=np.asmatrix((1/np.sqrt(2*np.pi*var)))
			#print "scale	 :",scale

			# store any other necessary information: # of classes, # of features, original labels
			self.means=np.matrix(mean)
			self.vars=np.matrix(var)
			self.scales=np.matrix(scale)
			
			if class_index==0:
				#print "0"
				self.class_means=np.matrix(mean)
				self.class_vars=np.matrix(var)
				self.class_scales=np.matrix(scale)
			else:
				#print "  ####	  ",class_index
				#print "****** shape  ",self.class_means.shape,"	  ",type(mean)
				self.class_means=np.concatenate((self.class_means, mean), axis=0)
				self.class_vars=np.concatenate((self.class_vars, var), axis=0)
				self.class_scales=np.concatenate((self.class_scales, scale), axis=0)
		
			
		
			
		return

	def classify( self, A, return_likelihoods=False ):
		'''Classify each row of A into one category. Return a matrix of
		category IDs in the range [0..C-1], and an array of class
		labels using the original label values. If return_likelihoods
		is True, it also returns the NxC likelihood matrix.

		'''

		# error check to see if A has the same number of columns as the class means
		if A.shape[1]!=self.class_means.shape[1]:
			print "Error alert, number of columns not the same"
			return # terminate

		# class for each data point
		# a matrix of zeros that is N (rows of A) x C (number of classes)
		P = np.zeros((A.shape[0],self.num_classes))
		#P=np.asmatrix(P)
		
		
		# calculate the probabilities by looping over the classes
		#  with numpy-fu you can do this in one line inside a for loop
		"""
		# inefficient for large data sets
		index=0
		probabilities_list=[]
		for point in range(self.num_classes): # calculate probability for each point, from the row data of A 
			#print " pont : ",point
			probabilities=[]
			for feature in range(self.num_features): 
				for classindex in range(0,self.num_classes):
					if (2*self.class_vars[point]).all()==0: # avoid this as it is costly timewise, dividing by zero
						pass
					else:
						P[:,point]=np.prod(np.multiply(self.class_scales[point,:],np.exp(-np.square(A-self.class_means[point,:])/(2*self.class_vars[point]))),axis=1)
						#print P[:,point]
		"""
		
		# solution to time efficiency problem with my running time for the forloop above , thanks to Arthur, however this gives me the wrong categories
		for i in range(self.num_classes):
			# for each column
			P.transpose()[i]=(self.class_scales[i]*np.exp(-(np.multiply(A-self.class_means[i],A-self.class_means[i])/(2*self.class_vars[i]))).transpose())
		

		# calculate the most likely class for each data point
		#cats = np.argmax(P,axis=1) # take the argmax of P along axis 1
		cats = np.reshape(np.argmax(P,axis=1),(A.shape[0],1))
		cats=np.asmatrix(cats)
		
		
		# use the class ID as a lookup to generate the original labels
		labels = self.class_labels[cats]

		if return_likelihoods:
			return cats, labels, P

		return cats, labels

	def __str__(self):
		'''Make a pretty string that prints out the classifier information.'''
		s = "\nNaive Bayes Classifier\n"
		for i in range(self.num_classes):
			s += 'Class %d --------------------\n' % (i)
			s += 'Mean	: ' + str(self.class_means[i,:]) + "\n"
			s += 'Var	: ' + str(self.class_vars[i,:]) + "\n"
			s += 'Scales: ' + str(self.class_scales[i,:]) + "\n"
			pass
		s += "\n"
		return s
		
	def write(self, filename):
		'''Writes the Bayes classifier to a file.'''
		# extension
		return

	def read(self, filename):
		'''Reads in the Bayes classifier from the file'''
		# extension
		return

	
class KNN(Classifier):

	def __init__(self, dataObj=None, headers=[], categories=None, K=None):
		'''Take in a Data object with N points, a set of F headers, and a
		matrix of categories, with one category label for each data point.'''
		
		# call the parent init with the type
		Classifier.__init__(self, 'KNN Classifier')
		
		# store the headers used for classification
		self.headers=headers
		# number of classes and number of features
		self.num_classes=K
		self.num_features=0
		# original class labels
		self.class_labels=[] # empty list
		# unique data for the KNN classifier: list of exemplars (matrices)
		self.exemplars=[]
		self.category_data=[]
		
		
		# if given data,
		if dataObj!=None:
			# call the build function
			self.build(dataObj.get_Num_Matrix(),categories,K)
			
			print " data object created"
		
	def build( self, A, categories, K = None ):
		'''Builds the classifier give the data points in A and the categories'''

		# figure out how many categories there are and get the mapping (np.unique)
		unique, mapping = np.unique( np.array(categories.transpose()), return_inverse=True)
		
		# store any necessary information: # of classes, # of features, original labels
		# create the matrices for the means, vars, and scales
		self.num_classes=len(unique) # number of unique classes/categories
		self.num_features=A.shape[1] # number of columns in data matrix
		self.class_labels=unique # unique categories
		num_rows=A.shape[0]
		
		
		# the output matrices will be categories (C) x features (F)
		matrix=np.zeros((self.num_classes,self.num_features))
		self.means=matrix
		self.vars=matrix
		self.scales=matrix # same dimensions
		
		
		# for each category i, build the set of exemplars
		for i,label in enumerate(unique):
			
			# if K is None
			if K==None:
				# append to exemplars a matrix with all of the rows of A where the category/mapping is i
				self.exemplars.append(A[(unique[mapping] == label), :])
			else:	# else
				# run K-means on the rows of A where the category/mapping is i
				codebook, errors =vq.kmeans(A[(unique[mapping] == label), :], K)
				
				#print "  codebook	",codebook.shape
				self.exemplars.append(codebook)	 # append the codebook to the exemplars
			self.means[i] = np.mean(self.exemplars[i], axis = 0)
		return

	
	def classify(self, A, K=3, return_distances=False):
		'''Classify each row of A into one category. Return a matrix of
		category IDs in the range [0..C-1], and an array of class
		labels using the original label values. If return_distances is
		True, it also returns the NxC distance matrix.

		The parameter K specifies how many neighbors to use in the
		distance computation. The default is three.'''
		num_rows=A.shape[0]
		print "	  A.shape[1]  ",A.shape[1]
		# error check to see if A has the same number of columns as the class means
		if A.shape[1]!=self.exemplars[0].shape[1]:
			print "Error alert, number of columns not the same"
			return # terminate
		

		# make a matrix that is N x C to store the distance to each class for each data point
		D = np.zeros((A.shape[0],self.num_classes)) # a matrix of zeros that is N (rows of A) x C (number of classes)
		
		
		
		# for each class i
		for i in range(self.num_classes):
			# make a temporary matrix that is N x M where M is the number of examplars (rows in exemplars[i])
			temp=np.zeros((A.shape[0],self.exemplars[i].shape[0]))
			# calculate the distance from each point in A to each point in exemplar matrix i (for loop)
			for p in range(num_rows):
				for x in range(self.exemplars[i].shape[0]):
					
					distance=scipy.spatial.distance.euclidean(A[p,:], self.exemplars[i][x,:])
					temp[p,x]=distance # add to temporary matrix
			
			# sort the distances by row
			temp=np.sort(temp,axis=1)
			# sum the first K columns
			# this is the distance to the first class
			sum=np.sum(temp[:,:K],axis=1)
			
			for j in range(num_rows):
				D[p,i]=sum[p]
		
		# calculate the most likely class for each data point
		cats = np.matrix(np.argmin(D,axis=1)).transpose() # take the argmin of D along axis 1

		# use the class ID as a lookup to generate the original labels
		labels = self.class_labels[cats]

		if return_distances:
			return cats, labels, D

		return cats, labels

	def __str__(self):
		'''Make a pretty string that prints out the classifier information.'''
		s = "\nKNN Classifier\n"
		for i in range(self.num_classes):
			
			s += 'Class %d --------------------\n' % (i)
			s += 'Number of Exemplars: %d\n' % (self.exemplars[i].shape[0])
			#print self.exemplars[i]
			s += 'Mean of Exemplars	 :' + str(np.mean(self.exemplars[i], axis=0)) + "\n"

		s += "\n"
		return s


	def write(self, filename):
		'''Writes the KNN classifier to a file.'''
		# extension
		return

	def read(self, filename):
		'''Reads in the KNN classifier from the file'''
		# extension
		return
	

