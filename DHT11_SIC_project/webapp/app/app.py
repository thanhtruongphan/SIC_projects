from flask import Flask, render_template, jsonify
import pymysql
import time

app = Flask(__name__)

def get_data_from_db():
    try:
        connection = pymysql.connect(
            host='192.168.1.4',
            user='root',
            password='1234',
            db='mysql',
            charset='utf8'
        )
        cursor = connection.cursor()
        sql = "SELECT DATATIME, TEMP FROM temperature ORDER BY DATATIME DESC LIMIT 1"
        cursor.execute(sql)
        result = cursor.fetchone()
        return {"time": result[0], "temperature": result[1]} if result else None
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    data = get_data_from_db()
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "No data available"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
