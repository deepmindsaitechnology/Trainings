from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
#import numpy as np

# setting the plot with 3D projection
fig=plt.figure()
chart=fig.add_subplot(1,1,1,projection='3d')

# set labels
chart.set_title('Sample 3D plots')
chart.set_xlabel('x axis')
chart.set_ylabel('y axis')
chart.set_zlabel('z axis')

# Set the co ordinates
x=[1,2,3,4,5,6,7,8]
y=[2,3,2,7,9,11,13,15]
z=[3,4,12,8,10,12,14,16]

# 3D Line Plot
#chart.plot(x,y,z)
#chart.plot_wireframe(X,Y,Z) # not working

#3D scatter plots
chart.scatter(x,y,z,marker='o',c='red')


# Multiple scattered plot on one graph
#fig=plt.figure()
#chart=fig.add_subplot(1,1,1,projection='3d')

x2=[-1,-2,-3,-4,-5,-6,-7,-8]
y2=[-2,3,-2,-7,9,-11,-13,15]
z2=[3,-4,-12,8,-10,-12,-14,16]

chart.scatter(x2,y2,z2,marker='^',c='blue')

plt.show()

# another 3D example
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

fig=plt.figure()
chart=fig.add_subplot(1,1,1,projection='3d')

z=np.linspace(0,30,100)
x=np.sin(z)
y=np.cos(z)

chart.plot(x,y,z)


# 3D graphs-2
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

fig=plt.figure()
chart=fig.add_subplot(1,1,1,projection='3d')

#Co-ordinates data from get_test_data function.
x,y,z=axes3d.get_test_data(0.05)
#x,y,z=axes3d.get_test_data(1.05)

chart.plot_wireframe(x,y,z,rstride=10,cstride=1)
#chart.plot_wireframe(x,y,z,rstride=1,cstride=1)
chart.set_xlabel('X label')
chart.set_ylabel('Y label')
chart.set_zlabel('Z label')

plt.show()

# #D bar plots example

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

fig=plt.figure()
chart=fig.add_subplot(1,1,1,projection='3d')
x=[1,2,3,4,5,6,7,8,9,10]
y=[4,6,9,12,3,5,4,5,6,8]
z=[0,0,0,0,0,0,0,0,0,0]
#z=[0,0,3,0,0,0,0,0,0,0]
#z=[3,8,2,9,6,9]
#dx=np.ones(10)
dx=[0,0,0,0,0,0,0,0,0,0]
dy=np.ones(10)
dz=[1,2,3,4,5,6,7,8,9,10]

chart.bar3d(x,y,z,dx,dy,dz,color='cyan')
chart.set_xlabel('X label')
chart.set_ylabel('Y label')
chart.set_zlabel('Z label')
plt.show()


