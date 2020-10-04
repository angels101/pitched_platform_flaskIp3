from flask_wtf.csrf import CsrfProtect
from app import create_app,db
from app.models import User
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager,Server

# Creating app instance can you hear me??
app = create_app('development')

manager = Manager(app)
manager.add_command('server',Server)
csrf = CsrfProtect(app)

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db, User=User)


if __name__ =='__main__':
    manager.run()

   
    