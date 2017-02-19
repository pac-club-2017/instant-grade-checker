from igc.controller import auth_controller
from igc.controller import dashboard_controller
from models import create_sql_alchemy

def register_controllers(app):
    db, User = create_sql_alchemy(app)

    models = {
        "user" : User
    }
    auth_controller.controller(app, models, db)
    dashboard_controller.controller(app, models, db)