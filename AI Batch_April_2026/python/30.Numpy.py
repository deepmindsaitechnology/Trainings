# Python program to demonstrate  
# basic array characteristics 
import numpy as np 
  
#Basic Numpy Arrays

# Creating array object 
arr = np.array( [ 1, 2, 3])
arr.ndim,arr.shape,arr.size

# Printing type of arr object 
print("Array is of type: ", type(arr)) 
  
# Printing array dimensions (axes) 
print("No. of dimensions: ", arr.ndim) 
  
# Printing shape of array 
print("Shape of array: ", arr.shape) 
  
# Printing size (total number of elements) of array 
print("Size of array: ", arr.size) 
  
# Printing type of elements in array 
print("Array stores elements of type: ", arr.dtype) 



# creating flot type array 
arr2=np.array([1,2,3,4],dtype=np.float64)
arr2
                 
                 
# two dimensional arrays
arr = np.array( [[ 1, 2, 3], 
                 [ 4, 2, 5]] ) 
  
# Printing type of arr object 
print("Array is of type: ", type(arr)) 
  
# Printing array dimensions (axes) 
print("No. of dimensions: ", arr.ndim) 
  
# Printing shape of array 
print("Shape of array: ", arr.shape) 
  
# Printing size (total number of elements) of array 
print("Size of array: ", arr.size) 
  
# Printing type of elements in array 
print("Array stores elements of type: ", arr.dtype) 

# Slicing of Arrays :

arr[0]
arr[0][2]  # Row number and columns number.
arr[-1]
arr[-1][1]

# transformation - rows become columns and vicd versa

arr.transpose() 

# Another example

# Reshaping 3X4 array to 2X2X3 array 
arr = np.array([[1, 2, 3, 4], 
                [5, 2, 4, 2], 
                [1, 2, 0, 1]]) 
  
newarr = arr.reshape(2, 2, 3) 
  
print ("\nOriginal array:\n", arr) 
print ("Reshaped array:\n", newarr) 
  
# Flatten array 
arr = np.array([[1, 2, 3], [4, 5, 6]]) 
flarr = arr.flatten() 
  
print ("\nOriginal array:\n", arr) 
print ("Fattened array:\n", flarr) 

#Linear Algebra
A = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
B = np.array([
    [6, 5],
    [4, 3],
    [2, 1]
])

A.dot(B)

A @ B

# Transpose
B.T

B.T @ A

# arraays witth given range
np.linspace(0,10,5)
np.arange(0,10)
np.arange(0,10,3)

# arrays with random
np.random.standard_normal((2,4))  

# stacking vertical and horizantal
  
a=np.random.standard_normal((2,4))  
b=np.random.standard_normal((3,4))  
a
b
np.vstack((a,b))  # no of rows shd match for vertical
np.hstack((a,b)) # no of cols shd match for horizantal

c=np.random.standard_normal((3,5))  
np.hstack((b,c))

# to save array to a name and reload into program
a=np.random.standard_normal((2,4))  
np.save('test.npy',a)
a
# reload
al=np.load('test.npy')
al

# Handling date

x=np.datetime64('2016-12')
x
y=np.datetime64('2017-11')
x-y

x<y

r=np.arange(np.datetime64('2018-03-01'),np.datetime64('2018-04-01'))
r

#Useful Numpy functions

# random functions
np.random.random(size=2)
np.random.normal(size=2)
np.random.rand(2, 4)

# arange functions
np.arange(10)
np.arange(5, 10)
np.arange(0, 1, .1)

# reshape functions
np.arange(10).reshape(2, 5)
np.arange(10).reshape(5, 2)

# linspace functions
np.linspace(0, 1, 5)
np.linspace(0, 1, 20)
np.linspace(0, 1, 20, False)

# zeros, ones, empty functions
np.zeros(5)
np.zeros((3, 3))
np.zeros((3, 3), dtype=np.int32)
np.ones(5)
np.ones((3, 3))
np.empty(5)
np.empty((2, 2))

#identity and eye functions
#numpy.eye(R, C = None, k = 0, dtype = type <‘float’>) : Return a matrix having 1’s on the diagonal and 0’s elsewhere w.r.t. k.
np.identity(3)  # Return a identity matrix i.e. a square matrix with ones on the main daignol.
#numpy.eye(R, C = None, k = 0, dtype = type <‘float’>) : Return a matrix having 1’s on the diagonal and 0’s elsewhere w.r.t. k.
np.eye(3) # np.eye(3,3) is same
np.eye(8, 4)
np.eye(8, 4, k=1) # one row above the central diagonal
np.eye(8, 4, k=-3) # 3 below the main diagonal

"Hello World"[6]  # same as st[6]