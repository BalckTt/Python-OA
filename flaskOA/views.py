from models import *
from flask import request,redirect
from app import app,render_template

from functools import wraps
import time
# 限制直接访问别的页面
def log_delimit(fun):
    @wraps(fun)
    def inner():
        person_name = request.cookies.get("person_name")
        # print("--------------------------------")
        # print(person_name)
        if person_name:
            return fun()
        return redirect("/")
    return inner


# 登录
@app.route("/")
def inedx():
    return render_template("login.html")

# 判断账号密码
@app.route("/ispwd/",methods=["GET","POST"])
def ispwd():
    str1 = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # print(username,password)
        # person_obj = Person()
        person_obj = Person.query.filter(Person.name==username,Person.password==password).first()
        if person_obj:
            # 将用户名保存到cookie中
            print("恭喜你登录成功")
            response = redirect("/index/")
            response.set_cookie("person_name", username)
            response.set_cookie('person_id', str(person_obj.id))
            return response
        str1 = "密码错误"

    return render_template("login.html",str=str1)

# 退出
@app.route("/exit/")
def exit():
    response = redirect("/")
    # 删除cookie
    response.delete_cookie("person_name")
    return response

# 首页
@app.route("/index/")
@log_delimit
def index():
    return render_template("首页.html")


# # 新闻管理
# @app.route("/news/")
# @log_delimit
# def news():
#     return render_template("news.html")

@app.route("/person/")
@log_delimit
def person():
    person_object = Person.query.all()
    # print(person_object)
    # [{"name":"sss","partment":"kaifa","position":"jingli"}]
    # list1 = []
    # for person in person_object:
    #     name = person.name # 职员名称
    #     position = person.positions.name # 职位名称
    #     department = person.positions.dept.name # 部门名称
    #     # print(name,position,department)
    #     list1.append({"name":name,"position":position,"department":department})

    # return render_template("person.html",person_object=person_object)
    return redirect("/person_list/")

# 完成系统中创建用户
@app.route("/add_person/")
def add_person():
    posi = Position.query.all()
    # list2 = a.positions.name
    dict1 = {}
    j=1
    for i in posi:
        dict1[j]=i.name
        j+=1
    # print(dict1)
        # list1.append(i.name)
    return render_template("add_person.html",dict1=dict1,posi=posi)


@app.route("/add_person2/",methods=["GET","POST"])
def add_person2():
    username = request.form.get("username")
    password = request.form.get("password")
    position_id = request.form.get("position_id")
    person = Person()
    person.name=username
    person.password=password
    person.position_id=position_id
    person.save()
    # print(username,password,position_id)
    # print(list1)
    return redirect("/person/")

# 职员管理-详情
@app.route("/detail_person/")
@log_delimit
def detail_person():
    # 获取git方式获取的参数
    id = request.args.get("id")
    # 获取id对应的数据库里面的值
    person = Person.query.get(id)
    # print(person)
    username = person.name
    password = person.password
    nickname = person.nickname
    gender = person.gender
    return render_template("detail_person1.html",person=person)


import os
# 职员管理-编辑
@app.route("/edit_person/",methods=["GET","POST"])
@log_delimit
def edit_person():
    if request.method =="GET":
        # a标签的get请求
        id = request.args.get("id")
        person = Person.query.get(id)
        # print(id)
        position = Position.query.all()
        return render_template("edit_person1.html",person = person,position=position)

    # 表单的POST请求
    else:
        id = request.form.get("id")
        username = request.form.get("username")
        password = request.form.get("password")
        nickname = request.form.get("nickname")
        gender = request.form.get("gender")
        age = request.form.get("age")
        # 获取照片
        photo = request.files.get("photo")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")
        position_id = request.form.get("position_id")
        # print(username,password,nickname,gender)

        # 照片操作
        if photo.filename:
            path = os.path.join("static/img/", photo.filename)
            photo.save(path)
        else:
            path = None
        # 更新个人信息
        person_obj = Person.query.get(id)
        # print(person_obj)
        person_obj.name=username
        person_obj.password=password
        person_obj.nickname=nickname
        person_obj.gender=gender
        person_obj.age=age
        person_obj.picture=path
        person_obj.email=email
        person_obj.phone=phone
        person_obj.address=address
        person_obj.position_id = position_id
        person_obj.update()
        # print(position)
        return redirect("/person/")


# 职员管理 删除
@app.route("/del_person/")
def del_person():
    id = request.args.get("id")
    person = Person.query.get(id)
    if person.picture!=None:
        os.remove(person.picture)
    person.delete()
    return redirect("/person/")

