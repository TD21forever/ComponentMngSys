# -*- coding: utf-8 -*-
# @Author: TD21forever
# @Date:   2019-07-12 22:42:09
# @Last Modified by:   TD21forever
# @Last Modified time: 2019-07-18 21:53:33
from app import db,app
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
from flask_login import UserMixin
from hashlib import md5
from app import login_manager


'''
连接表
'''
class Application(db.Model):
	'''
SQLAlchemy会假设你的表名就模型类型的小写版本。但是，如果你想给表起个别的名字，你可以给类添加'__tablename__'的类属性。另外，通过采用这种方式，你也可以使用在数据库中已经存在的表，只需把表名设为该属性的值：
	'''
	__tablename__ = 'application'
	#将id设置为主键是为了解决 同一个人对同一个元器件申请多次的问题
	id = db.Column(db.Integer,primary_key=True)
	student_id = db.Column(db.String(8),db.ForeignKey('students.student_num'),nullable=False)
	component_id = db.Column(db.Integer,db.ForeignKey('components.id'),nullable=False)
	quantity = db.Column(db.Integer,nullable=False)
	time = db.Column(db.Date,nullable=False)
	status = db.Column(db.String(64),nullable=False,default="申请中")
	remark = db.Column(db.String(128),nullable=True,default="无")

'''
学生类
'''
class Student(UserMixin,db.Model):
	"""docstring for User"""
	__tablename__='students'
	student_num = db.Column(db.String(64),primary_key=True)
	username = db.Column(db.String(64),index=True,unique=True,nullable=False)
	email = db.Column(db.String(120),index=True,unique=True,nullable=False)
	password_hash = db.Column(db.String(128))
	components = db.relationship("Component",secondary="application",backref=db.backref('students',lazy='dynamic'),lazy='dynamic')

	def __repr__(self):
		return '<Student {}>'.format(self.username)

	def set_password(self,password):
		self.password_hash = generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.password_hash,password)
	#没有id就要重载get_id
	#override
	def get_id(self):
		return self.student_num

'''
管理员
'''
class Admin(UserMixin,db.Model):
	"""docstring for Admin"""
	__tablename__='admin'
	admin_num = db.Column(db.String(64),primary_key=True)
	username = db.Column(db.String(64),index=True,unique=True,nullable=False)
	email = db.Column(db.String(120),index=True,unique=True,nullable=False)
	password_hash = db.Column(db.String(128))

	def __repr__(self):
		return '<Admin {}>'.format(self.username)

	def set_password(self,password):
		self.password_hash = generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.password_hash,password)
	#override
	def get_id(self):
		return self.admin_num
'''
元器件类
添加元器件可能会有问题 是否能重复添加等问题.
'''
class Component(db.Model):
	__tablename__='components'
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64))#不可以为空
	type = db.Column(db.String(64))
	quantity = db.Column(db.Integer)
	unitPrice = db.Column(db.Float)
	totalPrice = db.Column(db.Float)
	remark = db.Column(db.String(128),nullable=True)


#这个函数的功能还不是很能理解
@login_manager.user_loader
def load_user(num):
	#学生学号长度为
	if len(num) == 8:
		return Student.query.get(int(num))
	#管理员工号长度为4
	elif len(num) == 4:
		return Admin.query.get(int(num))


