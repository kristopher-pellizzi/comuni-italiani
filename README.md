# comuni-italiani
File in diversi formati contenenti informazioni sui comuni italiani

Informazioni recuperate dal sito dell' Istat e aggiornate al 19/02/2020.

Source: https://www.istat.it/it/archivio/6789

The repository also includes 2 python 3 scripts:

- *createNewJsonComuni.py*: opens 'comuni-italiani.json' and from its content creates 'comuni-italiani-short.json'
***NOTE:* the script uses a path on the local machine. The path should be changed in order to work properly**
- *storeComuniToDB.py*: tries to connect to a **local** instance of postgresql DB and stores 3 tables (regioni, province, comuni) in the database (called comuni).
