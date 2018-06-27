## Organize data in a way where it can be easily accessed

### Clean theoretical data
After recieving theoretical data load these up into a single dataframe.
Format should be universal so this should be easier than the experimental data.

### Clean experimental data
Files have all the information about the specific run in their name but these names don't have a universal format.
Write a script that goes through each file and create labels by hand and add each spectrum to a pandas dataframe.
After this is finished we will have a single file containing all the spectra with it's corresponding labels.

### Functionality for the dataframe
Write class which loads up our dataframe containing all the experimental and theoretical data.
Functions that can filter data, return individual spectrums, etc..
