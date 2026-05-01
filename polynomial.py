import numpy as np
from scipy.special import comb
import pylab as pl

def barycentric_weights_equispaced(nodes):
    n = nodes.shape[0]
    ones = np.ones((n,))
    weights = (-1.)**np.arange(n)*ones
    weights *= comb((n-1)*ones, np.arange(n))
    return weights
def barycentric_weights_chebyshev_second_kind(nodes):
    n = nodes.shape[0]
    weights = (-1.)**np.arange(n)
    weights[0] *= .5
    weights[-1] *= .5
    return weights

def barycentric_weights(nodes):
    num_interp_points = nodes.shape[0]

    distance = nodes.reshape(num_interp_points,1) - nodes.reshape(1,num_interp_points)
    distance += np.eye(num_interp_points)
    product_of_node_distances = np.prod(distance, axis=1)
    return 1./product_of_node_distances


def barycentric_first_kind(x, nodes, values, weights=None):
    if weights is None:
        weights = barycentric_weights(nodes)
    num_eval_points = x.shape[0]
    num_interp_points = nodes.shape[0]

    '''
    distance = x.reshape(num_eval_points,1) - nodes.reshape(1,num_interp_points)
    weights_div_distance = weights/distance
    
    numerator = np.dot(weights_div_distance, values)
    node_polynomial = np.prod(distance, axis=1)

    return node_polynomial*numerator
    '''
    ret = np.zeros_like(x)
    for eval_i in range(num_eval_points):
        xi = x[eval_i]
        node_poly = np.prod([xi - nodes[j] for j in range(num_interp_points)])
        for node_j in range(num_interp_points):
            ret[eval_i] += weights[node_j]/(xi - nodes[node_j])*values[node_j]
        ret[eval_i]*= node_poly
    return ret
            
def barycentric_second_kind(x, nodes, values, weights=None):
    if weights is None:
        weights = barycentric_weights(nodes)
    
    num_eval_points = x.shape[0]
    num_interp_points = nodes.shape[0]

    distance = x.reshape(num_eval_points,1) - nodes.reshape(1,num_interp_points)
    weights_div_distance = weights/distance
    
    numerator = np.dot(weights_div_distance, values)
    denominator = np.sum(weights_div_distance, axis=1)

    return numerator/denominator

def lagrange_naive(x, nodes, values):
    num_eval_points = x.shape[0]
    num_interp_points = nodes.shape[0]
    def evaluate_jth_basis_function(x,nodes, j):
        basis_func_value = np.ones_like(x);
        xj = nodes[j]
        for i in range(num_interp_points):
            xi = nodes[i]
            if i != j:
                basis_func_value *= (x - xi)/(xj - xi)
        return basis_func_value
    return sum(values[j]*evaluate_jth_basis_function(x,nodes, j) for j in range(n))

n = 30
#nodes = np.cos(np.pi*np.arange(n)/(n-1))
nodes = np.linspace(-1,1,n)
print(nodes)
#weights = barycentric_weights_chebyshev_second_kind(nodes)
#weights = barycentric_weights_equispaced(nodes)
#print(weights)
weights = barycentric_weights(nodes)
#print(weights)
#quit()
#y = 2*np.random.rand(n) -1
#f = lambda x:np.exp(5*x)*np.sin(20*x)
f = lambda x : 1./(1.+ 25*x*x)
#f = lambda x: (x <= 0.) + .1
y = f(nodes)

pl.plot(nodes,y, 'bo')
x = np.linspace(-1,1,20*n)
print('naive',lagrange_naive(x,nodes, y))
bary2 = barycentric_second_kind(x,nodes, y, weights)
bary1 = barycentric_first_kind(x,nodes, y)
#naive =lagrange_naive(x,nodes, y)
pl.plot(x, bary2, 'b-', label='second')
pl.plot(x, bary1, 'g-', label='first' )
pl.legend()
#pl.plot(x, naive, 'r-')
pl.figure()
true = f(x)
pl.semilogy(x, np.abs(bary2 - true)/np.abs(true),'b-', label='second')
pl.semilogy(x, np.abs(bary1 - true)/np.abs(true),'g-', label='first' )

#pl.semilogy(x, np.abs(naive- true)/np.abs(true),'r-')
pl.legend()
pl.show()

