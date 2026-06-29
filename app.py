from flask import Flask, render_template, request, redirect, session
import sqlite3
import bcrypt


app = Flask(__name__)

app.secret_key = "secure_secret_key"


# Database

def create_db():

    conn = sqlite3.connect("database.db")

    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)


    conn.commit()
    conn.close()



create_db()



# Register

@app.route("/register", methods=["GET","POST"])

def register():

    if request.method=="POST":

        username = request.form["username"]
        password = request.form["password"]


        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )


        try:

            conn = sqlite3.connect("database.db")

            cursor = conn.cursor()


            cursor.execute(
                "INSERT INTO users(username,password) VALUES (?,?)",
                (
                    username,
                    hashed
                )
            )


            conn.commit()

            return redirect("/")


        except:

            return "Username already exists"



    return render_template("register.html")





# Login

@app.route("/", methods=["GET","POST"])

def login():

    if request.method=="POST":


        username=request.form["username"]

        password=request.form["password"]



        conn=sqlite3.connect("database.db")

        cursor=conn.cursor()


        cursor.execute(
            "SELECT password FROM users WHERE username=?",
            (username,)
        )


        user=cursor.fetchone()



        if user and bcrypt.checkpw(
            password.encode(),
            user[0]
        ):

            session["user"]=username

            return redirect("/dashboard")


        else:

            return "Invalid Login"



    return render_template("login.html")






# Dashboard

@app.route("/dashboard")

def dashboard():

    if "user" in session:

        return render_template(
            "dashboard.html",
            user=session["user"]
        )


    return redirect("/")






# Logout


@app.route("/logout")

def logout():

    session.clear()

    return redirect("/")





if __name__=="__main__":

    app.run(debug=True)
