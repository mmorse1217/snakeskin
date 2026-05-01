import numpy as np
import scipy.interpolate as si
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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
    spl = si.BSpline(knots, control_points, degree)
    return spl

def eval_bspline(spline, num_control_points, degree, n=100):
    max_param = num_control_points - (degree)
    return spline(np.linspace(0,max_param,n))

def deform(position_constraints, parameter_values, knots, degree):
    def form_system_matrix(num_basis_elements, num_constraints):
        bspline_system_matrix = np.zeros((num_constraints,num_basis_elements))

        for j in range(num_basis_elements):
            knot_span_of_ith_bspline = knots[j:j+degree+2]
            print(j,'th knots',knot_span_of_ith_bspline)
            ith_bspline = si.BSpline.basis_element(knot_span_of_ith_bspline,
                    extrapolate=False)
            #x = np.linspace(0.,9.,100)
            #plt.plot(x,ith_bspline(x),'-',color=colors[j%7])
            #plt.plot(parameter_values,ith_bspline(parameter_values),'o',color=colors[j
            #    % 7])

            for i in range(num_constraints):
                ith_bspline_value = ith_bspline(parameter_values[i])
                ith_bspline_value = 0. if np.isnan(ith_bspline_value) else ith_bspline_value
                bspline_system_matrix[i,j] = ith_bspline_value
        #plt.show()
        return bspline_system_matrix
    
    num_knots = knots.shape[0]
    num_basis_elements = num_knots - degree - 1
    num_constraints = position_constraints.shape[0]
    
    bspline_system_matrix = form_system_matrix(num_basis_elements,num_constraints)
    pseudo_inv = np.linalg.pinv(bspline_system_matrix)

    return pseudo_inv @ position_constraints

colors = ('b', 'g', 'r', 'c', 'm', 'y', 'k')
degree = 6
num_control_points = 12
dim = 10
control_point_dims = [ (2*(np.arange(num_control_points) % 2)-1).reshape(num_control_points,1)]
control_point_dims += [ np.arange(num_control_points).reshape(num_control_points,1)]*(dim-1)
cv = np.hstack(control_point_dims)
spline = scipy_bspline(cv,n=100, degree=degree)

# mark locations of positions to update
max_param = num_control_points - degree
num_constraints =10
constraint_locations = np.linspace(3*max_param/4., max_param-2e-15, num_constraints)
position_constraints = np.ones((num_constraints,dim))*2.
deformed_control_points = deform(position_constraints, constraint_locations, spline.t, degree)
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


quit()
plt.plot(constraint_x, constraint_y, 'go-', label='Deformed Constraints')
plt.plot(sx, sy, 'ko-', label='Original spline values')

# Plot original spline
x = np.linspace(0,max_param,500)
plt.plot(cv[:,0],cv[:,1], 'ro-', label='Initial Control Points')
sx,sy = spline(x).T
plt.plot(sx,sy, 'r--', label='Initial Spline')

# Plot new spline
plt.plot(updated_control_points[:,0],updated_control_points[:,1], 
        'bo-', label='Deformed Control Points')
sx,sy = deformed_spline(x).T
plt.plot(sx,sy, 'b--', label='Deformed Spline')

plt.legend()
plt.show()
