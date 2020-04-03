# dhbw-networking
Implementation of the Prim algorithm to generate a minimal spanning tree
for simulation of a Layer 2 (OSI) network in Python.


![Python Version][python-image]
## Usage
Python version 3.8.2 or greater is required to run this program.

To start the program, cd into the directory of `main.py` at the document root and use

```
python main.py -i <importpath>
```
This starts the program and solves the graph that is declared in the file at \<importpath\> (if the file is valid, more on 
this in Data Specifications).
Optional arguments include:
* -v: run the program verbose
* -d: run the program with debug messages 
* -t: run the unit tests
* -e \<exportfile\>: export the solved graph to a given file location (file can not exist yet)

For a full list on this, use `-h`.

Multiple commands can be combined. They will be executed in the order they were put in. So for example, `python main.py 
-t -i somefile.txt` runs the unit tests, then imports and solves `somefile.txt`.

## Data Specifications
Following specifications must be regarded when importing:
* File has to be .txt
* File must start with `Graph [name] {` in a separate line before any definition can be made
* File must end with a `}` in a separate line
* File needs to have a new line for every definition need to be in a new line
* Definitions must terminate with `;`
* Node definitions must be of format `[NODE NAME] = [NODE ID];`
* Edge definitions must be of format `[FROM] - [TO] : [COST];` 
(`[FROM]` and `[TO]` must be String, `[COST]` must be integer)
* Comments must start with `//`
* Every definition must adhere to the maximum values set by the constants in `Controllers/FileController.py`


[python-image]: https://img.shields.io/badge/python-v3.8.2+-brightgreen?style=flat-square&logo=python