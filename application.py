from flask import Flask, render_template, request
import os
import pymysql

app = Flask(__name__)
application = app  # Elastic Beanstalk compatibility

RDS_HOST = os.getenv("DB_HOST")
RDS_USER = os.getenv("DB_USER")
RDS_PASSWORD = os.getenv("DB_PASSWORD")
RDS_DB = os.getenv("DB_NAME")



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
    app.run(host="0.0.0.0", port=5000, debug=True)
