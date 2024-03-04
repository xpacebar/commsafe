from datetime import datetime
# import requests,json
import os,random,string
from functools import wraps
from flask import Flask,render_template,url_for,request,redirect,session,flash
from werkzeug.security import generate_password_hash, check_password_hash
from pkg import app
from pkg.forms import Login,SignUp,Contact
from pkg.models import db,User,QuickContact,State,Lga,UserType,Report,ReportCategory,Admin,FeaturedServices,Feedback


# login requried decorator
def login_required(f):
    @wraps(f) #This ensure that the details about the original function f, that is being decorated is still available
    def check_login(*args, **kwargs):
        """Checks if session id is set or not"""
        if session.get('useronline') != None:
            return f(*args, **kwargs)
        else:
            flash("You must be logged in to access this page",category='error')
            return redirect(url_for('admin_login'))
    return check_login

@app.route('/admin/login/', methods=['GET','POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('admin/admin_login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('pwd')
        if email == "" or password == "":
            flash('Provide a valid credential to proceed!', category='error')
            return render_template('admin/admin_login.html')
        else:
            admin_record = db.session.query(Admin).filter(Admin.admin_email == email).first()
            if admin_record:
                hashed_pwd = admin_record.admin_pwd
                rsp = check_password_hash(hashed_pwd,password)
                if rsp:
                    id = admin_record.admin_id
                    session['useronline'] = id
                    flash(f'Welcome Back!', category='info')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid Login Credentials!', category='error')
                    return redirect('/admin/login/')
            else:
                flash('Invalid Login Credentials!', category='error')
                return redirect('/admin/login/')
                



    

@app.route('/admin/dashboard/')
@login_required
def dashboard():
    id = session.get('useronline')
    deets = Admin.query.get(id)
    all_registered_users = db.session.query(User).count()
    all_admin_users = db.session.query(Admin).count()
    all_reports = db.session.query(Report).count()
    anonymous = db.session.query(Report).filter(Report.report_hide_user == "on").count()
    blocked_users = db.session.query(User).filter(User.user_status == '1').count()
    restricted_reports = db.session.query(Report).filter(Report.report_status == '1').count()
    return render_template('admin/admin_dashboard.html', all_registered_users=all_registered_users, all_reports=all_reports, anonymous=anonymous,blocked_users=blocked_users,restricted_reports=restricted_reports,deets=deets,all_admin_users=all_admin_users)

@app.route('/admin/registered-users/')
@login_required
def registered_users():
    id = session.get('useronline')
    deets = Admin.query.get(id)
    all_registered_users = db.session.query(User).all()
    return render_template('admin/registered_users.html',all_registered_users=all_registered_users,deets=deets)


@app.route('/admin/blocked-users/')
@login_required
def blocked_users():
    id = session.get('useronline')
    deets = Admin.query.get(id)
    blocked_users = db.session.query(User).filter(User.user_status == '1').all()
    return render_template('admin/blocked_users.html',blocked_users=blocked_users,deets=deets)


@app.route('/admin/restricted-reports/')
@login_required
def restricted_reports():
    id = session.get('useronline')
    deets = Admin.query.get(id)
    restricted_reports = db.session.query(Report).filter(Report.report_status == '1').all()
    return render_template('admin/restricted_reports.html',restricted_reports=restricted_reports,deets=deets)

@app.route('/admin/block-user-reversal/<id>')
@login_required
def block_user_reversa(id):
    user = User.query.get(id)
    user.user_status = "0"
    db.session.commit()
    return redirect(url_for('blocked_users'))


@app.route('/admin/all-reports/')
@login_required
def all_reports():
    id = session.get('useronline')
    deets = Admin.query.get(id)
    all_reports = db.session.query(Report).order_by(Report.report_date.desc()).all()
    return render_template('admin/all_reports.html',all_reports=all_reports,deets=deets)

@app.route('/admin/anonymous-reports/')
@login_required
def anonymous_reports():
    id = session.get('useronline')
    deets = Admin.query.get(id)
    anonymous_reports = db.session.query(Report).filter(Report.report_hide_user == "on").order_by(Report.report_date.desc()).all()
    return render_template('admin/anonymous_reports.html',anonymous_reports=anonymous_reports,deets=deets)


@app.route('/admin/admin-users/')
@login_required
def admin_users():
    id = session.get('useronline')
    deets = Admin.query.get(id)
    admin_users = Admin.query.all()
    return render_template('admin/admin_users.html',deets=deets,admin_users=admin_users)


@app.route('/admin/block-user/<id>')
@login_required
def block_user(id):
    user = User.query.get(id)
    user.user_status = "1"
    db.session.commit()
    return redirect(url_for('registered_users'))

@app.route('/admin/unblock-user/<id>')
@login_required
def unblock_user(id):
    user = User.query.get(id)
    user.user_status = "0"
    db.session.commit()
    return redirect(url_for('registered_users'))

@app.route('/admin/restrict-report/<id>')
@login_required
def restrict_report(id):
    report = Report.query.get(id)
    report.report_status = "1"
    db.session.commit()
    return redirect(url_for('all_reports'))

@app.route('/admin/unrestrict-report/<id>')
@login_required
def unrestrict_report(id):
    report = Report.query.get(id)
    report.report_status = "0"
    db.session.commit()
    return redirect(url_for('all_reports'))


@app.route('/admin/undo-restrict-report/<id>')
@login_required
def undo_restrict_report(id):
    report = Report.query.get(id)
    report.report_status = "0"
    db.session.commit()
    return redirect(url_for('restricted_reports'))


@app.route('/admin/edit-profile/', methods=['GET','POST'])
@login_required
def admin_edit_profile():
    id = session.get('useronline')
    if request.method == 'GET':
        deets = Admin.query.get(id)
        return render_template('admin/admin_edit_profile.html',deets=deets)
    else:
        admin = Admin.query.get(id)
        admin.admin_fname = request.form.get('first_name')
        admin.admin_lname = request.form.get('last_name')
        admin.admin_gender = request.form.get('gender')
        admin.admin_type = request.form.get('admin_type')
        db.session.commit()
        flash('Profile Updated Successfully!', category='info')
        return redirect(url_for('dashboard'))
    
@app.route('/admin/change-password/', methods=['GET','POST'])
@login_required
def admin_change_password():
    id = session.get('useronline')
    if request.method == 'GET':
        deets = Admin.query.get(id)
        return render_template('admin/admin_change_password.html',deets=deets)
    else:
        old_pwd = request.form.get('old_pwd')
        new_pwd = request.form.get('new_pwd')
        new_pwd1 = request.form.get('new_pwd1')
        if old_pwd == "" or new_pwd == "" or new_pwd1 == "":
            flash('Enter all fields to change your password', category='error')
            return redirect(url_for('admin_change_password'))
        else:
            admin = Admin.query.get(id)
            hashed_pwd = admin.admin_pwd
            pwd = check_password_hash(hashed_pwd,old_pwd)
            if pwd:
                if new_pwd != new_pwd1:
                    flash('Confirm new password match', category='error')
                    return redirect(url_for('admin_change_password'))
                elif new_pwd == old_pwd:
                    flash('Cannot change to a currently used password ', category='error')
                    return redirect(url_for('admin_change_password'))
                else:
                    new_password = generate_password_hash(new_pwd)
                    admin.admin_pwd = new_password
                    db.session.commit()
                    flash('Password Changed Successfully!', category='info')
                    return redirect(url_for('dashboard'))
            else:
                flash('Old Password incorrect', category='error')
                return redirect(url_for('admin_change_password'))


@app.route('/admin/add-admin/', methods=['GET','POST'])
@login_required
def admin_add_admin():
    id = session.get('useronline')
    if request.method == 'GET':
        deets = Admin.query.get(id)
        return render_template('admin/admin_add_admin.html',deets=deets)
    else:
        email = request.form.get('email')
        pwd = request.form.get('pwd')
        admintype = request.form.get('admin_type')
        if email == "" or pwd == "" or admintype == "":
            flash('Enter all fields to add new admin user', category='error')
            return redirect(url_for('admin_add_admin'))
        else:
            records = Admin.query.filter(Admin.admin_email == email).first()
            if records:
                flash('Admin User already exist', category='error')
                return redirect(url_for('admin_add_admin'))
            else:
                hashed_pwd = generate_password_hash(pwd)
                admin = Admin(admin_email = email,
                          admin_pwd = hashed_pwd,
                          admin_type = admintype)
                db.session.add(admin)
                db.session.commit()
                flash(f'Admin User {email} Added Successfully!', category='info')
                return redirect(url_for('admin_add_admin'))
            
@app.route('/admin/remove-admin/', methods=['GET','POST'])
@login_required
def admin_remove_admin():
    id = session.get('useronline')
    admin_users = db.session.query(Admin).all()
    if request.method == 'GET':
        deets = Admin.query.get(id)
        return render_template('admin/admin_remove_admin.html',deets=deets,admin_users=admin_users)
    else:
        adminUser = request.form.get('email')
        if adminUser == "":
            flash('Select an admin user', category='error')
            return redirect(url_for('admin_remove_admin'))
        else:
            admin = Admin.query.get(adminUser)
            db.session.delete(admin)
            db.session.commit()
            flash(f'Admin User {admin.admin_email} Successfully Removed', category='info')
            return redirect(url_for('admin_remove_admin'))
        
@app.route('/admin/all-featured-services/')
@login_required
def admin_all_featured_services():
    id = session.get('useronline')
    deets = Admin.query.get(id)
    featured_services = FeaturedServices.query.all()
    return render_template('admin/admin_all_featured_services.html', deets=deets,featured_services=featured_services)

@app.route('/admin/delete-featured-service/<fservice_id>')
@login_required
def admin_delete_featured_service(fservice_id):
    fservice = FeaturedServices.query.get(fservice_id)
    db.session.delete(fservice)
    db.session.commit()
    return redirect(url_for('admin_all_featured_services'))

        
@app.route('/admin/add-featured-services/', methods=['GET','POST'])
@login_required
def admin_add_featured_services():
    id = session.get('useronline')
    # featured_services = db.session.query(FeaturedServices).all()
    if request.method == 'GET':
        deets = Admin.query.get(id)
        return render_template('admin/admin_add_featured_services.html',deets=deets)
    else:
        service_name = request.form.get('name')
        service_desc = request.form.get('desc')
        service_addy = request.form.get('address')
        service_phone = request.form.get('phone')
        service_email = request.form.get('email')
        service_img = request.files.get('fspic')
        if service_name == "" or service_desc == "" or service_addy == "" or service_phone == "" or service_email == "" or service_img == "":
            flash('All Fields Required', category='error')
            return redirect(url_for('admin_add_featured_services'))
        else:
            pic_name = service_img.filename
            name,ext = os.path.splitext(pic_name)
            allowed=['.jpg','.png','.jpeg']
            if ext.lower() in allowed:
                final_name = random.random() * 1000000000
                final_name = str(final_name) + ext
                try:
                    service_img.save(f'pkg/static/featured_images/{final_name}')
                except:
                    os.remove(f'pkg/static/featured_images/{final_name}')
                else:
                    f_service = FeaturedServices(
                        featured_admin_id = id,
                        featured_name = service_name,
                        featured_desc = service_desc,
                        featured_address = service_addy,
                        featured_phone = service_phone,
                        featured_email = service_email,
                        featured_img_file = final_name
                        )
                    db.session.add(f_service)
                    db.session.commit()
                    flash('Featured Service Uploaded', category='info')
                    return redirect(url_for('admin_add_featured_services'))
            else:
                flash('upload either a .jpeg, .jpg or a .png file',category=('error'))
                return redirect(url_for('admin_add_featured_services'))
            

@app.route('/admin/users-feedback/', methods=['GET','POST'])
@login_required
def admin_users_feedback():
    id = session.get('useronline')
    deets = Admin.query.get(id)
    feedbacks = Feedback.query.all()
    return render_template('admin/admin_users_feedback.html',deets=deets,feedbacks=feedbacks)


@app.route('/admin/logout/')
@login_required
def admin_logout():
    session.pop('useronline', None)
    return redirect(url_for('admin_login'))

