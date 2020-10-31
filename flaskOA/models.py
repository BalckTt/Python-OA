from app import db
# 创建对象模型
class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    # 保存数据
    def save(self):
        db.session.add(self)
        db.session.commit()
    # 删除数据
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    # 更新数据
    def update(self):
        db.session.commit()

# 个人信息表
class Person(Base):
    __tablename__ = "person"
    name = db.Column(db.String(32),nullable=False)
    password = db.Column(db.String(32),nullable=False)
    nickname = db.Column(db.String(32),nullable=True)
    gender = db.Column(db.String(32),nullable=True)
    age = db.Column(db.Integer,nullable=True)
    job_num = db.Column(db.String(32),nullable=True)
    phone = db.Column(db.String(32),nullable=True)
    email = db.Column(db.String(32),nullable=True)
    picture = db.Column(db.String(64),nullable=True)
    address = db.Column(db.String(64),nullable=True)
    score = db.Column(db.Float,nullable=True)
    # 外键进行关联
    position_id = db.Column(db.Integer,db.ForeignKey("position.id"))
    # 设置关系属性
    positions = db.relationship("Position",backref="person")

# 职位与员工一对多关系
# 职位信息表
class Position(Base):
    __tablename__ = "position"
    name = db.Column(db.String(32),nullable=True)  # 职位名称
    level = db.Column(db.Integer) # 职级  1,2,3
    # 部门和职位的外键
    Department_id = db.Column(db.Integer,db.ForeignKey("department.id"))


# 职位和权限是多对多关系
# 权限表和职位表的中间表
permission_position = db.Table(
    "permission_position", # 表格名称
    db.Column("permission_id",db.Integer,db.ForeignKey("permission.id")),
    db.Column("position_id",db.Integer,db.ForeignKey("position.id"))
)

# 权限表
class Permission(Base):
    __tablename__ = "permission"
    name = db.Column(db.String(32)) # 权限名称
    desc = db.Column(db.Text) # 权限描述
    # 设置关系多对多表的关系属性
    positions = db.relationship("Position",
                                backref="permission",
                                secondary=permission_position)




# 部门和职位是一对多关系
# 部门表
class Department(Base):
    __tablename__ = "department"
    name = db.Column(db.String(32)) # 部门名称
    desc = db.Column(db.Text) # 部门描述
    positions = db.relationship("Position",backref="dept")

# 新闻模型类
class News(Base):
    __tablename__ = "news"
    title = db.Column(db.String(64))
    author = db.Column(db.String(32))
    ntime = db.Column(db.Date)
    content = db.Column(db.Text)
    picture = db.Column(db.String(128), nullable=True)

# 考勤模型类
class Attendance(Base):
    __tablename__ = "attendance"
    reason = db.Column(db.Text) # 请假原因
    atype = db.Column(db.String(32))
    adate = db.Column(db.Float) # 请假天数
    start_time = db.Column(db.Date)
    end_time = db.Column(db.Date)
    astauts = db.Column(db.String(32),default="申请中") # 假条状态
    examine = db.Column(db.String(32),nullable=True,default="") # 审核人
    # 考勤和职员的关系
    person_id = db.Column(db.Integer,db.ForeignKey("person.id"))