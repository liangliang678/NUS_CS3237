import numpy as np
import matplotlib.pyplot as plt

data = np.load("samples/test_samples.npy")
# print(data)

for sample in range(data.shape[0]):
    plt.cla()
    X = []
    Y = [[] for i in range(9)]
    if(sample == 10):
        print(data[sample])
    for i in range(30):
        X.append(i)
        for j in range(9):
            Y[j].append(float(data[sample][i][j]))
    for i in range(9):
        plt.subplot(3, 3, i+1)
        plt.plot(X, Y[i], "r-o")
    plt.savefig("samples/testImages/test%d.png" % sample)
    for i in range(9):
        plt.subplot(3, 3, i+1)
        plt.cla()
    
