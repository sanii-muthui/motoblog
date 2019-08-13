from app import create_app, db
from app.models import User, Role, Comment
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app('development')
manager = Manager(app)
manager.add_command('server',Server)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# unit testing
@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User )
    
if __name__ == '__main__':
    manager.run()
