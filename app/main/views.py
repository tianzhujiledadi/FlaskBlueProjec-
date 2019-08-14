#-*-coding:utf-8-*-
from flask import render_template, redirect,session,make_response  # redirect重定向
from . import main #.代表当前目录
from app.models import *
from flask import request, jsonify
import hashlib
from .forms import TeacherForm,Stu_CouForm
from app import csrf
# @app.route('/student/',methods=["GET","POST"])#前后台必须加斜杠
@main.route('/loginvalid/')
def loginValid(fun):
    def inner(*args, **kwargs):
        username = request.cookies.get("user_name")
        session_name = session.get("username")
        if username and session_name and session_name == spw(username):
            user = User.query.filter_by(username=username).first()
            if user:
                return fun(*args, **kwargs)
        return redirect("/login/")
    return inner
#@csrf.exempt#exempt免除、豁免exempt,exempt #免除单个视图的csrf校验
@main.route('/register/', methods=["GET", "POST"])
def register(): # 已经导入request包不用再在参数里添加
    if request.method == "POST":
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")
        identity = form_data.get("identity")
        user = User()
        user.username = username
        user.password = spw(password)
        user.identity = identity
        user.save()
        return redirect('/login/')
    return render_template('register.html', **locals())
#from  app import  cache
@csrf.exempt#exempt免除、豁免exempt,exempt #免除单个视图的csrf校验
@main.route('/login/', methods=["GET", "POST"])
#@cache.cached(timeout=60)#尽量使用页面缓存，不要使用视图缓存#重定向不宜用缓存
def login():
    if request.method == "POST":
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")
        user = User.query.filter_by(username=username).first()
        identity=user.identity
        identity_id=user.identity_id
        if  user and spw(password) == user.password:
            response = redirect('/index/')
            response.set_cookie("user_name", str(username))
            response.set_cookie("user_id",str(user.id))
            response.set_cookie("identity",str(identity))
            session["username"] = spw(username)
            if identity_id:
                response.set_cookie("identity_id",str(identity_id))
            else:
                response.set_cookie("identity_id","")
            return response
    return render_template('login.html', **locals())
