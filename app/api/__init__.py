#-*-coding:utf-8-*-
from  flask import Blueprint
from flask_restful import Api#第三方Api包
#api_main=Blueprint("api",__name__,url_prefix="/api/")
api_main=Blueprint("api",__name__)

api=Api(api_main)

from . import  ApiResource
