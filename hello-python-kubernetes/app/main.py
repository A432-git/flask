from flask import Flask
import os
app = Flask(__name__)
import socket
import mysql.connector


@app.route("/")
def hello():
    return "Hello from Python!"


@app.route('/h')
def hello_2():
    # construct HTML output
    html = "<h3>Hello World from {hostname}!</h3>"
    html += "<h3>Your random word is: {random_word}</h3>"

    # yes, this is a terrible way to do this, but it works/is simple
    db = mysql.connector.connect(
        host=os.getenv("MYSQL_SERVICE_HOST"),
        port=os.getenv("MYSQL_SERVICE_PORT"),
        # host = 'localhost',
        # port = '3306',
        user="root",
        passwd="password",
        database="randomizer",
        auth_plugin="mysql_native_password"
    )

    cursor = db.cursor()
    cursor.execute("select word from random_words order by rand() limit 1;")
    res = cursor.fetchall()

    return html.format(random_word=res[0][0], hostname=socket.gethostname())


if __name__ == "__main__":
    app.run(host='0.0.0.0')
