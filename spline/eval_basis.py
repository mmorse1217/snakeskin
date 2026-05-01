import numpy as np
import pylab as pl

def deboor(x, i, degree, knots, control_points):
    if degree == 0:
        return np.where(np.all([knots[i] <=  x,
                                x < knots[i+1]],axis=0), control_points[i], 0.0)
        '''
        if knots[i] <= x and x < knots[i+1]:
            return np.ones_like(x)
        else:
            return np.zeros_like(x)
        '''
        
    first_numerator = x-knots[i]
    first_denominator = knots[i+degree]-knots[i]
    
    second_numerator = knots[i+degree+1]-x
    second_denominator = knots[i+degree+1]-knots[i+1]
    
    first_term = first_numerator/first_denominator
    second_term = second_numerator/second_denominator

    if np.abs(first_denominator) < 1e-16:
        first_term = 0.
    if np.abs(second_denominator) < 1e-16:
        second_term = 0.
    first_deboor_eval = deboor(x,i,degree-1, knots, control_points)
    second_deboor_eval = deboor(x,i+1,degree-1, knots, control_points)
    return first_term*first_deboor_eval + second_term*second_deboor_eval

degree = 6
num_control_points = 12
#num_knots = num_control_points -2*(degree + 1)
#num_knots =  

x = np.linspace(0,1,400)
control_points = np.ones((num_control_points,))
knots = np.hstack([np.zeros((degree+1,)),
    np.linspace(0,1,num_control_points - degree -1), 
    np.ones((degree+1,))])
print(knots)
print(knots.shape)
print(num_control_points)
#print(deboor(x,3,degree, knots, control_points))
for i in range(4):
    bspline_values = deboor(x,i,degree, knots, control_points)
    pl.plot(x,bspline_values,'-')
pl.show()
