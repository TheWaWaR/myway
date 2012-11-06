
# For deploy

## check version
bins = {
    'ubuntu' : {
        'python': 'python',
        'pip'   : 'pip',
    }
    'arch'   : {
        'python': 'python2',
        'pip'   : 'pip2'
    }
}
with open('/proc/version', 'r') as f:
    version = f.read().lower()
for v in bins.keys():
    if version.find(v) > -1:
        version = v
        break

# commands        
python = bins[version]['python']
pip = bins[version]['pip']


# ============================================================
## Pip install
modules = [
    # install name, import name
    'flask',
    'flask_sqlalchemy',
    'flask_wtf',
    ('flask_uploads',  'flask.ext.uploads'),
    ('pillow', 'PIL')           # Image process
    'misaka',                   # Markdown parser
    'fabric',                   # Deploy tools
]

## System package install
packages = {
    'MySQLdb' : {
        'arch': 'mysql-python',
        'ubuntu': 'python-mysqldb'
    },
}

## Shell commands
shell = {
    'mkdir' : 'myway/static/uploads/images/thumbs',
    'python': 'manager.py create_db'
}

## SQL commands
sql = [
    'CREATE DATABASE myway CHARSET utf8 COLLATE utf8_general_ci;',
    "INSERT INTO users(login, password) VALUES('weet', 'hello123');",
    "INSERT INTO categories(name, descr) VALUES('None', 'Just none');"
]
