# GSselect
This repository provides a python example of using the 
Gemini Observatory API for triggering template observations
that are On Hold. Details of the ToO activation process are
given [here](https://www.gemini.edu/sciops/observing-gemini/phase-ii-and-s/w-tools/too-activation).
The document [urltoo_readme.txt](https://github.com/bryanmiller/gsselect/blob/master/urltoo_readme.txt)
give more details about the API.

The example triggering script is urltrigger.py but most of the 
code is for selecting a guide star. As of November 2018 guide 
stars are still required with the trigger and the API does
not support the new automated guide star selection features 
in the Observing Tool. The script gsselect.py mimics these 
features and should find an appropriate guide star if one is 
available in the UCAC4 catalog. 

## Installation
The scripts require a standard python distribution that includes 
numpy, matplotlib, astropy, requests, and [aplpy](http://aplpy.github.io). 

Then install the scripts by downloading and unpacking the zip
file or use git, e.g.

git clone https://github.com/bryanmiller/gsselect.git

