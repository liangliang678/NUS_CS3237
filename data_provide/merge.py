import numpy as np
import random

"""make test samples and labels"""
def makeTest():
    running = np.load("samples/running/running-for-test.npy")
    walking = np.load("samples/walking/walking-for-test.npy")
    skipping = np.load("samples/ropeskipping/skipping-for-test4.npy")


    print(running.shape, walking.shape)

    all_running = running.reshape((running.shape[0]*30, 6))
    all_walking = walking.reshape((walking.shape[0]*30, 6))
    all_skipping = skipping.reshape((skipping.shape[0]*30, 6))

    testcases = np.empty(shape=[0, 30, 6])
    testlabels = []

    
    for i in range(20):
        index = random.randint(0, running.shape[0]*30-30)
        sample = all_running[index:index+30]
        testcases = np.concatenate((testcases, [sample]))
        testlabels.append(1)

    for i in range(20):
        index = random.randint(0, walking.shape[0]*30-30)
        sample = all_walking[index:index+30]
        testcases = np.concatenate((testcases, [sample]))
        testlabels.append(0)
    
    for i in range(20):
        index = random.randint(0, skipping.shape[0]*30-30)
        sample = all_skipping[index:index+30]
        testcases = np.concatenate((testcases, [sample]))
        testlabels.append(2)

    np.save("samples/test_samples.npy", testcases)
    np.save("samples/test_labels.npy", np.array([testlabels]))

    print(testcases)
    print(np.array([testlabels]))

""" merge running samples and walking samples into one sample file"""
def merge():
    running = np.load("samples/running/running_samples.npy")
    walking = np.load("samples/walking/walking_samples.npy")
    ropeskipping = np.load("samples/ropeskipping/ropeskipping_samples.npy")
    print(running.shape, walking.shape, ropeskipping.shape)
    running_labels = np.load("samples/running/running_labels.npy")
    walking_labels = np.load("samples/walking/walking_labels.npy")
    ropeskipping_labels = np.load("samples/ropeskipping/ropeskipping_labels.npy")
    print(running_labels.shape, walking_labels.shape, ropeskipping_labels.shape)

    samples = np.concatenate((running, walking, ropeskipping), axis=0)
    labels = np.concatenate((running_labels, walking_labels, ropeskipping_labels), axis=1)

    print(samples.shape, labels.shape)

    np.save("samples/samples.npy", samples)
    np.save("samples/labels.npy", labels)

if __name__ == "__main__":
    makeTest()
    # merge()

