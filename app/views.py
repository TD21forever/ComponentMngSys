	# -*- coding: utf-8 -*-
# @Author: TD21forever
# @Date:   2019-07-12 21:16:52
# @Last Modified by:   TD21forever
# @Last Modified time: 2019-08-18 15:37:01
from app import app,db
from app.forms import LoginForm,RegistrationForm,AddComponentForm,ApplyComponentForm
from app.models import Student,Component,Admin,Application
from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, flash, redirect, session, url_for, request, g
import datetime

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/login/<identity>', methods = ['GET', 'POST'])
def login(identity):	
	#如果已经登陆了，就直接去index，不用重复登录

	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		if identity == 'student':
			user = Student.query.filter_by(student_num=form.id.data).first()
			
		elif identity == 'admin':
			user = Admin.query.filter_by(admin_num=form.id.data).first()
		#如果用户名不存在 或者 密码错误,就继续留在login
		if user is None or not user.check_password(form.password.data):
			flash('用户名或者密码错误')
			return redirect(url_for('login',identity=identity))
		#登录了

		login_user(user,remember = form.remember_me.data)
		#url中是视图函数的名字
		# return redirect(url_for('index'))
		#如果直接进入login页面，登陆后自动跳转到index
		next_page = request.args.get('next')
		#如果登录 URL 没有一个 next 参数
		#如果登录 URL 的 next 参数被设置成了包含域名的完整路径（安全性）
		if not next_page or url_parse(next_page).netloc != "":
			next_page = url_for('index')	
		#以下处理是：如果是先访问的index 但要求登录 登录完后跳转到next
		return redirect(next_page)		
	if identity == 'student':
		return render_template('studentLogin.html',
			title = 'Sign In',
			form = form,
			)
	elif identity == 'admin':
		return render_template('adminLogin.html',
			title = 'Sign In',
			form = form,
			)

@app.route('/logout')
def logout():
	logout_user()
	return	redirect(url_for('index'))

