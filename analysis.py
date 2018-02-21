#Mkhanyisi Gamedze
# CS 251 - Spring 2017
# project 2

# global fields

import sys
import numpy as np
import csv
import data
import scipy.stats
import scipy.cluster.vq as vq
import random


# functions
def range_(headers, data):
	""" Takes in a list of column headers and the Data object and returns a list of 2-element 
		lists with the minimum and maximum values for each column. 
		The function is required to work only on numeric data types."""
	column_matrix=data.get_data(headers).getT() # get columns as rows, as this makes analysis much easier by just perfoming operations on column list directly
	if column_matrix==[]:
		print "wrong headers, not present in data Object"
		return []
	column_max=column_matrix.max(1)
	column_min=column_matrix.min(1)
	final=np.concatenate((column_min, column_max), axis=1)
	
	rng=final.tolist()
	return rng
	
def mean(headers, data):
	""" Takes in a list of column headers and the Data object and returns a list of the
	 mean values for each column. Use the built-in numpy functions to execute this calculation."""
	column_matrix=data.get_data(headers)
	mean_values=column_matrix.mean(0)
	
	return mean_values


def stdev(headers, data):
	"""stdev - Takes in a list of column headers and the Data object and returns a list of the 
	standard deviation for each specified column. Use the built-in numpy functions to execute 
	this calculation."""
	column_matrix=data.get_data(headers)
	mean_values=column_matrix.std(0)
	std_values=mean_values.tolist()
	return std_values

	 
def normalize_columns_separately(headers, data):
	"""Takes in a list of column headers and the Data object and returns a matrix with each 
	column normalized so its minimum value is mapped to zero and its maximum value is mapped to 1."""
	column_matrix=data.get_data(headers)
	column_max=column_matrix.max(1)
	column_min=column_matrix.min(1)
	range=column_max-column_min
	nomalized=(column_matrix-column_min)/range
	return nomalized
	
def normalize_columns_together(headers, data):
	""" Takes in a list of column headers and the Data object and returns a matrix with each entry normalized 
	so that the minimum value (of all the data in this set of columns) is mapped to zero and its maximum value 
	is mapped to 1."""
	column_matrix=data.get_data(headers)
	max=column_matrix.max()
	print "The maximum:	 ", max
	min=column_matrix.min()
	print "The minimum:	 ", min
	range=max-min
	print "range: ", range
	column_matrix=column_matrix-min
	normalized=column_matrix/range
	return normalized
	
def sort(headers, data): # extension
	""" Return the numeric matrices with sorted columns	 """
	column_matrix=data.get_data(headers) # get raw matrix data for numeric values
	print "\n before sorting \n "
	print column_matrix
	
	column_matrix=column_matrix.tolist()
	column_array=np.asarray(column_matrix)
	
	column_array.sort(axis=0)
	
	print "\n \n done sorting here is your matrix \n"
	
	return column_array
	
def normalize_sort(headers, data): # extension
	column_matrix=data.get_data(headers)
	max=column_matrix.max()
	
	min=column_matrix.min()
	
	range=max-min
	column_matrix=column_matrix-min
	normalized=column_matrix/range
	print "\n before sorting \n ", normalized, "\n \n "
	
	normalized.sort(axis=0)
	print "\n after sorting \n "
	return normalized


	
def linear_regression(d, ind, dep):
	""" takes in data object and then creates a linear regression using the dependant variable"""

	y=d.get_data([dep])
	print "y  :",y
	A=d.get_data(ind)
	print "A  :",A
	ones = np.asmatrix(np.ones( (A.shape[0]) )).transpose()
	A=np.concatenate((A, ones), axis=1)
	print "concatenated A  :",A
	AAinv=np.linalg.inv( np.dot(A.transpose(), A))
	print "AAinv:  \n",AAinv
	"""
	print "A  :",A
	print "y:  ",y
	print "AAinv:  ",AAinv"""
	print "shape A:	 ",A.shape
	print "shape y	:", y.shape
	x=np.linalg.lstsq(A,y)
	print "x   :\n",x
	b=x[0]
	print "\n b : \n",b
	N=len(y)
	print "N :	\n",N
	C=len(b)
	print "C  :	 ",C
	df_e=N-C
	df_r=C-1
	error=y - np.dot(A, b)
	print "error:	",error
	sse=np.dot(error.transpose(), error) / df_e
	print "sse	:",sse
	stderr=np.sqrt( np.diagonal( sse[0, 0] * AAinv ) )
	print "stderr: ",stderr
	t = b.transpose() / stderr
	print "t :", t
	p=2*(1 - scipy.stats.t.cdf(abs(t), df_e))
	print "p:	",p
	r2=1 - error.var() / y.var()
	print "R^2	 :",r2, "\n \n \n \n*************************************"
	
	
	return [b,sse,r2,t,p]

