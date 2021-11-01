import json
import numpy

# Add the variables needed in order.
variableOrder = ['gyrox', 'gyroy', 'gyroz'] 

""" 
@Brief
    parse collected data in json file
@params
    str f: filename of json
    boolean keyable: whether push button is used to indicate the beginning and end of data
@returns
    array in which each line is a sample
"""
def parse(f, keyable=True):
    with open(f,'r') as load_f:
        load_dict = json.load(load_f)
    
    records = {}
    for entry in load_dict:
        time, value, variable = entry['time'], entry['value'], entry['variable']
        realTime = time[:-3]
        try:
            records[realTime][variable] = value
        except KeyError:
            records[realTime] = {variable:value}
    records = sorted(records.items(), key=lambda x: x[0], reverse=False)
    data = []
    if(keyable):
        """ states
            0: not reading data
            1: reading when key1 = 1
            2: reading data
            3: reading when key1 = 0
        """
        state = 0
        for item in records:
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
                data.append([item[1][name] for name in variableOrder])
    else:
        for item in records:
            data.append([item[1][name] for name in variableOrder])
    return numpy.mat(data)

def main():
    data = parse("export.json", False)
    print(data)

if __name__ == "__main__":
    main()