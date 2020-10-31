from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
app = Flask(__name__)
# 设置链接mysql数据库的信息
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:root@127.0.0.1:3306/shijintao"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(os.path.abspath(os.path.dirname(__file__)),"sqlite.db")
db = SQLAlchemy(app)
class Person(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(32),nullable=False)


if __name__ == '__main__':
    # app.run(debug=True)
    db.create_all()