def spw(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()  # 返回加密的密码
@main.route('/index/', methods=["GET", "POST"])
@loginValid
#@cache.cached(timeout=60)
def index():#identity用户身份
    identity=request.cookies.get("identity")#肯定存在
    id= request.cookies.get("identity_id")
    teacherForm = TeacherForm()
    teacherForm.course_id.choices = [(str(c.id), str(c.label)) for c in Course.query.all()]
    if request.method == "GET":
        if id:#已经写好信息
            if  identity=="0":
                teacher=Teachers.query.filter_by(id=id).first()
            elif identity=="1" :
                student=Students.query.get(id)
                courses=Course.query.all()
                courses_student = student.to_course.all()
                grades=Grade.query.filter_by(student_id=id)
                lenth=0
                for i in grades:
                    lenth+=1
            else:
                users = User.query.filter_by(id=id).first()
        else:
            teacher={}
            student={}
            users={}
            courses = Course.query.all()
    if request.method == "POST":
        name=request.form.get("name")
        age = int(request.form.get("age"))
        gender=int(request.form.get("gender"))
        if identity=="0":
            course = request.form.get("course_id")
            teacher = Teachers()
            teacher.name=name
            teacher.age=age
            teacher.gender=gender
            teacher.course_id=course
            teacher.save()
            id =teacher.id
        elif identity == "1":
            course = request.form.getlist("course_id")
            courses=Course.query.all()
            student=Students()
            student.name = name
            student.age = age
            student.gender = gender
            student.save()
            id=student.id
            print(course,id)
            for courseId in course:
                course=Course.query.get(int(courseId))
                student.to_course.append(course)
                student.save()#将学生和课程关系对应
                grade=Grade()#将学生和课程存入成绩表
                grade.course_id=int(courseId)
                grade.student_id=id
                grade.save()
        else:
            id=request.cookies.get("user_id")
            pass
        user=User.query.filter_by(id=int(request.cookies.get("user_id"))).first()
        print(int(request.cookies.get("user_id")),id)
        user.identity_id=id
        user.save()
        response=make_response(redirect("/index/"))#make_response#返回页面，下面接着运行
        response.set_cookie("identity_id",str(user.identity_id))
        return  response
    return render_template('index.html', **locals())
@main.route('/logout/', methods=["GET", "POST"])
def logout():
    response = redirect("/login/")
    for key in request.cookies:
        response.delete_cookie(key)
        print(key)
    del session["username"]
    return response
@main.route("/userValid/",methods=["GET","POST"])
def UserValid():
    result = {"code": "","data": ""}
    if request.method=="POST":
        data = request.args.get("username")#get获取参数方法
        data=request.form.get("username")#post获取参数方法
        if data:
            user = User.query.filter_by(username=data).first()
            if user:
                result["code"] = 400
                result["data"] = "用户名已经存在"
            else:
                result["code"] = 200
                result["data"] = "用户名未被注册，可以使用"
    else:
        result["code"] = 400
        result["data"] = "请求方法错误"
    return jsonify(result)
@main.route("/stu_cou/<int:id>", methods=["GET", "POST"])
def stu_cou(id):
    stucouForm= Stu_CouForm()
    stucouForm.course_id.choices = [(str(c.id), str(c.label)) for c in Course.query.all()]  # 这里必须是字符串类型
    #stu_couForm.students_id.choices=[(str(s.id), str(s.name)) for s in Students.query.all()]#这里必须是字符串类型
    print(2,stucouForm.course_id.choices)
    if request.method == "POST":
        course_id= request.form.get("course_id")
        stu=Students.query.filter_by(id=int(id)).first()
        stu.save()
        cou=Course.query.filter_by(id in course_id).all()
        cou.save()
        stu.to_course.append(cou)#添加一个元素
        #stu.to_course=[cou]#按照学生id设置一门课程或者修改课程不能修改课程，
        stu.save()
        #stu_cou=Stu_Cou.query.filter_by(students_id=students_id).first()
    return render_template("stu_cou_add.html", **locals())

@main.route('/student_list/<int:id>',methods=["GET","POST"])
def student_list(id):
    print("函数调用成功")
    student_list = Students.query.filter_by(id=id)
    return render_template("student.html", **locals())
# @main.route("/clearCache/")
# def clearCache():
#     cache.clear()
#     return "cache  is clear,缓存已经清空"

@csrf.exempt
@main.route("/add_teacher/", methods=["GET", "POST"])
def add_teacher():
    teacherForm = TeacherForm()
    teacherForm.course_id.choices=[(str(c.id), str(c.label)) for c in Course.query.all()]#这里必须是字符串类型
    print(1,teacherForm.course_id.choices)
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        course_id=request.form.get("course_id")
        print(name, age, gender)
        teacher = Teachers()  # 增加数据
        teacher.name = name
        teacher.age = int(age)
        teacher.gender = int(gender)
        teacher.course_id = int(course_id)
        # teacher.course_id =1
        teacher.save()
        teacher = Teachers.query.filter_by(name=name).first()
        print(teacher)
    return render_template("add_teacher.html", **locals())
@csrf.exempt
@main.route("/stu_cou_add/", methods=["GET", "POST"])
def stu_cou_add():
    stu_couForm= Stu_CouForm()
    stu_couForm.course_id.choices = [(str(c.id), str(c.label)) for c in Course.query.all()]  # 这里必须是字符串类型
    stu_couForm.students_id.choices=[(str(s.id), str(s.name)) for s in Students.query.all()]#这里必须是字符串类型
    print(2,stu_couForm.course_id.choices)
    if request.method == "POST":
        course_id= request.form.get("course_id")
        students_id= request.form.get("students_id")
        print(students_id,type(students_id))
        stu=Students.query.filter_by(id=int(students_id)).first()
        cou = Course.query.filter_by(id in course_id).all()
        stu.to_course.append(cou)#添加一个元素
        #stu.to_course=cou#按照学生id设置一门课程或者修改课程不能修改课程，
        stu.save()
        stu_cou=Stu_Cou.query.filter_by(students_id=students_id).first()
    return render_template("stu_cou_add.html", **locals())

@main.route("/e/",methods=["GET","POST"])
def Example():
    #print([value for key,value in request.form if key == "testCheck"])
    # for key in request.form:
    #     print(key)
    print(request.form.getlist("testCheck"))
    return render_template("example.html")