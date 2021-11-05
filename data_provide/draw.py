import numpy as np
import matplotlib.pyplot as plt

data = np.load("predict.npy")

def draw(data, name=None):
    for sample in range(data.shape[0]):
        plt.cla()
        X = []
        Y = [[] for i in range(9)]
        if(sample == 10):
            print(data[sample])
        for i in range(30):
            X.append(i)
            for j in range(6):
                Y[j].append(float(data[sample][i][j]))
        for i in range(6):
            plt.subplot(3, 3, i+1)
            plt.plot(X, Y[i], "r-o")
        if(name):
            plt.savefig(name)
        else:
            plt.savefig("predict%d.png" % (sample))
        for i in range(6):
            plt.subplot(3, 3, i+1)
            plt.cla()

def isValid(data):
  for dim in range(6):
    for i in range(25):
      flag = False
      future = [data[j][dim] for j in range(i, i+4)]
      if(dim < 3):
        flag = (max(future) - min(future)) < 30
      else:
        flag = (max(future) - min(future)) < 0.2
      if(flag):
          return False
  return True

if __name__ == '__main__':
    draw(np.load("realtime/samples.npy"))
    """
    testcases = np.empty(shape=[0, 30, 6])
    data = np.load("realtime/samples.npy")
    for j in range(len(data)):
        if(isValid(data[j])):
            print(j)
            testcases = np.concatenate((testcases, [data[j]]))
    """
    # print(testcases.shape)
    # np.save("samples/ropeskipping/ropeskipping7.npy", testcases)