# 部门管理
@app.route("/department/")
@log_delimit
def department():
    department = Department.query.all()
    # print(department)
    return render_template("department1.html",department=department)

# 编辑部门管理
@app.route("/edit_department/",methods=["GET","POST"])
@log_delimit
def edit_department():
    if request.method == "GET":
        id = request.args.get("id")
        department_obj = Department.query.get(id)
        return render_template("edit_department1.html",department_obj=department_obj)
    else:
        id = request.form.get("department_id")
        # print(id)
        name = request.form.get("name")
        description = request.form.get("description")
        # print("1223444")
        department_obj = Department.query.get(id)
        print(department_obj)
        department_obj.name = name
        department_obj.desc = description
        department_obj.update()
        return redirect("/department/")

# 增加部门管理
@app.route("/add_department/",methods=["GET","POST"])
def add_department():
    if request.method == "GET":
        return render_template("add_department.html")
    else:
        name = request.form.get("name")
        desc = request.form.get("description")
        # print(name,desc)
        department_obj = Department()
        department_obj.name = name
        department_obj.desc = desc
        department_obj.save()
        return redirect("/department/")

# 删除部门管理
@app.route("/delete_department/")
def delete_department():
    id = request.args.get("id")
    # print(id)
    department_obj = Department.query.get(id)
    department_obj.delete()
    return redirect("/department/")

# 查看职位
@app.route("/look_position/",methods=["GET","POST"])
def look_position():
    if request.method == "GET":
        id = request.args.get("id")
        department_obj = Department.query.get(id)
        # print(department_obj)
        position_obj = department_obj.positions
        return render_template("look_position.html",position_obj=position_obj,department_obj=department_obj)

# 增加职位
@app.route("/add_position/",methods=["POST","GET"])
def add_position():
    if request.method == "POST":
        id = request.form.get("dept_id")
        name = request.form.get("name")
        level = request.form.get("level")
        position = Position()
        position.Department_id = id
        position.name=name
        position.level=level
        position.save()
        return redirect("/look_position/?id="+id)

# 编辑职位
@app.route("/edit_position/",methods=["GET","POST"])
def edit_position():
    if request.method == "POST":
        id = request.form.get("position_id")
        name = request.form.get("name")
        level = request.form.get("level")
        position_obj = Position.query.get(id)
        position_obj.name = name
        position_obj.level = level
        position_obj.update()
        dept = position_obj.dept
        dept_id = dept.id
        print(type(dept_id))
        dept_id = str(dept_id)
        return redirect("/look_position/?id="+dept_id)


# 删除职位
@app.route("/delete_position/")
def delete_position():
    id = request.args.get("id")
    po_id = Position.query.get(id)
    # 删除职位对应的员工
    person_obj = po_id.person
    for i in person_obj:
        i.delete()
    dept_id = po_id.dept
    dept_id = dept_id.id
    # 删除职位
    po_id.delete()
    return redirect("/look_position/?id="+str(dept_id))

# 搜索职员
@app.route("/search_person/")
def search_person():
    person_username = request.args.get("person_username")
    # 查询数据库
    # person_object = Person.query.filter(Person.name == person_username).all()
    # 模糊查询
    person_object = Person.query.filter(Person.name.like('%'+person_username+'%')).all()
    # 返回页面
    return render_template("person.html",person_object=person_object)


# 新闻管理
@app.route("/news/")
def news():
    news_obj = News.query.all()
    return render_template("news.html",news_obj=news_obj)

# 添加新闻
@app.route("/add_news/",methods=["GET","POST"])
def add_news():
    if request.method == "GET":
        return render_template("add_news.html")
    else:
        title = request.form .get("title")
        author = request.form.get("author")
        content = request.form.get("content")
        picture = request.files.get("picture")
        # 照片操作
        print(picture.filename)
        if picture.filename:
            path = os.path.join("static/img/", picture.filename)
            picture.save(path)
        else:
            path = None
        new_obj = News()
        new_obj.title = title
        new_obj.author = author
        new_obj.content = content
        new_obj.picture = path
        # 获取现在的时间精确到年月日
        # ret = time.strftime("%Y-%m-%d",time.localtime())
        from datetime import datetime
        new_obj.ntime = datetime.now()
        new_obj.save()
        return redirect("/news/")

# 新闻详情
@app.route("/detail_news/",methods=["GET","POST"])
def detail_news():
    if request.method == "GET":
        id = request.args.get("id")
        new_obj = News.query.get(id)
        return render_template("/detail_news.html/",new_obj=new_obj)

