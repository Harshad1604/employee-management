from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import requests
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = "supersecretkey"

def get_db_connection():
    conn = sqlite3.connect("employee.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    employees = conn.execute("SELECT * FROM employee").fetchall()
    conn.close()
    return render_template("index.html", employees=employees)

@app.route("/add", methods=["POST"])
def add():
    try:
        emp_id = request.form["id"]
        name = request.form["name"]
        salary = request.form["salary"]
        conn = get_db_connection()
        conn.execute("INSERT INTO employee (id, name, salary) VALUES (?, ?, ?)", (emp_id, name, salary))
        conn.commit()
        conn.close()
        flash("Employee added successfully.", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("index"))

@app.route("/update", methods=["POST"])
def update():
    try:
        emp_id = request.form["id"]
        name = request.form["name"]
        salary = request.form["salary"]
        conn = get_db_connection()
        conn.execute("UPDATE employee SET name = ?, salary = ? WHERE id = ?", (name, salary, emp_id))
        conn.commit()
        conn.close()
        flash("Employee updated successfully.", "success")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM employee WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Employee deleted successfully.", "success")
    return redirect(url_for("index"))

@app.route("/chart")
def chart():
    conn = get_db_connection()
    data = conn.execute("SELECT name, salary FROM employee ORDER BY salary DESC LIMIT 5").fetchall()
    conn.close()

    names = [row["name"] for row in data]
    salaries = [row["salary"] for row in data]
    plt.figure(figsize=(8, 4))
    plt.bar(names, salaries, color="skyblue")
    plt.title("Top 5 Salaried Employees")
    plt.xlabel("Name")
    plt.ylabel("Salary")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    return jsonify({"chart": img})

@app.route("/location")
def location():
    try:
        res = requests.get("https://ipinfo.io")
        data = res.json()
        loc = data.get("city", "Unknown") + ", " + data.get("region", "Unknown")
        return jsonify({"location": loc})
    except:
        return jsonify({"location": "Error retrieving location"})

@app.route("/temperature")
def temperature():
    try:
        api_key = "13a389e6a7777f4e06f7e81b9d4d8373"
        city = "Mumbai"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        temp = response.json()["main"]["temp"]
        return jsonify({"temperature": f"{temp}°C"})
    except:
        return jsonify({"temperature": "N/A"})

if __name__ == "__main__":
    app.run(debug=True)
