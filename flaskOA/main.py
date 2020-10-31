from app import app
from views import *
from flask_script import Manager
from flask_migrate import MigrateCommand # 导入命令
# 管理app
manager = Manager(app)
# 安装命令
manager.add_command("db",MigrateCommand)
if __name__ == '__main__':
    # db.drop_all()
    # manager.run()
    app.run(debug=True)
    # db.create_all()