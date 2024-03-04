from datetime import datetime
import json #requests,
import os,random,string
from functools import wraps
from flask import Flask,render_template,url_for,request,redirect,session,flash,jsonify
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message,Mail
from pkg import app,mail
from pkg.forms import Login,SignUp,Contact
from pkg.models import db,User,QuickContact,State,Lga,UserType,Report,ReportCategory,Comment,Like,FeaturedServices,MessageTable,Feedback


# login requried decorator
def login_required(f):
    @wraps(f) #This ensure that the details about the original function f, that is being decorated is still available
    def check_login(*args, **kwargs):
        """Checks if session id is set or not"""
        if session.get('useronline') != None:
            return f(*args, **kwargs)
        else:
            flash("User Must Log In",category='error')
            return redirect(url_for('home'))
    return check_login

# user blocked checker
def blocked_checker(f):
    @wraps(f)
    def blocked_status(*args, **kwargs):
        """Checks if the user is blocked"""
        id = session.get('useronline')
        if id is None:
            flash("User Must Log In", category='error')
            return redirect(url_for('home'))
        user = db.session.query(User).get(id)
        if user is None:
            flash("User Must Log In", category='error')
            return redirect(url_for('home'))
        if user.user_status == "0":
            return f(*args, **kwargs)
        else:
            flash("User Blocked", category='error')
            return redirect(url_for('home'))
    return blocked_status




