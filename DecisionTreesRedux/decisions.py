__author__ = 'Icarus'
def ID3(examples, targetAttribute, Attributes):
    root = node()
    pos = 0
    neg = 0
    for attribute in targetAttribute:
        if attribute:
            pos += 1
        else:
            neg += 1
    if neg == 0:
        root.goodLabel = True
        return root
    elif pos == 0:
        root.goodLabel = False
        return root
    elif len(Attributes) == 0:
        if pos >= neg:
            root.goodLabel = True
            return root
        else:
            root.goodLabel = False
            return root
    else:
        toBeRemoved = None
        informationGain = 0
        totalPos = 0
        totalNeg = 0
        eMaxPos = None
        eMinPos = None
        eMaxNeg = None
        eMinNeg = None
        for attribute in Attributes:
            maxPos = 0
            minPos = 1000
            maxNeg = 0
            minNeg = 1000
            cMax = 0
            cMin = 1000
            for i in range(0, len(examples) - 1):
                current = examples[i][attribute]
                if targetAttribute[i]:
                    totalPos += current
                    if current > maxPos:
                        maxPos = current
                    elif current < minPos:
                        minPos = current
                else:
                    totalNeg += current
                    if current > maxNeg:
                        maxNeg = current
                    elif current < minNeg:
                        minNeg = current
                if current > cMax:
                    cMax = current
                if current < cMin:
                    cMin = current
            v1 = totalPos / pos
            v2 = totalNeg / neg
            if (cMax - cMin) != 0:
                sMax = (v1 - cMin) / (cMax - cMin)
                sMin = (v2 - cMin) / (cMax - cMin)
                if (sMax - sMin) > informationGain:
                    informationGain = (sMax - sMin)
                    toBeRemoved = attribute
                    eMaxPos = maxPos
                    eMinPos = minPos
                    eMaxNeg = maxNeg
                    eMinNeg = minNeg
        if toBeRemoved == None:
            if pos >= neg:
                root.goodLabel = True
                return root
            else:
                root.goodLabel = False
                return root
        cutLine = 0
        if eMinPos > eMaxNeg:
            cutLine = (eMinPos + eMaxNeg) / 2
        elif eMinNeg > eMaxPos:
            cutLine = (eMinNeg + eMaxPos) / 2
        else:
            cutLine = (eMaxPos + eMinPos + eMaxNeg + eMinNeg) / 4
        root.cutLine = cutLine
        root.decision = toBeRemoved
        Attributes.remove(toBeRemoved)
        leftChild = list()
        leftChildTA = list()
        rightChild = list()
        rightChildTA = list()
        i = 0
        for example in examples:
            if example[toBeRemoved] < cutLine:
                leftChild.append(example)
                leftChildTA.append(targetAttribute[i])
            else:
                rightChild.append(example)
                rightChildTA.append(targetAttribute[i])
            i += 1
        root.leftChild = ID3(leftChild, leftChildTA, Attributes)
        root.rightChild = ID3(rightChild, rightChildTA, Attributes)
        return root


def getAnswer(question, tree):
    if tree.goodLabel != None:
        return tree.goodLabel
    point = question[tree.decision]
    if point <= tree.cutLine:
        return getAnswer(question, tree.leftChild)
    else:
        return getAnswer(question, tree.rightChild)


class node():
    def __init__(self):
        self.goodLabel = None
        self.leftChild = None
        self.rightChild = None
        self.decision = None
        self.cutLine = None