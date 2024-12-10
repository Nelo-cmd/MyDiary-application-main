from app import createapp
from mydb import connect_db


app = createapp()
connect_db()

if __name__ == "__main__":
    app.run(debug = True)