@app.route('/register/<identity>',methods=['GET', 'POST'])
def register(identity):
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		if identity == 'student':
			user = Student(student_num=form.id.data,email=form.email.data,username=form.username.data)
			#手动将输入密码放入数据库中
		else:
			user = Admin(admin_num=form.id.data, email=form.email.data,username=form.username.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login',identity=identity))
	return render_template('register.html', title='Register', form=form,identity=identity)

@app.route('/component',methods=['GET','POST'])
@login_required
def component():
	if isinstance(current_user._get_current_object(),Admin):
		items = Component.query.all()
		add_form = AddComponentForm()
		if add_form.validate_on_submit():
			quantity = add_form.quantity.data
			unitPrice = add_form.unitPrice.data
			totalPrice = round(quantity*unitPrice,2)
			if Component.query.filter_by(name=add_form.name.data,type=add_form.type.data).first() is not None:
				flash("已存在这个元器件")
				return redirect(url_for('component'))
			component = Component(
				name=add_form.name.data,
				type=add_form.type.data,
				quantity = quantity,
				unitPrice = unitPrice,
				totalPrice = totalPrice,
				remark = add_form.remark.data	
				)
			db.session.add(component)
			db.session.commit()
			flash("元器件添加成功")
			return redirect(url_for('component'))
		return render_template('admin/component.html',items = items,form = add_form)
	elif isinstance(current_user._get_current_object(),Student):
		items = Component.query.all()
		apply_form = ApplyComponentForm()
		return render_template('student/component.html',items = items,form = apply_form)
'''
@app.route('/add',methods=['GET', 'POST'])
def add():
	add_form = AddComponentForm()
	if add_form.validate_on_submit():
		quantity = add_form.quantity.data
		unitPrice = add_form.unitPrice.data
		totalPrice = round(quantity*unitPrice,2)
		component = Component(
			name=add_form.name.data,
			type=add_form.type.data,
			quantity = quantity,
			unitPrice = unitPrice,
			totalPrice = totalPrice,
			remark = add_form.remark.data	
			)
		db.session.add(component)
		db.session.commit()
		flash("元器件添加成功")
	return render_template('component.html',form=add_form)
'''
@app.route('/delete/<component_id>',methods=['GET', 'POST'])
def delete(component_id):
	component = Component.query.filter_by(id = component_id).first()
	db.session.delete(component)
	db.session.commit()
	flash("删除成功")
	return redirect(url_for('component'))

#这里有点难度
@app.route('/application/<student_num>/<component_id>',methods=['GET', 'POST'])
@login_required
def application(student_num,component_id):
	if request.method == 'POST':
		quantity = request.form['quantity']
		#申请的元器件
		component = Component.query.filter_by(id = component_id).first()
		#申请的数量
		if quantity == "":
			flash("申请数量不能为空")
		else:
			quantity = int(quantity)
			if quantity <= 0:
				flash("申请数量有误")
				return redirect(url_for("component"))
			if quantity > component.quantity:
				flash("库存不足")
				return redirect(url_for("component"))
		#申请的时间
		time = datetime.datetime.now().date()
		application = Application(
			student_id=student_num,
			component_id=component_id,
			quantity=quantity,
			time = time
			)	
		db.session.add(application)
		db.session.commit()

		component.quantity -= quantity
		db.session.add(component)
		db.session.commit()

		flash("申请中,请注意查看是否申请成功")
		return redirect(url_for('component'))

@app.route('/unapplication/<application_id>',methods=['GET', 'POST'])
@login_required
def unapplication(application_id):
	application = Application.query.filter_by(id=application_id).first()
	application.status = "未申请"
	component_id = application.component_id
	component = Component.query.filter_by(id = component_id).first()
	quantity = application.quantity
	component.quantity += quantity
	db.session.add(application)
	db.session.add(component)
	db.session.delete(application)
	db.session.commit()
	flash("已经取消申请")
	return redirect(url_for('info'))


#这边的处理比较难
@app.route('/info',methods=['GET','POST'])
@login_required
def info():
	'''
	三个表连接,将data转换成为字典
	列表中的项并不是标准的 Python tuple，<class 'sqlalchemy.util._collections.result'>，它是一个 AbstractKeyedTuple 对象，拥有一个 keys() 方法，这样可以很容易将其转换成 dict ：
	[{'Application': <Application 17061833, 1>, 'Student': <Student dct>, 'Component': <Component 1>}, {'Application': <Application 17061833, 2>, 'Student': <Student dct>, 'Component': <Component 2>}, {'Application': <Application 17061833, 3>, 'Student': <Student dct>, 'Component': <Component 3>}]

	'''
	#items是一个字典
	if isinstance(current_user._get_current_object(),Admin):
		data = db.session.query(Application,Student,Component).join(Student).join(Component).all()
		items = [dict(zip(result.keys(), result)) for result in data]
		return render_template('admin/info.html',items=items)
	elif isinstance(current_user._get_current_object(),Student):
		data = db.session.query(Application,Student,Component).join(Student).join(Component).filter(Application.student_id == current_user.student_num).all()	
		items = [dict(zip(result.keys(), result)) for result in data]	
		return render_template('student/info.html',items=items)


@app.route('/agree/<application_id>',methods=['GET','POST'])
@login_required
def agree(application_id):
	application = Application.query.filter_by(id=application_id).first()
	application.status = "申请成功"
	db.session.add(application)
	db.session.commit()
	flash("已同意")
	return redirect(url_for("info"))

'''
如果修改了表结构 这里可能会有点问题
'''
@app.route('/disagree/<application_id>',methods=['GET','POST'])
@login_required
def disagree(application_id):
	if request.method == 'POST':
		remark = request.form['remark']
		application = Application.query.filter_by(id=application_id).first()
		component_id = application.component_id
		component = Component.query.filter_by(id = component_id).first()
		component.quantity += application.quantity
		application.status = "申请失败"
		application.remark = remark
		db.session.add(application)
		db.session.commit()
		flash("已拒绝")
		return redirect(url_for("info"))


@app.route('/modify/<component_id>',methods=['GET','POST'])
@login_required
def modify(component_id):
	# application = Application.query.filter_by(id=component_id)
	component = Component.query.filter_by(id=component_id).first()
	if request.method == 'POST' or request.method == 'GET':
		remark = request.form['remark']
		quantity = request.form['quantity']
		unitPrice = request.form['unitPrice']
		if remark != component.remark:
			component.remark = remark
		if quantity != component.quantity:
			component.quantity = quantity
		if unitPrice != component.unitPrice:
			component.unitPrice = unitPrice
		db.session.add(component)
		db.session.commit()
		flash("修改成功!")
		return redirect(url_for('component'))

	return redirect(url_for('component'))

