from flask import Flask, request, render_template
import pymysql
app = Flask(__name__)
def select(query):
    db = None
    cur = None
    try:
        db = pymysql.connect(host='192.168.1.4', user='root', password='1234', db='mysql', charset='utf8')
        cur = db.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None
    finally:
        if cur:
            cur.close()
        if db:
            db.close()
@app.route('/temp_humid_chart')
def lm35_chart():
    sql = "SELECT DATATIME, TEMP FROM temperature ORDER BY DATATIME ASC LIMIT 100"
    result = select(sql)
    if result is None:
        return "Failed to retrieve data from database", 500
    return render_template("temp_humid_chart.html", result=result)
@app.route('/<path:path>')
def catch_all(path):
    return "This page does not exist", 404
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