# Index/Login Page
@app.route("/login/", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def home():
    """The home route"""
    title = "Home - Login"
    login = Login()
    if request.method == 'GET':
        return render_template('user/index.html', title=title, login=login)
    else:
        if login.validate_on_submit():
            email = login.email.data
            pwd = login.password.data
            records = db.session.query(User).filter(User.user_email == email).first()
            if records:
                hashed_pwd = records.user_pwd
                rsp = check_password_hash(hashed_pwd,pwd)
                if rsp:
                    blocked = records.user_status
                    if blocked == "1":
                        flash('User blocked', category="error")
                        return redirect('/login/')
                    else:
                        # msg = Message("CSN Account Login",
                        #               sender="admin@csn.com",
                        #               recipients=[email])
                        # msg.html="<h1>Account Login</h1><p style='color:blue;'>Your Account has been logged in, if this isn't you, change your password rightaway</p>"
                        # mail.send(msg)
                        id = records.user_id
                        session['useronline'] = id
                        flash(f'Welcome Back! {records.user_fname.capitalize()}', category='info')
                        return redirect(url_for('userpage'))
                else:
                    flash('Invalid Login Credentials!', category='error')
                    return redirect('/login/')
            else:
                flash('Invalid Login Credentials!', category='error')
                return redirect('/login/')
    return render_template('user/index.html', title=title, login=login)


@app.route("/forgot-password/")
def user_forget_pass():
    title = "Home - Login"
    return render_template('user/user_forgot_pass.html', title=title)

@app.route("/pass/reset/", methods=['POST'])
def pass_reset():
    email = request.form.get('email')
    record = db.session.query(User).filter(User.user_email == email).first()
    if record:
        otp = [random.randint(0,9) for r in range(6)]
        otp_int = int(''.join(map(str, otp)))
        record.user_otp = otp_int
        db.session.commit()
        msg = Message("CSN - PASSWORD RESET",
                      sender="admin@csn.com",
                      recipients=[email])
        msg.html = f"<h1 style='color:green;'>OTP - Password Reset</h1><p style='color:black;'>Your OTP to reset your password is {otp_int}, if this wasn't requested by you, ignore this mail</p>"
        mail.send(msg)
        return "success"
    else:
        flash('Email account does not exist', category='error')
        return "error"

@app.route("/password/reset/", methods=['POST'])
def password_reset():
    otp = int(request.form.get('otp'))
    email = request.form.get('email')
    record = db.session.query(User).filter(User.user_email == email).first()
    if record.user_otp == otp:
        return "success"
    else:
        return "error"
    

@app.route("/reset/user/password/", methods=['POST'])
def reset_user_password():
    pwd = request.form.get('pwd')
    pwd1 = request.form.get('pwd1')
    email = request.form.get('email')
    record = db.session.query(User).filter(User.user_email == email).first()
    if pwd == pwd1:
        hashed_pwd = generate_password_hash(pwd)
        record.user_pwd = hashed_pwd
        flash('Password Reset Successful', category="info")
        return "success"
    else:
        return "error"
    
    

@app.route("/signup/", methods=['GET', 'POST'])
def sign_up():
    """The signup route"""
    title = "Home - SignUp"
    signup = SignUp()
    if request.method == 'GET':
        return render_template('user/signup.html', title=title, signup=signup)
    else:
        if signup.validate_on_submit():
            #retrieve data
            email = signup.email.data
            email_records = db.session.query(User).filter(User.user_email == email).first()
            if email_records:
                flash('Email Already Exist!', category='error')
                return redirect(url_for('sign_up'))
            fname = signup.fname.data
            lname = signup.lname.data
            pwd = signup.password.data
            gender = signup.gender.data
            phone = signup.phone.data
            hashed_pwd = generate_password_hash(pwd)
            user = User(user_email = email,user_fname = fname, user_lname = lname,user_pwd = hashed_pwd, user_gender=gender, user_phone = phone)
            db.session.add(user)
            db.session.commit()
            msg = Message("CSN Account Login",
                          sender="admin@csn.com",
                          recipients=[email])
            msg.html=f"<h1>New Account created for {email}</h1><p style='color:blue;'>You have created a new account on Community Safety Network</p>"
            mail.send(msg)
            id = user.user_id
            session['useronline'] = id
            flash(f'Welcome {user.user_fname.capitalize()}! You can edit your profile on the profile page',category='info')
            return redirect(url_for('userpage'))
        return render_template('user/signup.html', title=title, signup=signup)



# Start Index Pages
@app.route('/community-news/')
def community_news():
    title = "Community News"
    return render_template('user/communitynews.html', title=title)

@app.route('/safety-alerts/')
def safety_alerts():
    title = "Safety Alerts"
    return render_template('user/safetyalerts.html', title=title)

@app.route('/volunter-opportunities/')
def volunteer_opp():
    title = "Volunteer Opportunities"
    return render_template('user/volunteeropp.html', title=title)

@app.route('/community-forum/')
def community_forum():
    title = "Community Forum"
    return render_template('user/communityforum.html', title=title)

@app.route('/emergency-services/')
def emergency_services():
    title = "Emergency Services"
    return render_template('user/emergservices.html', title=title)

@app.route('/more-features/')
def more_services():
    title = "More Features"
    return render_template('user/moreservices.html', title=title)

@app.route('/contact-information/', methods=['GET','POST'])
def contact_info():
    title = "Community Information"
    contact = Contact()
    if request.method == 'GET':
        return render_template('user/contactinfo.html', title=title, contact=contact)
    else:
        if contact.validate_on_submit:
            name = contact.name.data
            email = contact.email.data
            message = contact.message.data
            deets = QuickContact(quick_contact_name = name,
            quick_contact_email = email,
            quick_contact_message = message)
            db.session.add(deets)
            db.session.commit()
            flash('Message Sent', category='info')
            return redirect(url_for('home'))
        else:
            flash('Message not sent', category='error')
            return render_template('user/contactinfo.html', title=title, contact=contact)
# End index Pages 

@app.route('/user-edit-display-picture/', methods=['POST','GET'])
@login_required
@blocked_checker
def change_dp():
    """View controller to edit profile picture"""
    id = session.get('useronline')
    deets = User.query.get(id)
    old_pix = deets.user_picture
    report_category = db.session.query(ReportCategory).all()
    if request.method == 'GET':
        return render_template('user/change_dp.html', deets=deets,report_category=report_category)
    else:
        dp = request.files.get('dp')
        filename = dp.filename
        if filename == "":
            flash('Please Select either a .jpg, .png or .jpeg file', category='Error')
            return redirect(url_for('change_dp'))
        else:
            name,ext = os.path.splitext(filename)
            allowed=['.jpg','.png','.jpeg']
            if ext.lower() in allowed:
                final_name = random.random() * 1000000000
                final_name = str(final_name) + ext
                try:
                    dp.save(f'pkg/static/profile_pictures/{final_name}')
                    user = db.session.query(User).get(id)
                    user.user_picture = final_name
                except:
                    os.remove(f'pkg/static/profile_pictures/{final_name}')
                else:
                    db.session.commit()
                try:
                    os.remove(f'pkg/static/profile_pictures/{old_pix}')
                except:
                    pass
                flash('Profile Picture Uploaded Successfully', category='success')
                return redirect(url_for('user_profile'))
            else:
                flash('upload either a .jpeg, .jpg or a .png file',category=('error'))
                return redirect(url_for('change_dp'))



@app.route('/user-edit-profile/', methods=['POST', 'GET'])
@login_required
@blocked_checker
def edit_profile():
    id = session.get('useronline')
    report_category = db.session.query(ReportCategory).all()
    if request.method == 'GET':
        deets = User.query.get(id)
        user_type = db.session.query(UserType).all()
        states = db.session.query(State).all()
        lgas = db.session.query(Lga).all()
        return render_template('user/edit_profile.html', deets=deets,user_type=user_type,states=states,lgas=lgas,report_category=report_category)
    else:
        user = User.query.get(id)
        user.user_fname = request.form.get('first_name')
        user.user_lname = request.form.get('last_name')
        user.user_gender = request.form.get('gender')
        user.user_type_id = request.form.get('user_type')
        user.user_address = request.form.get('address')
        user.user_state_id = request.form.get('state')
        user.user_lga_id = request.form.get('lga')
        user.user_phone = request.form.get('phone')
        user.user_website = request.form.get('website')
        user.user_opr_hours = request.form.get('operating_hour')
        # user.user_profile_lastedit = datetime.utcnow
        db.session.commit()
        flash('Profile Updated Successfully!', category=('info'))
        return redirect(url_for('user_profile'))

@app.route('/user-change-password/', methods=['GET','POST'])
@login_required
@blocked_checker
def user_change_password():
    id = session.get('useronline')
    if request.method == 'GET':
        deets = User.query.get(id)
        return render_template('user/user_change_password.html',deets=deets)
    else:
        old_pwd = request.form.get('old_pwd')
        new_pwd = request.form.get('new_pwd')
        new_pwd1 = request.form.get('new_pwd1')
        if old_pwd == "" or new_pwd == "" or new_pwd1 == "":
            flash('Enter all fields to change your password', category='error')
            return redirect(url_for('user_change_password'))
        else:
            user = User.query.get(id)
            hashed_pwd = user.user_pwd
            pwd = check_password_hash(hashed_pwd,old_pwd)
            if pwd:
                if new_pwd != new_pwd1:
                    flash('Confirm new password match', category='error')
                    return redirect(url_for('user_change_password'))
                elif new_pwd == old_pwd:
                    flash('Cannot change to a currently used password ', category='error')
                    return redirect(url_for('user_change_password'))
                else:
                    new_password = generate_password_hash(new_pwd)
                    user.user_pwd = new_password
                    db.session.commit()
                    flash('Password Changed Successfully!', category='info')
                    return redirect(url_for('user_profile'))
            else:
                flash('Old Password incorrect', category='error')
                return redirect(url_for('admin_change_password'))


@app.route('/state/lgas/', methods=['GET','POST'])
@login_required
@blocked_checker
def get_lgas():
    stateID = request.form.get('state')
    print(stateID)
    state = State.query.get_or_404(stateID)
    lgas = []
    lga_data = state.state_lga_deets
    for lga in lga_data:
        lgas.append({"lga_id":lga.lga_id,'lga_name':lga.lga_name})
    return jsonify(lgas)


@app.route('/user-page/', methods=['GET', 'POST'])
@login_required
@blocked_checker
def userpage():
    id = session.get('useronline')
    deets = User.query.get(id)
    all_reports = db.session.query(Report).filter(Report.report_status == "0").order_by(Report.report_date.desc()).all()
    report_category = db.session.query(ReportCategory).all()
    user_likes = {like.like_report_id: True for like in Like.query.filter_by(like_user_id=id).all()}
    report_likes_count = {like.like_report_id: Like.query.filter_by(like_report_id=like.like_report_id).count() for like in Like.query.all()}
    comment_counts = {comment.comment_report_id: Comment.query.filter_by(comment_report_id=comment.comment_report_id).count() for comment in Comment.query.all()}
    report_comments = {post.report_id: Comment.query.filter_by(comment_report_id=post.report_id).order_by(Comment.comment_datetime.desc()).all() for post in all_reports}
    top_featured_services = db.session.query(FeaturedServices).order_by(FeaturedServices.featured_date_created.desc()).limit(3)
    if request.method == 'GET':
        return render_template('user/user_page.html',deets=deets,report_category=report_category,all_reports=all_reports,user_likes=user_likes,report_likes_count=report_likes_count,report_comments=report_comments,comment_counts=comment_counts,top_featured_services=top_featured_services)
    else:
        report = request.form.get('report')
        category = request.form.get('category')
        anonymous = request.form.get('anonymous')
        report_pic = request.files.get('report_pic')
        report_pic_name = report_pic.filename
        name,ext = os.path.splitext(report_pic_name)
        report_pic_ext_allowed=['.jpg','.png','.jpeg' ]
        if report == "":
            flash('Write a content and select a category to post a report', category='error')
            return redirect(url_for('userpage'))
        elif category == "":
            flash('You must select a category to post a report', category='error')
            return redirect(url_for('userpage'))
        else:
            if report_pic_name == "":
                post_report=Report(
                    report_user_id = id,
                    report_category_id = category,
                    report_desc = report,
                    report_hide_user = anonymous
                    )
                db.session.add(post_report)
                db.session.commit()
                flash('Report Posted Successfully!', category='info')
                return redirect(url_for('userpage'))
            else:
                if ext.lower() in report_pic_ext_allowed:
                    report_pix = random.random() * 1000000
                    report_pix = str(report_pix) + ext
                    try:
                        report_pic.save(f'pkg/static/report_images/{report_pix}')
                    except:
                        os.remove(f'pkg/static/report_images/{report_pix}')
                    else:
                        post_report=Report(
                            report_user_id = id,
                            report_category_id = category,
                            report_file_name = report_pix,
                            report_desc = report,
                            report_hide_user = anonymous
                            )
                        db.session.add(post_report)
                        db.session.commit()
                        flash('Report Posted Successfully!', category='info')
                        return redirect(url_for('userpage'))
                else:
                    flash('Upload either a .jpg, .png or .jpeg file', category='error')
                    return redirect(url_for('userpage'))
    



@app.route('/comment/', methods=['POST'])
@login_required
@blocked_checker
def comment():
     id = session.get('useronline')
     report_id = request.form.get('report_id')
     comment = request.form.get('comment')
     if comment == "":
         return "error"
     else:
         user_comment = Comment(
             comment_report_id = report_id,
             comment_user_id = id,
             comment_desc = comment
             )
         db.session.add(user_comment)
         db.session.commit()
         data2return = {'report_id' : user_comment.comment_report_id,
                        'user_fname' : user_comment.comment_user_deet.user_fname,
                        'user_lname' : user_comment.comment_user_deet.user_lname,
                        'comment' : user_comment.comment_desc,
                        'comment_date': user_comment.comment_datetime}
         return jsonify(data2return)
     


@app.route('/like/', methods=['POST'])
@login_required
@blocked_checker
def like():
    id = session.get('useronline')
    report_id = request.form.get('report_id')
    status = "0"
    like = Like(like_report_id = report_id,
                like_user_id = id,
                like_status = status
                )
    db.session.add(like)
    db.session.commit()
    like_count = db.session.query(Like).filter_by(like_report_id=report_id).count()
    count = {'count': like_count}
    return jsonify(count)



@app.route('/unlike/', methods=['POST'])
@login_required
@blocked_checker
def unlike():
    id = session.get('useronline')
    report_id = request.form.get('report_id')
    unlike = Like.query.filter_by(like_report_id=report_id, like_user_id=id).first()
    db.session.delete(unlike)
    db.session.commit()
    like_count = db.session.query(Like).filter_by(like_report_id=report_id).count()
    count = {'count': like_count}
    return jsonify(count)


@app.route('/user-profile/')
@login_required
@blocked_checker
def user_profile():
    id = session.get('useronline')
    deets = User.query.get(id)
    all_reports = db.session.query(Report).filter_by(report_user_id = id, report_status= "0").order_by(Report.report_date.desc()).all()
    report_category = db.session.query(ReportCategory).all()
    user_reports = db.session.query(Report).filter_by(report_user_id=id,report_status= "0").count()
    user_likes = {like.like_report_id: True for like in Like.query.filter_by(like_user_id=id).all()}
    report_likes_count = {like.like_report_id: Like.query.filter_by(like_report_id=like.like_report_id).count() for like in Like.query.all()}
    comment_counts = {comment.comment_report_id: Comment.query.filter_by(comment_report_id=comment.comment_report_id).count() for comment in Comment.query.all()}
    report_comments = {post.report_id: Comment.query.filter_by(comment_report_id=post.report_id).order_by(Comment.comment_datetime.desc()).all() for post in all_reports}
    return render_template('user/user_profile.html', deets=deets, all_reports=all_reports,report_category=report_category,user_reports=user_reports,user_likes=user_likes,report_likes_count=report_likes_count,comment_counts=comment_counts,report_comments=report_comments)


@app.route('/profile/<user_id>/')
@login_required
@blocked_checker
def visit_profile(user_id):
    id = session.get('useronline')
    deets = User.query.get(id)
    profile_info = User.query.get(user_id)
    total_reports = db.session.query(Report).filter(Report.report_user_id == user_id,Report.report_status == "0",Report.report_hide_user == None).count()
    all_reports = db.session.query(Report).filter_by(report_user_id = user_id,report_status = "0").order_by(Report.report_date.desc()).all()
    report_category = db.session.query(ReportCategory).all()
    user_likes = {like.like_report_id: True for like in Like.query.filter_by(like_user_id=id).all()}
    report_likes_count = {like.like_report_id: Like.query.filter_by(like_report_id=like.like_report_id).count() for like in Like.query.all()}
    comment_counts = {comment.comment_report_id: Comment.query.filter_by(comment_report_id=comment.comment_report_id).count() for comment in Comment.query.all()}
    report_comments = {post.report_id: Comment.query.filter_by(comment_report_id=post.report_id).order_by(Comment.comment_datetime.desc()).all() for post in all_reports}
    return render_template('user/visit_profile.html',deets=deets,all_reports=all_reports,profile_info=profile_info,report_category=report_category,user_likes=user_likes,report_likes_count=report_likes_count,comment_counts=comment_counts,report_comments=report_comments,total_reports=total_reports)
    

# @app.route('/profile/<user>}/')
# @login_required
# @blocked_checker
# def user_select(user):
#     id = session.get('useronline')
#     deets = User.query.get(id)
#     user_select = db.session.query(User).filter(User.user_id == user)
#     report_category = db.session.query(ReportCategory).all()
#     return render_template('user/user_select.html', deets=deets,user_select=user_select,report_category=report_category)



@app.route('/user-community-news/')
@login_required
@blocked_checker
def user_comm_news():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/user_comm_news.html',deets=deets)



@app.route('/user-safety-alerts/')
@login_required
@blocked_checker
def user_safety_alerts():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/user_safety_alerts.html',deets=deets)



@app.route('/user-emergency-services/')
@login_required
@blocked_checker
def user_emergency_services():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/user_emerg_serv.html',deets=deets)



@app.route('/user-community-members/')
@login_required
@blocked_checker
def user_community_members():
    id = session.get('useronline')
    deets = User.query.get(id)
    all_users = db.session.query(User).all()
    return render_template('user/user_comm_member.html',deets=deets,all_users=all_users)



@app.route('/user-schools-nearby/')
@login_required
@blocked_checker
def schools_nearby():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/user_schools_nearby.html',deets=deets)



@app.route('/user-church-nearby/')
@login_required
@blocked_checker
def church_nearby():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/church_nearby.html',deets=deets)



@app.route('/user-mosque-nearby/')
@login_required
@blocked_checker
def mosque_nearby():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/mosque_nearby.html',deets=deets)



@app.route('/user-hospital-nearby/')
@login_required
@blocked_checker
def hospital_nearby():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/hospital_nearby.html',deets=deets)



@app.route('/user-featured-services/')
@login_required
@blocked_checker
def user_featured_services():
    id = session.get('useronline')
    deets = User.query.get(id)
    featured_services = FeaturedServices.query.all()
    return render_template('user/user_featured_services.html',deets=deets,featured_services=featured_services)



@app.route('/user-upcoming-events/')
@login_required
@blocked_checker
def user_upcoming_events():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/user_upcoming_events.html',deets=deets)



@app.route('/user-volunter-opportunity/')
@login_required
@blocked_checker
def user_volunter_opp():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/user_volunter_opp.html',deets=deets)



@app.route('/user-community-forum/')
@login_required
@blocked_checker
def user_community_forum():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/user_community_forum.html',deets=deets)



@app.route('/user-neighbourhood-watch/')
@login_required
@blocked_checker
def neighbourhood_watch():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/neighbourhood_watch.html',deets=deets)



@app.route('/user-community-feedback/', methods=['GET','POST'])
@login_required
@blocked_checker
def community_feedback():
    id = session.get('useronline')
    deets = User.query.get(id)
    if request.method == 'GET':
        return render_template('user/community_feedback.html',deets=deets)
    else:
        feedback = request.form.get('feedback')
        if feedback == "":
            flash('Enter a Feedback Message to Submit',category='error')
            return redirect(url_for('community_feedback'))
        else:
            fb = Feedback(
                feedback_user_id = id,
                feedback_msg = feedback
            )
            db.session.add(fb)
            db.session.commit()
            flash('Feedback Submitted Successfully',category='info')
            return redirect(url_for('userpage'))



@app.route('/user-message/')
@login_required
@blocked_checker
def user_message():
    id = session.get('useronline')
    deets = User.query.get(id)
    all_users = db.session.query(User).filter(User.user_status == "0").all()
    return render_template('user/user_message.html',deets=deets,all_users=all_users)



@app.route('/send-message/<user>/', methods=['GET','POST'])
@login_required
@blocked_checker
def send_message(user):
    id = session.get('useronline')
    deets = User.query.get(id)
    receiver = User.query.get(user)
    all_users = db.session.query(User).filter(User.user_status == "0").all()
    message = MessageTable.query.filter(
        ((MessageTable.message_user1_id == id) & (MessageTable.message_user2_id == user)) |
        ((MessageTable.message_user1_id == user) & (MessageTable.message_user2_id == id))
    ).all()
    return render_template('user/send_message.html',all_users=all_users,deets=deets,message=message,receiver=receiver)


    
@app.route('/send/', methods=['POST'])
@login_required
@blocked_checker
def send():
    sender_id = session.get('useronline')
    msg = request.form.get('message')
    receiver_id = request.form.get('receiver_id')
    if msg == "":
        return "error"
    else:
        message = MessageTable(
            message_content = msg,
            message_user1_id = sender_id,
            message_user2_id = receiver_id
            )
        db.session.add(message)
        db.session.commit()
        message_details = {
            'id': message.message_id,
            'sender_id': message.message_user1_id,
            'receiver_id': message.message_user2_id,
            'content': message.message_content
            }
        return jsonify(message_details)



@app.route('/user-search-page/', methods=['GET', 'POST'])
@login_required
@blocked_checker
def user_search_page():
    """User Search Page Route"""
    id = session.get('useronline')
    deets = User.query.get(id)
    top_featured_services = db.session.query(FeaturedServices).order_by(FeaturedServices.featured_date_created.desc()).limit(3)
    if request.method == 'GET':
        return render_template('user/user_search_page.html',deets=deets,top_featured_services=top_featured_services)
    else:
        search_input = request.form.get('search_input')
        user_results = User.query.filter(or_(
            User.user_fname.ilike(f'%{search_input}%'),
            User.user_lname.ilike(f'%{search_input}%')
        )).all()
        report_results = Report.query.filter(Report.report_desc.ilike(f'%{search_input}%')).all()
        category_results = ReportCategory.query.filter(ReportCategory.report_category_name.ilike(f'%{search_input}%')).all()
        results = {
            'users': [{'id': user.user_id, 'name': f'{user.user_fname} {user.user_lname}', 'type': 'People'} for user in user_results],
            'reports': [{'id': report.report_id, 'name': report.report_desc, 'type': 'Report'} for report in report_results],
            'categories': [{'id': category.report_category_id, 'name': category.report_category_name, 'type': 'Category'} for category in category_results]
        } 
        return jsonify(results)

@app.route('/logout/')
@login_required
@blocked_checker
def logout():
    """Logout route"""
    # if session.get('useronline') != None :
    session.pop('useronline',None)
    return redirect(url_for('home'))
