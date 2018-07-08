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

### Loading and accessing dataframe

Loading up organized data

```
from spec_db import *

# Load up data
data = SpecBase('specBase.csv')

data.df # returns data in a DataFrame

# Filter dataframe
filtered = data.getTable(max_energy=5000,min_energy=1000,max_current=160,min_current=0,element=[26, 54], fstring='EUV')
```

Although this may help loading it up like this:
```
data = df.read_csv('specBase.csv', delimiter=',')
```
Might be more convenient.

*(2018/06/29):* Original plan was to load experimental and theoretical data into a single dataframe, for now we will keep them seperate
*(2018/07/06):* Finished merging of theoretical dataset into a single .csv
