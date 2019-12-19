# counters
Preparation of a file with readings of water and heat meters for the Rents program, based on data files from the remote reading system.

## Important for Windows
Before installing counters on Windows, You must install NSIS (Nullsoft Scriptable Install System). NSIS is a professional open source system to create Windows installers. 
https://nsis.sourceforge.io/Main_Page

## Install
### For Windows
1. Go to page: [python.org](https://www.python.org/) and download python, example: [python 3.8](https://www.python.org/ftp/python/3.8.0/python-3.8.0-amd64.exe)

2. Install python

3. Get application: counters.zip and unzip that you want

4. Run windows console and go to folder counters

5. Run command: `python -m venv venv`

6. Run command: `venv\Scripts\activate.bat`

7. Run command: `pip install -r requirements.txt`

8. Run command: `venv\Scripts\python.exe counters\counters.py`

   
## Install
1. Rozpakuj plik: counters.zip na c:\

2. Struktura po rozpakowaniu
C:\counters
    |-> counters
    |   |-> config
    |   |   |-> liczniki.dat
    |   |   |-> sciezki.dat - ścieżki do plików odczytów i wyniku
    |   |-> lib
    |   |-> resources
    |   |-> tmp
    |-> test
    |-> venv
    |-> Konwenter odczytów.lnk

3. W pliku sciezki.dat podaj odpowiednie ściezki

4. Skrót: Konwenter odczytów.lnk skopiuj na pulpit
