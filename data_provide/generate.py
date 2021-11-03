import numpy as np

dic = {"walking": 0, "running": 1, "rope-skipping": 2}

def main():
    filelist = ["samples/running/running1.npy",
                "samples/running/running2.npy",
                "samples/running/running3.npy",
                "samples/running/running4.npy",
                "samples/running/running5.npy",
                "samples/running/running6.npy"]
    data = np.empty(shape=[0, 30, 9])
    for file in filelist:
        samples = np.load(file)
        data = np.concatenate((data, samples))
    
    np.save("samples/running/running_samples.npy", data)
    print(data.shape)

    labels = np.full((1, data.shape[0]), dic["running"])
    np.save("samples/running/running_labels.npy", labels)


if __name__ == "__main__":
    main()