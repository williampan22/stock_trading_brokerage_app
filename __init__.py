from models import User, Role

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)