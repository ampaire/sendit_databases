from app.database import Database
from app import app
from app.api.routes import register_new_user
db = Database()
db.create_tables()
db.drop_tables

if __name__ == "__main__":
    app.run(debug= True)