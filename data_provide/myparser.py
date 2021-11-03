import json
import numpy
import matplotlib.pyplot as plt

# Add the variables needed in order.
variableOrder = ['gyrox', 'gyroy', 'gyroz', 'magx', 'magy', 'magz', 'accelx', 'accely', 'accelz'] 

""" 
@Brief
    parse collected data in json file
@params
    str f: filename of json
    int mode:
        0 -- get every data
        1 -- only get data until when key1 is pushed
        2 -- only get data from when key1 is pushed
        3 -- get data bewteen two times when key1 is pushed
    boolean keyable: whether push button is used to indicate the beginning and end of data
@returns
    array in which each line is a sample
"""
def parse(f, mode):
    with open(f,'r') as load_f:
        load_dict = json.load(load_f)
    
    records = {}
    for entry in load_dict:
        time, value, variable = entry['serie'], entry['value'], entry['variable']
        realTime = time[:-1]
        try:
            records[realTime][variable] = value
        except KeyError:
            records[realTime] = {variable:value}
    records = sorted(records.items(), key=lambda x: x[0], reverse=False)
    data = []
    if(mode >= 2):
        """ states
            0: not reading data
            1: reading when key1 = 1
            2: reading data
            3: reading when key1 = 0
        """
        state = 0
        for item in records:
            # print(item)
            if("key1" not in item[1].keys()):
                item[1]['key1'] = 0
            if(state == 0):
                if(int(item[1]['key1']) == 1):
                    state = 1
            elif(state == 1):
                if(int(item[1]['key1']) == 0):
                    state = 2
            elif(state == 2):
                if(int(item[1]['key1']) == 1):
                    state = 3
            else:
                if(int(item[1]['key1']) == 0):
                    state = 0
            if(state != 0):
                rec = [float(item[1][name]) for name in variableOrder]
                data.append(rec)
    elif(mode == 1):
        for item in records:
            if(int(item[1]['key1']) == 1):
                return numpy.array(data)
            # print(item)
            data.append([float(item[1][name]) for name in variableOrder])
    else:
        for item in records:
            if('key1' not in item[1].keys()):
                continue
            # print(item)
            data.append([float(item[1][name]) for name in variableOrder])
    return numpy.array(data)

def main():
    """ extract data from json file, and put every 30 sets of data into an array """
    data = parse("samples/walking/walking-for-test2.json", 3)

    output = numpy.empty(shape=[0, 30, 9])
    for i in range(data.shape[0] // 30):
        sample = data[i*30:i*30+30]
        output = numpy.concatenate((output, [sample]))
    print(output.shape)
    numpy.save("samples/walking/walking-for-test2.npy", output)


if __name__ == "__main__":
    main()