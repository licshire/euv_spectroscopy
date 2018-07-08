# Extreme Ultraviolet Spectroscopy

## Data preperation
Theoretical and Experimental data both came in different formats and different experimental measurements also came in different formats. Organize data into a usable format.

Finished up on this data is now in 2 .csv files which are easily usable with pandas.

## Experimental data calibration
Every spectrum in our experimental data is of length (1,2048). One intensity value for each channel. We have to find a function that converts our channel numbers to wavelengths.

## Theoretical data merge
Unlike in our experimetal data our theoretical data has charge states seperated. We have to merge these seperate charge states together. Also each wavelength responds to one intensity, we have to distribute this intensity around that wavelength.