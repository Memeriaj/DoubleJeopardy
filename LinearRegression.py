from numpy import loadtxt, zeros, ones, array, linspace, logspace, mean, std, arange
from pylab import scatter, show, title, xlabel, ylabel, plot, contour
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


Xs = [2.07, 2.37, 2.54, 2.54, 2.55, 2.79, 2.91, 3.04,
      3.11, 3.16, 3.33, 3.38, 3.41, 3.42, 3.53, 3.64, 3.67,
      3.93, 4.05, 4.25, 4.34, 4.38, 4.42, 4.61, 4.69, 4.98,
      5.04, 5.07, 5.42, 5.44, 5.46, 5.57, 5.60, 5.69, 5.72,
      5.85, 6.20, 6.35, 6.48, 6.74, 6.86, 7.02, 7.08, 7.15,
      7.47, 7.60, 7.74, 7.77, 7.83, 7.93]

Ys = [0.78, 0.92, 0.91, 0.91, 0.94, 0.97, 0.96, 0.91,
      0.94, 0.96, 0.90, 0.91, 0.94, 0.97, 1.05, 1.01, 0.96,
      0.97, 1.08, 1.15, 1.03, 1.01, 0.97, 1.09, 1.06, 1.12,
      1.03, 1.09, 1.07, 1.16, 1.08, 1.11, 1.10, 1.16, 1.14,
      1.08, 1.13, 1.12, 1.20, 1.21, 1.13, 1.12, 1.21, 1.25,
      1.25, 1.18, 1.19, 1.30, 1.26, 1.26]

#Evaluate the linear regression

def feature_normalize(X):
    '''
    Returns a normalized version of X where
    the mean value of each feature is 0 and the standard deviation
    is 1. This is often a good preprocessing step to do when
    working with learning algorithms.
    '''
    mean_r = []
    std_r = []

    X_norm = X

    n_c = X.shape[1]
    for i in range(n_c):
        m = mean(X[:, i])
        s = std(X[:, i])
        mean_r.append(m)
        std_r.append(s)
        X_norm[:, i] = (X_norm[:, i] - m) / s

    return X_norm, mean_r, std_r


def compute_cost(X, y, theta):
    '''
    Comput cost for linear regression
    '''
    #Number of training samples
    m = y.size

    predictions = X.dot(theta)

    sqErrors = (predictions - y)

    J = (1.0 / (2 * m)) * sqErrors.T.dot(sqErrors)

    return J


def gradient_descent(X, y, theta, alpha, num_iters):
    '''
    Performs gradient descent to learn theta
    by taking num_items gradient steps with learning
    rate alpha
    '''
    m = y.size
    J_history = zeros(shape=(num_iters, 1))

    for i in range(num_iters):

        predictions = X.dot(theta)

        theta_size = theta.size

        for it in range(theta_size):

            temp = X[:, it]
            temp.shape = (m, 1)

            errors_x1 = (predictions - y) * temp

            theta[it][0] = theta[it][0] - alpha * (1.0 / m) * errors_x1.sum()

        J_history[i, 0] = compute_cost(X, y, theta)

    return theta, J_history

#Load the dataset
data = loadtxt('ex1data2.txt', delimiter=',')


#Plot the data
new = []

for val in Xs:
    new.append([val])
    
X = array(new)
y = array(Ys)

# X = array([X])
X = data[:, :2]
print X
y = data[:, 2]
print y

# scatter(X, y, marker='o', c='b')



#number of training samples
m = y.size

y.shape = (m, 1)

#Scale features and set them to zero mean
x, mean_r, std_r = feature_normalize(X)

#Add a column of ones to X (interception data)

it = ones(shape=(m, x.ndim+1))
print "it"
print it
print it[:, 1]
it[:, 1:x.ndim+1] = x
print it

#Some gradient descent settings
iterations = 100
alpha = 0.01

#Init Theta and Run Gradient Descent
theta = zeros(shape=(x.ndim+1, 1))

theta, J_history = gradient_descent(it, y, theta, alpha, iterations)
print theta, J_history
result = it.dot(theta).flatten()
# plot(array(new), result)
show()
plot(arange(iterations), J_history)
xlabel('Iterations')
ylabel('Cost Function')
show()

#Predict price of a 1650 sq-ft 3 br house
# price = array([1.0,   ((1650.0 - mean_r[0]) / std_r[0]), ((3 - mean_r[1]) / std_r[1])]).dot(theta)

data = loadtxt('', delimiter=',')
