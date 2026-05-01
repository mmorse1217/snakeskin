import numpy as np
import scipy.interpolate as si
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import product

def scipy_bspline(control_points, n=100, degree=3):
    """ Calculate n samples on a bspline

        cv :      Array ov control vertices
        n  :      Number of samples to return
        degree:   Curve degree
    """
    control_points = np.asarray(control_points)
    num_control_points = control_points.shape[0]


    # Opened curve
    degree = np.clip(degree,1,num_control_points-1)
    knots = np.clip(np.arange(num_control_points+degree+1)-degree,0,num_control_points-degree)
    spl = si.BivariateSpline._from_tck([knots, knots, control_points, degree,
        degree])
    return spl

def eval_bspline(knots, cv, degree, x,y):
    dim = cv.shape[1]
    n = x.shape[0]
    assert x.shape[0] == y.shape[0]
    positions = np.zeros((n,dim))
    for i in range(dim):
        positions[:, i] = si.dfitpack.bispeu(knots,knots, cv[:,i], degree, degree, x,y)[0]
    return positions

def deform(position_constraints, parameter_values, knots, degree):
    def form_system_matrix(num_basis_elements, num_constraints, dim):
        basis_elements = { j :
            si.BSpline.basis_element(knots[j:j+degree+2], extrapolate=False)
            for j in range(num_basis_elements) 
            }
        bspline_system_matrix = np.zeros((num_constraints,num_basis_elements**2))

        for j,k in product(range(num_basis_elements),range(num_basis_elements)):
            jth_bspline =  basis_elements[j]
            kth_bspline =  basis_elements[k]
            index = j*num_basis_elements + k
            #x = np.linspace(0.,9.,100)
            #plt.plot(x,ith_bspline(x),'-',color=colors[j%7])
            #plt.plot(parameter_values,ith_bspline(parameter_values),'o',color=colors[j
            #    % 7])

            for i in range(num_constraints):
                jth_bspline_value = jth_bspline(parameter_values[i][0])
                kth_bspline_value = kth_bspline(parameter_values[i][1])
                bspline_value = jth_bspline_value*kth_bspline_value
                bspline_value = 0. if np.isnan(bspline_value) else bspline_value
                bspline_system_matrix[i,index] = bspline_value
        #plt.show()
        return bspline_system_matrix

    num_knots = knots.shape[0]
    num_basis_elements = num_knots - degree - 1
    dim = position_constraints.shape[1] 
    num_constraints = position_constraints.shape[0]
    
    bspline_system_matrix = form_system_matrix(num_basis_elements,num_constraints, dim)
    pseudo_inv = np.linalg.pinv(bspline_system_matrix)

    return pseudo_inv @ position_constraints

colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
degree = 5
num_control_points = 20
dim = 3
knots = np.clip(np.arange(num_control_points+degree+1)-degree,0,num_control_points-degree)
max_param = num_control_points - degree
cv = np.zeros((num_control_points**2, dim))
temp =np.linspace(0,1,num_control_points)
for i in range(num_control_points):
    for j in range(num_control_points):
        index = i*num_control_points+ j
        #for d in range(dim):
        cv[index,0] = temp[i]
        cv[index,1] = temp[j]
#control_point_dims = [ (2*(np.arange(num_control_points) % 2)-1).reshape(num_control_points,1)]
#control_point_dims += [ np.arange(num_control_points).reshape(num_control_points,1)]*(dim-1)
#cv = np.hstack(control_point_dims)
spline = scipy_bspline(cv,n=100, degree=degree)

fig  = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot original spline
n = 5000
x = np.random.rand(n)*max_param
y = np.random.rand(n)*max_param
ax.scatter(cv[:,0],cv[:,1], cv[:,2], c='r', label='Initial Control Points')
#sx,sy = spline.ev(x[0], x[0]).T
positions = eval_bspline(knots, cv, degree, x, y)
ax.plot_trisurf(positions[:,0], positions[:,1], positions[:,2], color='b',
        edgecolor='none',linewidth=0,#antialiased=False,
        label='Initial Spline')

# Set up constraints
num_constraints =10
position_constraints = np.zeros((num_constraints,dim))
constraint_locations = np.zeros((num_constraints,2))
temp = np.linspace(0,max_param,num_constraints)
for i in range(num_constraints):
    #constraint_locations[i,:] = temp[i] , temp[i]
    constraint_locations[i,:] = np.random.rand(1,2)*max_param
    #position_constraints[i,:2] = constraint_locations[i,:]
    position_constraints[i,2] = 1.
deformed_control_points = deform(position_constraints, constraint_locations,
        knots, degree)
deformed_control_points += cv
# Plot deformed spline
print('Original control points', cv)
print('deformed control points', deformed_control_points)
print('Constraints:', position_constraints)
print('values at constraints:', eval_bspline(knots, deformed_control_points,
    degree, constraint_locations[:,0], constraint_locations[:,1]))
ax.scatter(deformed_control_points[:,0],
        deformed_control_points[:,1],
        deformed_control_points[:,2], c='g', label='Deformed Control Points')
positions = eval_bspline(knots, deformed_control_points, degree, x, y)
ax.plot_trisurf(positions[:,0], positions[:,1], positions[:,2], color='c',
        edgecolor='none',linewidth=0,#antialiased=False,
        label='Deformed Spline')


# Plot constraints
evaled_constraints= eval_bspline(knots, cv, degree, constraint_locations[:,0], constraint_locations[:,1])
ax.scatter(evaled_constraints[:,0],
        evaled_constraints[:,1],
        evaled_constraints[:,2],c='y', s=200,marker='*', label='Original Constraint locations')
evaled_constraints= eval_bspline(knots, deformed_control_points, degree, constraint_locations[:,0], constraint_locations[:,1])
ax.scatter(evaled_constraints[:,0],
        evaled_constraints[:,1],
        evaled_constraints[:,2],c='k',  s=200,marker='*',label='Deformed Constraint locations')
plt.show()
quit()
# mark locations of positions to update
max_param = num_control_points - degree
constraint_locations = np.linspace(3*max_param/4., max_param-2e-15, num_constraints)
position_constraints = np.ones((num_constraints,dim))*2.
#print('delta P:', deformed_control_points)
# Plot constraints
updated_control_points = cv + deformed_control_points 
deformed_spline = scipy_bspline(updated_control_points,n=100, degree=degree)

#sx,sy = spline(constraint_locations).T
x = np.linspace(0,max_param,300)
spline_values = spline(x)
fig  = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# plot control points
ax.scatter(cv[:,0],
        cv[:,1],
        cv[:,2],c='r', label='Original control points')

# plot original spline
ax.plot(spline_values[:,0],
        spline_values[:,1],
        spline_values[:,2],c='b', label='Original Spline')

#plot original spline constraint values
constraint_values =  spline(constraint_locations)
ax.scatter(constraint_values[:,0],
        constraint_values[:,1],
        constraint_values[:,2],c='g', label='Original Constraint locations')

#plot deformed spline constraint values
constraint_values =  spline(constraint_locations)+ position_constraints
print(constraint_values)
ax.scatter(constraint_values[:,0],
        constraint_values[:,1],
        constraint_values[:,2],c='k', label='Deformed Constraints')

#plot deformed_spline values
deformed_spline_values = deformed_spline(x)
ax.plot(deformed_spline_values[:,0],
        deformed_spline_values[:,1],
        deformed_spline_values[:,2],c='c', label='Deformed Spline')

plt.show()