# 新闻编辑
@app.route("/edit_news/",methods=["GET","POST"])
def edit_news():
    if request.method == "GET":
        id = request.args.get("id")
        news_obj = News.query.get(id)
        return render_template("edit_news.html",news_obj=news_obj)
    else:
        id = request.form.get("news_id")
        title = request.form.get("title")
        author = request.form.get("author")
        content = request.form.get("content")
        picture = request.files.get("picture")
        if picture.filename:
            path = os.path.join("static/img/",picture.filename)
            picture.save(path)
        else:
            path = None
        news_obj = News.query.get(id)
        # 判断此新闻是否有照片路径
        if news_obj.picture != None:
            os.remove(news_obj.picture)
        news_obj.title = title
        news_obj.author = author
        news_obj.content = content
        news_obj.picture = path
        # 时间的保存
        from datetime import datetime
        news_obj.ntime = datetime.now()
        news_obj.update()
        # return "1234565"
        return redirect("/news/")

# 新闻删除
@app.route("/delete_news/")
def delete_news():
    id = request.args.get("id")
    news_obj = News.query.get(id)
    if news_obj.picture != None:
        os.remove(news_obj.picture)
    news_obj.delete()
    return redirect("/news/")

# 个人考勤管理
# 考勤记录
@app.route("/attendance_me/")
def attendance_me():
    person_id = request.cookies.get("person_id")
    # print(type(person_id))
    att_obj = Attendance.query.filter(Attendance.person_id == int(person_id)).all()
    return render_template("attendance.html",att_obj_list=att_obj)

import datetime
# 考勤申请
@app.route("/apply_attendance/",methods=["GET","POST"])
def apply_attendance():
    reason = request.form.get("reason")
    type = request.form.get("type")
    day = request.form.get("day")
    start = request.form.get("start")
    end = request.form.get("end")
    p_id = request.cookies.get("person_id")
    # 保存到数据库
    attendance_obj = Attendance()
    attendance_obj.reason = reason
    attendance_obj.atype = type
    attendance_obj.adate = day
    attendance_obj.start_time = datetime.datetime.strptime(start,"%Y-%m-%d")
    attendance_obj.end_time = datetime.datetime.strptime(end,"%Y-%m-%d")
    attendance_obj.person_id = p_id
    attendance_obj.save()
    return redirect("/attendance_me/")

# 下属考勤
@app.route("/att_list_sub/",methods=["GET","POST"])
def att_list_sub():
    posi_obj = request.cookies.get("person_id")
    po_obj = Person.query.get(posi_obj)
    posi_obj = po_obj.positions.level
    print(posi_obj)
    # 查询当前用户下比当前职员职级小的人
    position_obj = Position.query.filter(Position.Department_id == po_obj.positions.Department_id).all()
    print(position_obj)
    list1 = []
    for i in position_obj:
        # person_obj = Person.query.filter(Person.position_id == i.id)
        if posi_obj < i.level:
            person_obj = Person.query.filter(Person.position_id == i.id).first()
            id2 = person_obj.id
            obj = Attendance.query.filter(Attendance.person_id == id2).first()
            list1.append(obj)
    return render_template("attendence_down.html",list1=list1)

#修改下属考勤状态
@app.route("/update_att_sub/")
def update_att_sub():
    id = request.args.get("id")
    status = request.args.get("status")
    att_obj = Attendance.query.get(id)
    att_obj.astauts = status
    person_name = request.cookies.get("person_name")
    att_obj.examine = person_name # 审核人
    att_obj.update()
    return redirect("/att_list_sub/")

# 分页
@app.route("/fytest/")
def fytest():
    pagination_obj = Person.query.paginate(2,1)
    for page in pagination_obj.iter_pages():
        print(page)
    return "分页"

# 分页开始
@app.route("/person_list/")
def person_list():
    # 获取前端传过来的页码
    page = int(request.args.get("page",1))
    # 查询数据库中的数据
    pagination_obj = Person.query.paginate(page,1)
    pagination_obj_list = pagination_obj.items

    # 3.判断页码范围
    if page < 3:
        start = 0
        end=5
    elif page >pagination_obj.pages-3:
        start = pagination_obj.pages-5
        end=pagination_obj.pages
    else:
        start = page-3
        end = page+2

    # 2.生成页码
    page_page = range(1,pagination_obj.pages+1)[start:end]
    return render_template('person.html',pagination_obj_list=pagination_obj_list,page_page=page_page,
                           pagination_obj=pagination_obj)


