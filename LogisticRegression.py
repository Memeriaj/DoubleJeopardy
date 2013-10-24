def findLogisticRegression(values, expected, alpha, degree, maxIter):
    def expectedValue(equation, slopes):
        linearCombo = 0
        for q in range(0, len(equation)):
            linearCombo += equation[q]*slopes[q]
        return 1/(1+math.exp(-linearCombo))
