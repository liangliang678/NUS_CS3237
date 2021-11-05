import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import torch.optim as optim
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader

torch.manual_seed(1)

class RNNModel(nn.Module):
    def __init__(self,BATCH_SIZE, HIDDEN_SIZE, OUTPUT_SIZE, NUM_LAYERS=2):
        super().__init__()

        self.rnn = nn.RNN(
            #batch_size=BATCH_SIZE,
            input_size =6,
            hidden_size = HIDDEN_SIZE,  # rnn hidden unit
            num_layers=NUM_LAYERS,  # number of rnn layer
            batch_first=True,  # input & output will has batch size as 1s dimension. e.g. (batch, time_step, input_size)
        )
        self.fc = nn.Linear(HIDDEN_SIZE, OUTPUT_SIZE)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x, h_state):
        output, h_state = self.rnn(x.to(torch.float32), h_state)
        output = output[:,-1,:]
        output = self.fc(output)
        output = self.softmax(output)
        #print('FFFFFFFFFFFFFFFFFFFFFFFFFF')
        return output,h_state
        


def train(model, LEARNING_RATE, EPOCHS, trainset,model_path):
    criterion = nn.CrossEntropyLoss()
    #optimizer = torch.optim.SGD(model.parameters(), lr=LEARNING_RATE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    for epoch in range(EPOCHS):
        model.train()
        running_loss = 0.0

        for batchnum,batch in enumerate(trainset):
            x = batch[0]
            y = batch[1]
            h_state = None
        
            prediction, h_state = model(x, h_state)
            h_state = h_state.data
            #print(len(prediction))

            loss = criterion(prediction, y)  
            #print("loss:",batchnum,":",loss)
            optimizer.zero_grad()  
            loss.backward()  # backpropagation
            optimizer.step()  
            running_loss += loss

        print("epoch",epoch+1,"Finished",running_loss)

    checkpoint = {'model_state_dict': model.state_dict()}
    torch.save(checkpoint, model_path)
    print('Model saved in ', model_path)

def test(model, testset):
    model.eval()
    ALL = 0
    RIGHT = 0
    walkright = 0
    walkwrong = 0
    runright = 0
    runwrong = 0
    jumpwrong = 0
    jumpright = 0

    for batchnum,batch in enumerate(testset):
        x = batch[0]
        y = batch[1]

        h_state = None
        prediction, h_state = model(x, h_state)

        result = 0

        for i in range(len(prediction)):
            p = prediction[i].detach().numpy().tolist()
            result = p.index(max(p))
            # if prediction[i][0]<prediction[i][1]:
            #     result = 1
            #print(result)
            #print(y[i])
            print(result)
            if result == 0 and y[i]==0:
                RIGHT = RIGHT + 1
                walkright = walkright+1
            if result != 0 and y[i]==0:
                walkwrong = walkwrong+1
            if result != 1 and y[i]==1:
                runwrong = runwrong+1
            if result == 1 and y[i]==1:
                RIGHT = RIGHT + 1
                runright = runright+1
            if result != 2 and y[i]==2:
                jumpwrong = jumpwrong+1
            if result == 2 and y[i]==2:
                RIGHT = RIGHT + 1
                jumpright = jumpright+1        
            ALL = ALL + 1
    print('ALL: '+str(ALL)+'   RIGHT: '+str(RIGHT))
    print('walkright:'+str(walkright)+'\n')
    print('walkwrong:'+str(walkwrong)+'\n')
    print('runright:'+str(runright)+'\n')
    print('runwrong:'+str(runwrong)+'\n')
    print('jumpright:'+str(jumpright)+'\n')
    print('jumpwrong:'+str(jumpwrong)+'\n')

'''
def predict(model,PREPATH,batchsize):
    model.eval()
    testdata = np.load(PREPATH)
    data = torch.from_numpy(testdata)
    temp =  torch.from_numpy(testdata)
    for i in range(batchsize-1):
        torch.cat((data,temp),0)
    h_state = None
    prediction, h_state = model(data, h_state)
    p = prediction[0].detach().numpy().tolist()
    result = p.index(max(p))
    return result
'''


def prepare_data(DATAPATH,LABELPATH,BATCH_SIZE):
    arraydata = np.load(DATAPATH)
    arraylabel = np.load(LABELPATH)
    arraylabel = arraylabel[0]
    print(arraydata.shape)
    print(type(arraydata))
    data = torch.from_numpy(arraydata)
    label = torch.from_numpy(arraylabel)

    datatensor = torch.split(data,BATCH_SIZE,dim = 0)
    labeltensor = torch.split(label,BATCH_SIZE,dim = 0)

    datalabel = [[],[]]


    for data in datatensor:
        datalabel[0].append(data)
    for label in labeltensor:
        datalabel[1].append(label)
    
    trainset = []
    
    for i in range(len(datalabel[0])):
        trainset.append([datalabel[0][i],datalabel[1][i]])
    return trainset

def split_data(custom_dataset):
    train_size = int(len(custom_dataset) * 0.8)
    test_size = len(custom_dataset) - train_size
    train_dataset, test_dataset = torch.utils.data.random_split(custom_dataset, [train_size, test_size])
    print('lentrain'+ str(train_size) +'lentest'+ str(test_size) )
    return train_dataset, test_dataset


class MyDataSet(Dataset):
    def __init__(self, loaded_data):
        self.data = loaded_data
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]

if __name__ == '__main__':
    if torch.cuda.is_available():
        device_str = 'cuda:{}'.format(0)
    else:
        device_str = 'cpu'
    device = torch.device(device_str)

    torch.manual_seed(0)

    DATAPATH = 'samples/samples.npy'
    LABELPATH = 'samples/labels.npy'

    MODELPATH = 'model.pt'
    
    BATCH_SIZE = 6
    HIDDEN_SIZE = 16
    OUTPUT_SIZE = 3

    dataset = prepare_data(DATAPATH,LABELPATH,BATCH_SIZE)
    trainset,testset = split_data(dataset)
    #print(trainset)


    model = RNNModel(BATCH_SIZE,HIDDEN_SIZE,OUTPUT_SIZE).to(device)
   
    LEARNING_RATE = 0.001
    EPOCHS = 80

    train(model, LEARNING_RATE, EPOCHS, trainset,MODELPATH)
    test(model,testset)

'''
    SPECIALTESTPATH = 'C:\\Users\\WU\\Desktop\\NUS\\IOT\\Project\\test_samples(7).npy'
    SPECIALLABELPATH = 'C:\\Users\\WU\\Desktop\\NUS\\IOT\\Project\\test_labels(7).npy'
    specialtest = prepare_data(SPECIALTESTPATH,SPECIALLABELPATH,BATCH_SIZE)
    #print(specialtest)
    test(model,specialtest)

    #SINGLETESTPATH = 
    #predict(model, SINGLETESTPATH, BATCH_SIZE)
'''

