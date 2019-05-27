from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from flask_script import Manager 
from flask_migrate import Migrate, MigrateCommand
from app import apl, db

migrate = Migrate(apl, db)
manager = Manager(apl)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()