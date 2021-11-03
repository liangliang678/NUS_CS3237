## README of data_provider ##

### myparser.py ###
Turns `.json` to `.npy` (readable by numpy). Data is extracted in array of shape (x, 30, 9).

### generate.py ###
Just to combine different `.npy` files (in the same catagory) into a single `.npy`, and create labels for them.

### merge.py ###
Read `.npy` files in different catagories as well as their labels and merge them into a single `.npy`.

### draw.py ###
Plot the samples in graphs.

### how they work? ###
1. Download json data from tago
2. Run ```myparser.py```. Don't forget to change input filename, parsing mode, and output filename in `main()`.
3. Run ```generate.py``` if there are more than 1 file in the same catagory, to get a single `.npy` file.
4. Run ```merge.py``` to get an overall sample file and label file.
5. Run ```draw.py``` if you want to look at plot graph within data in a single `.npy` file.