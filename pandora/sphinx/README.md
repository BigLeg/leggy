#Sphinx
video site project

## Setup Instruction

```
cd /path/to/sphinx
```

### 1. Setup Mysql
Refer to [Cellar](https://github.com/BigLeg/cellar). __Remember to forward port 3306 out.__

### 2. Install Libs

```
pip install virtualenv
./setup-dev.sh
```

### 3. Create Tables
__Only do this once__

For Linux/Mac users:

```
source venv/bin/activate
python app/manage.py shell
>>> db.drop_all()
>>> db.create_all()
>>> exit
deactivate
```

For windows users:

```
venv\bin\activate.bat
python app/manage.py shell
>>> db.drop_all()
>>> db.create_all()
>>> exit
venv\bin\deactivate.bat
```

### 4. Configure Mode
Create `conf/local.py` according to `conf/local.py.EXAMPLE`. These modes are pre-defined:

* prod
* test
* dev-docker
* dev-local
* dev-frontend


* If you want to run server at docker, use `dev-docker`. 
* If you want to run server at local and want to use db, use `dev-local`.
* If you want to run server at local and don't use db, use `dev-fontend`.


### 5. Run Server

For Linux/Mac users:

```
source venv/bin/activate
python app/manage.py runserver
```

For Windows users:

```
venv\bin\activate.bat
python app/manage.py runserver
```

Then it starts a server at [http://localhost:5000](http://localhost:5000)

If you meet any problem in setting up Pandora, try this simple server.


## Note
__Don't push your videos into repository, because they are too large. I pushed it here only for demo__

