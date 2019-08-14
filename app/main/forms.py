#-*-coding:utf-8-*-
from flask_wtf import Form#定义表单单的父类
import wtforms#wtfforms  #定义字段
from wtforms import  validators#validators验证器validators验证器validators验证器validators
from    ..models import Course,Students#..上一级目录
#course_list = [(str(c.id), str(c.label)) for c in Course.query.all()]#这里必须是字符串类型
#course_list=[(1,"python"),(2,"php"),(3,"java")]
class TeacherForm(Form):#该类在views.py中被调用
    username = wtforms.StringField("教师用户名",
                               render_kw={
                                   "class": "form-control",
                                   "placeholder": "教师用户名"
                               },
                               validators={
                                   validators.DataRequired("用户名不可以为空")
                               })
    password = wtforms.IntegerField("登录密码",
                                   render_kw={
                                       "class": "form-control",
                                       "placeholder": "登录密码"
                                   },
                                   validators={
                                       validators.DataRequired("登录密码不可以为空")
                                   })
    name=wtforms.StringField("教师姓名",
                              render_kw={
                                  "class":"form-control",
                                  "placeholder":"教师姓名"
                              },
                              validators={
                                  validators.DataRequired("姓名不可以为空")
                              })
    age=wtforms.IntegerField("教师年龄",
                             render_kw={#固定语法render_kw;render_kw;render_kw;render_kw
                                 "class":"form-control",#CSS样式
                                 "placeholder":"教师年龄",#占位符placeholder;placeholder;placeholder
                             },
                             validators=[#validators验证器，validators
                                 validators.DataRequired("年龄不可以为空")
                             ])#required必须的required;required;data数据data;
    gender = wtforms.SelectField("教师性别",
        choices=[('0','男'),('1','女'),('2','其他')],#这里必需是字符串类型1
        render_kw={
            "class":"form-control",
        })
    course_id=wtforms.SelectField(#选择框
        "学科",
        choices="",
        render_kw={
            "class":"form-control",
        }
    )
    """
    form 字段的参数
    label=None,表单的标签
    validators=None,校验，传入校验的方法
    filter=tuple(),过滤
    description='',描述
    id=None,html  id
    default=None,默认值
    widget=None,
    render_kw=None,
    """
class  Stu_CouForm(Form):#学生课程表单
    students_id=wtforms.SelectField("学生id",
        choices="",
        render_kw={
            "class":"form-control",#css样式
        })
    course_id=wtforms.SelectField("课程id",#Multiple多重的multiple
        choices="",#选择的内容
        render_kw={
        "class": "form-control",  # css样式
        })
class  StuCouForm(Form):#学生课程表单
    course_id=wtforms.SelectField("课程id",#Multiple多重的multiple
        choices="",#选择的内容
        render_kw={
        "class": "form-control",  # css样式
        })




