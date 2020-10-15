# LogFile2MySQL
This project purpose is converting Apache's log file into MySQL

# Parameters and configurations
Both Apache's log folder and MySQL config file is under config's folder. 
There are 2 config files, which is dev.py and prod.py.
* dev.py is for development environment

* prod.py is for production environent

You can choose one of those file that need to be use for this project at **main.py**.

```python
#you can change here into config.prod for production environment
import config.dev as cfg 
```



1.Apache Log Configuration

```python
apache = {
    "logFolder"         :   "your apache log's folder"
}

```
2.MySQL Configuration

```python
#MySQL Configuration
mysql = {
    "host"      :   "localhost",
    "user"      :   "your database user",
    "password"  :   "your database password",
    "db"        :   "your database name"
}
```

3.Software dependencies

This program is requires **pmysql** dependency to be working, first thing to do is install **pmysql** under you operating system.

4.Running the program

To run the program, you can copy entire folder that already have python files.

Then is simply run the project by running : 

```bash
$ python3 main.py
```