# This version uses SVD
def pca(d, headers, normalize=True):
	
	if normalize==True:
		A=normalize_columns_separately(headers, d)
	else:
		A=d.get_data(headers)
	m=mean(headers, d)
	D=A-m
	
	#calculate eigenvectors and eigenvalues
	U,S,V=np.linalg.svd(D,full_matrices=False)
	index=0
	#get the eigenvalues using the number of degress of freedom
	for d in S:
		e=(d*d)/(U.shape[0]-1)
		S[index]=e
		index=index+1
	#the projected data
	pdata=np.dot(V,(D.T))	 
	pdata=pdata.T
	
	pcad=data.PCAData(headers,pdata,S,V,m)

	return pcad
		
def kmeans_numpy( d, headers, K, whiten = True):
	'''Takes in a Data object, a set of headers, and the number of clusters to create
	Computes and returns the codebook, codes, and representation error.
	'''
	A=d.get_data(headers)
	W=vq.whiten(A)
	codebook, bookerror=vq.kmeans(W,K)
	codes, error=vq.vq(W, codebook)
	
	return codebook, codes, error
	
def kmeans_init(d, K, catergories=[]) :
	#return numpy matrix with K rows of the data
	print "type K :",type(K)
	
	r=np.matrix(np.zeros(K))
	c=np.matrix(np.zeros(d.shape[1]))
	r=r.transpose()
	retval=np.dot(r,c)
	retval=retval
	print "shape retval :",retval.shape 
	
	#  If no categories are given, a simple way to select the means is to randomly choose K data points 
	if len(catergories)==0:
		values=[] # values to be selected list
		h=d.shape[0]
		
		if K>h:
			print "The value of K is too high"
			return None
		#pick random rows
		
		while K>=0:
			val=random.randint(0,h-1)	#pick random value 
			while val in values:  #avoid duplicates, reselect if duplicate found
				val=random.randint(0,h-1)

			values.append(val) #add random index to values
			#retval[K,:]=d[val,:]
			K-=1
	# given an Nx1 matrix of categories/labels, then compute the mean values of each category 
	# and return those as the initial set of means		
	else:
		print "here"
		unique,labels=np.unique(catergories.tolist(),return_inverse=True)
		means=np.zeros((K,d.shape[1]))
		for i in range(len(unique)):	#for all unique values
			means [i,:]=np.mean(d[labels==i,:],axis=0)		#calculate means using categories
		retval=means   
	return retval
	
	
def kmeans_classify(d, means):
	ID=[] # list of ID values
	mindistances=[] # minimum distances algorithm 
	
	for dpoint in d:
		distances=[] # distances from each mean
		for mean in means: # compute distance of each mean, using the distance formula
			differences=dpoint-mean
			squares=np.square(differences)
			sums=np.sum(squares)
			distance=np.sqrt(sums)
			distances.append(distance) # add the distance to the distances list
		ID.append(np.argmin(distances))
		mindistances.append(distances[np.argmin(distances)])
		retval=[]
		retval.append(ID)
		retval.append(mindistances)
		
	return np.matrix(ID).transpose(), np.matrix(mindistances).transpose() # return a list of the ID values and the distances
""" 
def kmeans_algorithm(A, means):
	# set up some useful constants
	MIN_CHANGE = 1e-7
	MAX_ITERATIONS = 100
	D = means.shape[1]
	K = means.shape[0]
	N = A.shape[0]

	# iterate no more than MAX_ITERATIONS
	for i in range(MAX_ITERATIONS):
		# calculate the codes
		codes, errors = kmeans_classify( A, means )

		# calculate the new means
		newmeans = np.matrix(np.zeros_like( means ))
		counts = np.zeros( (K, 1) )
		for j in range(N):
			print "j :",j
			print "A[j,:]	:",A[j,:]
			print "codes ", codes
			print "codes[j,0]	:",codes[j,0]
			newmeans[codes[j,0],:] += A[j,:]
			counts[codes[j,0],0] += 1.0
		print "newmeans type:  ",type(newmeans)
		# finish calculating the means, taking into account possible zero counts
		for j in range(K):
			if counts[j,0] > 0.0:
				newmeans[j,:] /= counts[j, 0]
			else:
				newmeans[j,:] = A[random.randint(0,A.shape[0]-1),:] #randint is inclusive

		# test if the change is small enough
		diff = np.sum(np.square(means - newmeans))
		means = newmeans
		if diff < MIN_CHANGE:
			break

	# call classify with the final means
	codes, errors = kmeans_classify( A, means )
	print "result: ",means, codes, errors
	# return the means, codes, and errors
	return (means, codes, errors)
	"""

