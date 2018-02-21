# Bruce Maxwell
# Spring 2015
# CS 251 Project 8
#
# Modified from KNN class test
#

import sys
import data
import classifiers
import csv


class classify_NB:
	'''Reads in a training set and a test set and builds two KNN
	classifiers.  One uses all of the data, one uses 10
	exemplars. Then it classifies the test data and prints out the
	results.
	
	first part , reading in two input files, code is inspired by Bruce's code
	'''
	# initialize the object
	def __init__(self, train, test, t1=None, ts1=None):
	
	
		
	
		# read the training and test sets
		dtrain = data.Data(train)
		dtest = data.Data(test)
	
		""" Bruce KNN test code source starts here, with additional comments for my understanding """
	
		# get the categories and the training data A and the test data B
		if t1!=None and	ts1!=None:
			traincatdata = data.Data(t1)
			testcatdata = data.Data(ts1)
			traincats = traincatdata.get_data( [traincatdata.get_headers()[-1]] )
			testcats = testcatdata.get_data( [testcatdata.get_headers()[-1]] )
			A = dtrain.get_data( dtrain.get_headers()[:-1] )
			B = dtest.get_data( dtest.get_headers()[:-1] )
		else:
			# assume the categories are the last column
			traincats = dtrain.get_data( [dtrain.get_headers()[-1]] )  # training categories 
			testcats = dtest.get_data( [dtest.get_headers()[-1]] )	# test categories
			A = dtrain.get_data( dtrain.get_headers()[:-1] )  # train data matrice
			B = dtest.get_data( dtest.get_headers()[:-1] )	# test data matrice

		
		
		
		

	
	
		

		# create two classifiers, one using 10 exemplars per class
		nb = classifiers.NaiveBayes()
		knnc10 = classifiers.NaiveBayes()

		# build the classifiers given data and categories
		nb.build( A, traincats )
	

		# use the classifiers on the test data, to try classify A
		classcats, alllabels =nb.classify(A)
	
	
		""" #Bruce KNN test edited for my project code source ends here """
	
		# Classify the training set and print out a confusion matrix.
		# build confusion matrix and print it out
		confusion_matrix=nb.confusion_matrix(traincats , classcats )  #
		# print out the confusion matrix
		cmtxA=nb.confusion_matrix_str(confusion_matrix)
		#print classcats 
		print "	 **	  train set	  confusion matrix	 **\n ",cmtxA
	
	
		# Classify the test set and print out a confusion matrix.
		
		print " **  in:",B.shape
		
		# use the classifiers on the test data, to try classify B
		classcats, alllabels = nb.classify( B )
	
		print " **  out:",classcats.shape
		
		# build confusion matrix and print it out
		if len(testcats)!=len(classcats):
			print "#* Error:  Something terribly wrong   needs to be fixed. THE  CONFUSION MATRIX BELOW IS WRONG"
			testcats=classcats
		
		
		confusion_matrix=nb.confusion_matrix(testcats , classcats )  #
		# print out the confusion matrix
		cmtx=nb.confusion_matrix_str(confusion_matrix)
		
		#print classcats 
		print " **	test set	 confusion matrix	**\n ",cmtx
		self.cmtx=cmtx
		# write out csv file for test data +  predicted categories
		#create a temporary csv file that holds the data
		
		with open('testmatrix_data.csv', 'wb') as f:
			writer = csv.writer(f)

			#write in my headers
			list=[]
			headers=dtest.get_headers()[:-1]
			headers.append("Cluster ID")
			list.append(headers)
			writer.writerows(list)
		
			types=[] # asume all numeric data
			for i in range(len(headers)):
				types.append("numeric")
			writer.writerows([types])	# write in the types
		
		
		
			values=[]
			C=B.tolist()
		
			for i in range(len(C)):
				C[i].append(classcats[i].item(0))
		
		
			for row in C:  # row in test data
			
				values.append(row)
		
			writer.writerows(values) # write in all the rows
			print "****		new file created for test data , named 'testmatrix_data.csv'"

		f.close()
		
	def get_confusion(self):
		return self.cmtx
		
def main(argv):
	print "starting"
	 # usage
	if len(argv) >4 :
		print 'Usage: python %s <training data file> <test data file> <optional training category file> <optional test category file>' % (argv[0])
		classifier=classify_NB(argv[1],argv[2],argv[3],argv[4])
		exit(-1)
	else:
		classifier=classify_NB(argv[1],argv[2])
		
	

	
if __name__ == "__main__":
	main(sys.argv)
