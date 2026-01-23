from flask import Flask, render_template, request
import os
import pymysql

app = Flask(__name__)
application = app     # IMPORTANT for Elastic Beanstalk

RDS_HOST= "localhost"
RDS_USER= "root"
RDS_PASSWORD= "root123"
RDS_DB=  "database-1"


def get_connection():
    return pymysql.connect(
        host=RDS_HOST,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DB,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def home():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    number = request.form["number"]

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, number) VALUES (%s, %s)",
            (name, number)
        )
        conn.commit()
        cursor.close()
        conn.close()
        msg = "Data inserted successfully!"
    except Exception as e:
        msg = f"Error: {str(e)}"

    return msg

@app.route("/users")
def users():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"users": data}
    except Exception as e:
        return {"error": str(e)}

# ==============================
# NEW PAGE: HTML TABLE VIEW
# ==============================
@app.route("/view-users")
def view_users():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("users.html", users=data)
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run()