# 权限管理
@app.route("/permission/")
def permission():
    per_obj_list = Permission.query.all()
    return render_template("permission.html",per_obj_list=per_obj_list)

# 增加权限
@app.route("/add_permission/",methods=["GET","POST"])
def add_permission():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        permission_obj = Permission()
        permission_obj.name = name
        permission_obj.desc = description
        permission_obj.save()
        # 重定向
        return redirect("/permission/")
    return render_template("add_permission2.html")

# 修改权限
@app.route("/edit_permission/",methods=["GET","POST"])
def edit_permission():
    if request.method == "GET":
        id1 = request.args.get("id")
        permission_obj = Permission.query.get(id1)
        return render_template("edit_permission.html",permission_obj=permission_obj)
    else:
        id = request.form.get("id")
        name = request.form.get("name")
        desc = request.form.get("description")
        permission_obj = Permission.query.get(id)
        permission_obj.name = name
        permission_obj.desc = desc
        permission_obj.update()
        return redirect("/permission/")


# 删除权限
@app.route("/delete_permission/")
def delete_permission():
    id = request.args.get("id")
    permission_obj = Permission.query.get(id)
    permission_obj.delete()
    return redirect("/permission/")


# -----------------------------关联职位---------------------------------
# @app.route("/position_permission/")
# def position_permission():
#     id = request.args.get("id")
#     permission_obj = Permission.query.get(id)
#     # 查询所有的职位以及职位部门
#     position_obj = Position.query.all()
#     return render_template("position_permission.html",permission_obj=permission_obj,position_obj=position_obj)
@app.route('/position_permission/', methods=['GET', 'POST'])
def position_permission():
    if request.method == 'GET':
        # 3.获取权限id
        per_id = request.args.get('id')
        permission_obj = Permission.query.get(per_id)
        # 4.查询权限对应的职位对象对象
        per_obj = Permission.query.get(per_id)
        pos_list = per_obj.positions
        # 获取职位id
        pos_id_list = []
        for pos_obj in pos_list:
            pos_id_list.append(pos_obj.id)

        # 1.查询所有的职位
        pos_obj_list = Position.query.all()
        return render_template('position_permission.html', pos_obj_list=pos_obj_list, per_id=per_id,
                               pos_id_list=pos_id_list,permission_obj=permission_obj)

    else:
        # post 请求
        # 2.获取权限id
        per_id = request.form.get('per_id')
        # 1.获取选中的checkbox的值
        # 注意使用 getlist()方法获取提交的内容
        position_ids = request.form.getlist('position_ids')
        print(position_ids)  # ['1', '4', '5']
        pos_list = []
        for position_id in position_ids:
            pos_obj = Position.query.get(position_id)
            pos_list.append(pos_obj)

        # 3.设置权限和职位的关系
        per_obj = Permission.query.get(per_id)
        per_obj.positions = pos_list
        per_obj.save()
        return redirect('/permission/')

# 全局装饰器
@app.add_template_global
def aa():
    result = {
        'news': False,
        'renshi': False
    }
    # 思路通过 用户---职位--权限，根据权限名称进行设置
    person_id = request.cookies.get('person_id')
    person_obj = Person.query.get(person_id)
    pos_obj = person_obj.positions  # 职位对象
    permission_obj_list = pos_obj.permission  # 权限对象。

    for permission_obj in permission_obj_list:
        if permission_obj.name == '新闻管理':
            result['news'] = True

        if permission_obj.name == '人事管理':
            result['renshi'] = True

        if permission_obj.name == '考勤管理':
            result['kaoqin'] = True

    return result

from flask import jsonify

# 返回首页echarts数据
@app.route('/indexajax/')
def indexajax():
    # 1.查询部门以及对应的人数[{},{}]
    # 思路: 通过部门-->> 职位--->> 员工
    dept_obj_list = Department.query.all()

    dept_info_list = []

    for dept_obj in dept_obj_list:
        dic = {}
        dic['dept_name'] = dept_obj.name
        # print(dept_obj.name)
        # 获取部门对应的所有的职位
        positions_list = dept_obj.positions
        # 获取每个职位对应的员工
        # 计算职员总数
        # 研发部
        # 开发工程师   7
        # 高级开发工程师 1
        total_person_num = 0
        for position_obj in positions_list:
            person_obj_list = position_obj.person
            num = len(person_obj_list)
            total_person_num += num

        dic['num'] = total_person_num

        # 将字典追加到列表中
        dept_info_list.append(dic)

    return jsonify(dept_info_list)





