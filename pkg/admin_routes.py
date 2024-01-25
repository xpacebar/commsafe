from datetime import datetime
# import requests,json
import os,random,string
from functools import wraps
from flask import Flask,render_template,url_for,request,redirect,session,flash
from werkzeug.security import generate_password_hash, check_password_hash
from pkg import app
from pkg.forms import Login,SignUp,Contact
from pkg.models import db,User,QuickContact,State,Lga,UserType,Report,ReportCategory


@app.route('/admin/login/')
def admin_login():
    return render_template('admin/admin_login.html')

@app.route('/admin/dashboard/')
def dashboard():
    all_registered_users = db.session.query(User).count()
    all_reports = db.session.query(Report).count()
    anonymous = db.session.query(Report).filter(Report.report_hide_user == "on").count()
    blocked_users = db.session.query(User).filter(User.user_status == '1').count()
    restricted_reports = db.session.query(Report).filter(Report.report_status == '1').count()
    return render_template('admin/admin_dashboard.html', all_registered_users=all_registered_users, all_reports=all_reports, anonymous=anonymous,blocked_users=blocked_users,restricted_reports=restricted_reports)

@app.route('/admin/registered-users/')
def registered_users():
    all_registered_users = db.session.query(User).all()
    return render_template('admin/registered_users.html',all_registered_users=all_registered_users)


@app.route('/admin/blocked-users/')
def blocked_users():
    blocked_users = db.session.query(User).filter(User.user_status == '1').all()
    return render_template('admin/blocked_users.html',blocked_users=blocked_users)


@app.route('/admin/restricted-reports/')
def restricted_reports():
    restricted_reports = db.session.query(Report).filter(Report.report_status == '1').all()
    return render_template('admin/restricted_reports.html',restricted_reports=restricted_reports)

@app.route('/admin/block-user-reversal/<id>')
def block_user_reversa(id):
    user = User.query.get(id)
    user.user_status = "0"
    db.session.commit()
    return redirect(url_for('blocked_users'))


@app.route('/admin/all-reports/')
def all_reports():
    all_reports = db.session.query(Report).order_by(Report.report_date.desc()).all()
    return render_template('admin/all_reports.html',all_reports=all_reports)

@app.route('/admin/anonymous-reports/')
def anonymous_reports():
    anonymous_reports = db.session.query(Report).filter(Report.report_hide_user == "on").order_by(Report.report_date.desc()).all()
    return render_template('admin/anonymous_reports.html',anonymous_reports=anonymous_reports)


@app.route('/admin/admin-users/')
def admin_users():
    return render_template('admin/admin_users.html')


@app.route('/admin/block-user/<id>')
def block_user(id):
    user = User.query.get(id)
    user.user_status = "1"
    db.session.commit()
    return redirect(url_for('registered_users'))

@app.route('/admin/unblock-user/<id>')
def unblock_user(id):
    user = User.query.get(id)
    user.user_status = "0"
    db.session.commit()
    return redirect(url_for('registered_users'))

@app.route('/admin/restrict-report/<id>')
def restrict_report(id):
    report = Report.query.get(id)
    report.report_status = "1"
    db.session.commit()
    return redirect(url_for('all_reports'))

@app.route('/admin/unrestrict-report/<id>')
def unrestrict_report(id):
    report = Report.query.get(id)
    report.report_status = "0"
    db.session.commit()
    return redirect(url_for('all_reports'))


@app.route('/admin/undo-restrict-report/<id>')
def undo_restrict_report(id):
    report = Report.query.get(id)
    report.report_status = "0"
    db.session.commit()
    return redirect(url_for('restricted_reports'))