def kmeans_algorithm(A, means):
	# set up some useful constants
	MIN_CHANGE = 1e-7
	MAX_ITERATIONS = 100
	D = means.shape[1]
	K = means.shape[0]
	N = A.shape[0]

	# iterate no more than MAX_ITERATIONS
	for i in range(MAX_ITERATIONS):
		# calculate the codes
		codes, errors = kmeans_classify( A, means )

		# calculate the new means
		newmeans = np.matrix(np.zeros_like( means ))
		counts = np.zeros( (K, 1) )
		for j in range(N):
			newmeans[codes[j,0],:] += A[j,:]
			counts[codes[j,0],0] += 1.0

		# finish calculating the means, taking into account possible zero counts
		for j in range(K):
			if counts[j,0] > 0.0:
				newmeans[j,:] /= counts[j, 0]
			else:
				newmeans[j,:] = A[random.randint(0,A.shape[0]-1),:] #randint is inclusive

		# test if the change is small enough
		diff = np.sum(np.square(means - newmeans))
		means = newmeans
		if diff < MIN_CHANGE:
			break

	# call classify with the final means
	codes, errors = kmeans_classify( A, means )

	# return the means, codes, and errors
	return (means, codes, errors)

def kmeans(d, headers, K , categories = [] , whiten=True):
	'''Takes in a Data object, a set of headers, and the number of clusters to create
	Computes and returns the codebook, codes and representation errors. 
	If given an Nx1 matrix of categories, it uses the category labels 
	to calculate the initial cluster means.
	'''
	
	
	A=d.get_data(headers)
	#print "type A :",type(A)
	if whiten==True:
		W=vq.whiten(A)
		W=np.asmatrix(W)
	else:
		W=A
	#print "type W :",type(W)
	#print "K2  :",K
	
	
	codebook=kmeans_init(W,K, categories)
	#codebook=np.flipud(codebook)
	codebook, codes, errors = kmeans_algorithm(W, codebook)
	codes=codes
	
	
	return codebook, codes, errors	
	

def main(filename):
	d = data.Data( filename )
	headers = d.get_headers()
	
	
	
	
	
	print " \n \n ...........	   Testing your numeric data		.............."
	"""
	print " \n \n \n Your headers:"
	print d.get_headers()
	
	print "\n The types for your columns: you have ",d.get_num_columns(), "	 of them" 
	print d.get_type()
	
	
	print " \n The raw matrix of data"
	print d.printMatrix()
	
	
	headers.pop()
	
	print "\n \n get data for these columns:	  ",headers
	print d.get_data(headers)
	
	print "\n \n Range__ :"
	print "Your range values by column: ",range(headers, d)
	
	print "\n \n The column means are:	"
	print "Computed column mean: ", mean(headers, d)
	
	print " \n \n standard deviations:"
	print "Deviations:	", stdev(headers,d)
	
	print "\n \n Normalized columns"
	print normalize_columns_separately(headers, d)
	
	print "\n \n \n \nNormalizing the whole matrix"
	print normalize_columns_together(headers, d)
	
	print "############## Extensions ################"
	
	d.add_column("new data", "numeric")
	print "\n \n \n"
	d.add_datacolumn("new data", "numeric", [1, 2,3])
	
	print " \n \n ********* Extension 2- sorting		 ************** \n "
	
	print "Sorting a  matrix \n \n "
	print sort(headers, d)
	
	print "*** \n 2b)  normalize and sort \n"
	print " \n \n  \n ",normalize_sort(headers, d)
	"""
	print "*********************************************"
	print "linear regression"
	headers = d.get_headers()
	print "headers:	  ", headers
	print linear_regression(d, [headers[0],headers[1]], headers[2])
	
	
	
	





if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Usage: python %s <csv_filename>" % sys.argv[0]
		print "		  where <csv_filename> specifies a csv file"
		exit()
	main( sys.argv[1] )
	
	

	
	

	 
	 

	

	
	
	
	