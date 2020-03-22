# Web Assignment: Kanban Board![kanban board preview](https://github.com/nathantorento/CS162/blob/master/kanban/Kanban_preview.png "Kanban Board Preview")

## Instructions


### Ensure you have python3 installed.
https://www.python.org/downloads/

### Ensure you have the package "virtualenv" installed.
```bash
pip3 install virtualenv
```

### Set up virtual environment
To ensure that you have the needed dependencies required for this project and that they don't conflict with whatever you may currently have installed on your computer, we will need to create a virtual environment in your directory of choice. Be sure this directory is where you will download this project folder to.

```bash
python3 -m virtualenv venv
source venv/bin/activate
```

### Install dependencies
Now, manually install the dependencies specified in the requirements.txt file found in this project folder.

```bash
pip3 install -r requirements.txt
```

### Finally, run the application
```bash
python3 run.py
```

### Credits:
Thank you to Zineb Salimi, Juan Carlos, and Jason Liang for the help and framework they've provided for me to model my project on. I struggled particularly on how to route the links to each other and transfer the html form inputs into the SQLAlchemy database. Their code provided a lot of insight about how I could overcome these obstacles. Furthermore, referred to a lot of stackexchange forums for a lot of the workaround codes like recoding the 'url_for' and using "app.app_context" to import files from local directories.
