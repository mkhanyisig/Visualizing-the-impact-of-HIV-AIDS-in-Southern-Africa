# Bruce Maxwell
# Spring 2015
# CS 251 Project 8
#
# Modified from KNN class test
#

import sys
import data
import classifiers
import numpy  as np
def main(argv):
	'''Reads in a training set and a test set and builds two KNN
	classifiers.  One uses all of the data, one uses 10
	exemplars. Then it classifies the test data and prints out the
	results.
	
	first part , reading in two input files, code is inspired by Bruce's code
	'''

	# usage
	if len(argv) < 3:
		print 'Usage: python %s <training data file> <test data file> <optional training category file> <optional test category file>' % (argv[0])
		exit(-1)
	
	
	""" Bruce KNN test code source starts here, with comments for my understanding """
	
	
	# read the training and test sets
	dtrain = data.Data(argv[1])
	dtest = data.Data(argv[2])

	# get the categories and the training data A and the test data B
	if len(argv) > 4:
		traincatdata = data.Data(argv[3])
		testcatdata = data.Data(argv[4])
		traincats = traincatdata.get_data( [traincatdata.get_headers()[0]] )
		testcats = testcatdata.get_data( [testcatdata.get_headers()[0]] )
		A = dtrain.get_data( dtrain.get_headers() )
		B = dtest.get_data( dtest.get_headers() )
	else:
		# assume the categories are the last column
		traincats = dtrain.get_data( [dtrain.get_headers()[-1]] )  # training categories 
		testcats = dtest.get_data( [dtest.get_headers()[-1]] )	# test categories
		A = dtrain.get_data( dtrain.get_headers()[:-1] )  # train data matrice
		B = dtest.get_data( dtest.get_headers()[:-1] )	# test data matrice
	
	
	# for float categories, turn them into ints
	new=[]
	if type(traincats[0])==float:
		
		for t in traincats:
			new.append(int(t))
	traincats=new
	new=[]
	if type(testcats[0])==float:
		new=[]
		for t in testcats:
			new.append(int(t))
	testcats=new	
	
	# create two classifiers, one using 10 exemplars per class
	knncall = classifiers.KNN()
	knnc10 = classifiers.KNN()
	
	
	#print type(type(traincats))
	# build the classifiers given data and categories
	knncall.build( A, traincats )
	knnc10.build(A, traincats, 10) # specify K 

	# use the classifiers on the test data, to try classify A
	classcats, alllabels = knncall.classify( A )
	tencats, tenlabels = knnc10.classify( A )
	
	""" #Bruce KNN test edited for my project code source ends here """
	
	# Classify the training set and print out a confusion matrix.
	# build confusion matrix and print it out
	confusion_matrix=knncall.confusion_matrix(traincats , classcats )  #
	# print out the confusion matrix
	cmtx=knncall.confusion_matrix_str(confusion_matrix)
	#print classcats 
	print "   train set   confusion matrix \n ",cmtx
	
	
	# Classify the test set and print out a confusion matrix.
	
	# use the classifiers on the test data, to try classify B
	classcats, alllabels = knncall.classify( B )
	tencats, tenlabels = knnc10.classify( B )
	
	# build confusion matrix and print it out
	confusion_matrix=knncall.confusion_matrix(testcats , classcats )  #
	# print out the confusion matrix
	cmtx=knncall.confusion_matrix_str(confusion_matrix)
	#print classcats 
	print "   test set   confusion matrix \n ",cmtx
	
	
	return
	
if __name__ == "__main__":
	main(sys.argv)
