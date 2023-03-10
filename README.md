# README

Sequenzy is a small python program to mutate sequences of amino acids at predefined positions and create all possible combinations. The individual results are exported and saved as a FASTA file. 
In addition, a CVS and Excel file is created with the legend containing the change per export file. 

## Requirements


- python 3.7 or newer
  - Downlaod Python 3.11.2 for Windows: [Link](https://www.python.org/ftp/python/3.11.2/python-3.11.2-amd64.exe)
  - Download Side: [Link](https://www.python.org/downloads/)

- Libs
  - customtkinter
  - pandas
  - tabulate
  - openpyxl
  
---

## Install Python
Check your python installation.

Open a **Terminal** and run the command: 
``` bash
pyhton --version
```
The result should look like this:
``` bash
Python 3.11.2
```


## Install Lib

Libs can installed with pip manually or witht the included **requirements.txt** file.

Open a **Terminal** and run the command:

### Automated

``` bash
pip install -r requirements.txt
```

### Manual
``` bash
pip install customtkinter
pip install pandas
pip install tabulate
pip install openpyxl
```

---

## Usage

Open a **terminal** and navigate with the "CD" command to the directory which contains the program sequenzy.py.

For example:
``` bash
cd  %USERPROFILE%/Downloads/sequenzy
```
Then run the program with the command:

``` bash
python sequenzy.py
```

This will create in the same folder a new directory with the name 'output'.
This folder will be used to store the results.
