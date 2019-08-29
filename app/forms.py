# -*- coding: utf-8 -*-
# @Author: TD21forever
# @Date:   2019-07-12 22:59:10
# @Last Modified by:   TD21forever
# @Last Modified time: 2019-08-18 16:10:43
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField,IntegerField,widgets
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo,Length
from app.models import Student,Component,Admin
class LoginForm(FlaskForm):
	id = StringField(label="学号",validators=[DataRequired(message='学号不能为空'),Length(4, 8, "请输入正确格式的学号")],widget=widgets.TextInput(), render_kw={
			'class': 'form-control',
			'placeholder': '请输入学号',
			'required': '',
			'autofocus': ''
		})
	password = PasswordField(label='密码',validators=[DataRequired(message='密码不能为空')],widget=widgets.PasswordInput(),render_kw={
			'class': 'form-control',
			'placeholder': '请输入密码',
			'required': '',
			'autofocus': ''
		})
	remember_me = BooleanField(label='记住密码')
	submit = SubmitField(label='登录')

class RegistrationForm(FlaskForm):
	id = StringField("学号",
		validators=[DataRequired(message='学号不能为空'),Length(4, 8, "请输入正确格式的学号")],
		widget=widgets.TextInput(),
		render_kw={
			 'class': 'form-control',
			'placeholder': '请输入学号',
			'required': '',
			'autofocus': ''
		}
		)
	username = StringField('名字',
		validators=[DataRequired(message='名字不能为空')],
		widget=widgets.TextInput(),
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入姓名',
			'required': '',
			'autofocus': ''
		})
	email = StringField('邮箱',
		validators=[DataRequired(message='邮箱不能为空'),Email()],
		widget=widgets.TextInput(),
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入邮箱',
			'required': '',
			'autofocus': ''
		}
		)
	password = PasswordField('密码',validators=[DataRequired(message='密码不能为空')],
		widget=widgets.PasswordInput(),
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入密码',
			'required': '',
			'autofocus': ''
		}
		)
	password2 = PasswordField('重复密码',validators=[DataRequired(message='密码不能为空'),EqualTo('password')],widget=widgets.PasswordInput(),
		render_kw={
			'class': 'form-control',
			'placeholder': '请输入密码',
			'required': '',
			'autofocus': ''
		})
	submit = SubmitField("注册")
	#当你以 validate_<filed_name> 的模式添加方法的时候，WTForms会将它们作为自定义验证器
	def validate_id(self, id):
		student = Student.query.filter_by(student_num=id.data).first()
		if student is not None:
			raise ValidationError('该学生已注册')
		# admin = Admin.query.filter_by(admin_num=id.data).first()
		# if admin is not None:
		# 	raise ValidationError('该管理已注册过')

	def validate_email(self, email):
		user = Student.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('邮箱已被注册')

class AddComponentForm(FlaskForm):
	name = StringField('名称',
		validators=[DataRequired()],
		widget=widgets.TextInput(),
		render_kw={
			'class': 'form-control',
			'placeholder': '名称',
			'required': '',
			'autofocus': ''
		})
	type = StringField('型号',
		validators=[DataRequired()],
		widget=widgets.TextInput(),
		render_kw={
			'class': 'form-control',
			'placeholder': '型号',
			'required': '',
			'autofocus': ''
		})
	quantity = IntegerField('数量',
		validators=[DataRequired()],
		widget=widgets.TextInput(),
		render_kw={
			'class': 'form-control',
			'placeholder': '数量',
			'required': '',
			'autofocus': ''
		})
	unitPrice = IntegerField('单价',
	validators=[DataRequired()],
	widget=widgets.TextInput(),
	render_kw={
		'class': 'form-control',
		'placeholder': '单价',
		'required': '',
		'autofocus': ''
	})

	remark = StringField('备注',
	validators=[DataRequired()],
	widget=widgets.TextInput(),
	render_kw={
		'class': 'form-control',
		'placeholder': '备注',
		'required': '',
		'autofocus': ''
	})
	submit = SubmitField("添加")


class ApplyComponentForm(FlaskForm):
	quantity = IntegerField('申请数量',
	validators=[DataRequired()],
	widget=widgets.TextInput(),
	render_kw={
		'class': 'form-control',
		'placeholder': '申请数量',
		'required': '',
		'autofocus': ''
	})
	submit = SubmitField("申请")
	def get_data():
		return quantity.data
