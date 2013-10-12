
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

def findLinearRegression(values, expected, alpha, maxIters):
    points = len(values[0])
    ones = [1]*points
    values.insert(0, ones)
    variables = len(values)
    B = [0]*variables
    multiplier = alpha / points
    for iterations in range(0,maxIters):
        leastSquares = [0]*variables
        for curPoint in range(0,points):
            error = 0
            for q in range(0,variables):
                error += B[q]*values[q][curPoint]
            error -= expected[curPoint]
            for q in range(0,variables):
                leastSquares[q] += error*values[q][curPoint]
        for q in range(0,variables):
            B[q] -= multiplier*leastSquares[q]
    print B
    return B

findLinearRegression([Xs], Ys, 0.07, 1500)


x3d = [4,7,9,2,5,11,1,12]
y3d = [9,4,0,5,1,12,10,3]
z3d = [23.4997,12.4782,3.5672,13.6507,4.9742,32.1762,25.1412,
       11.3057]
findLinearRegression([x3d,y3d], z3d, 0.01, 10000)
