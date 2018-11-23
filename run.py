from sendit.database import Database
from sendit import app
from sendit.api import routes, authentication

db = Database()
db.create_tables()


if __name__ == "__main__":
    app.run(debug=True)
