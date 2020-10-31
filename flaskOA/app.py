from flask import Flask,render_template
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
# 实例化
migrate = Migrate()
# 使用sqlite来连接数据库
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# 设置信息 sqlite数据库链接格式
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///'+os.path.join(BASE_DIR,"sqlite2.db")
# 创建SQLAlchemy对象
db = SQLAlchemy(app)
migrate.init_app(app,db)



