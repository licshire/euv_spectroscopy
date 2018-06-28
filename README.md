## Extreme Ultraviolet Spectroscopy

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