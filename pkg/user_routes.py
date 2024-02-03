from datetime import datetime
# import requests,json
import os,random,string
from functools import wraps
from flask import Flask,render_template,url_for,request,redirect,session,flash,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from pkg import app
from pkg.forms import Login,SignUp,Contact
from pkg.models import db,User,QuickContact,State,Lga,UserType,Report,ReportCategory,Message,Comment,Like


# login requried decorator
def login_required(f):
    @wraps(f) #This ensure that the details about the original function f, that is being decorated is still available
    def check_login(*args, **kwargs):
        """Checks if session id is set or not"""
        if session.get('useronline') != None:
            return f(*args, **kwargs)
        else:
            flash("You must be logged in to access this page",category='error')
            return redirect(url_for('home'))
    return check_login



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
                    id = records.user_id
                    session['useronline'] = id
                    flash(f'Welcome Back! {records.user_fname}', category='info')
                    return redirect(url_for('userpage'))
                else:
                    flash('Invalid Login Credentials!', category='error')
                    return redirect('/login/')
            else:
                flash('Invalid Login Credentials!', category='error')
                return redirect('/login/')
    return render_template('user/index.html', title=title, login=login)

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
            pwd = signup.password.data
            gender = signup.gender.data
            phone = signup.phone.data
            hashed_pwd = generate_password_hash(pwd)
            user = User(user_email = email,user_pwd = hashed_pwd, user_gender=gender, user_phone = phone)
            db.session.add(user)
            db.session.commit()
            id = user.user_id
            session['useronline'] = id
            flash('Welcome! You can edit your profile on the profile page',category='info')
            return redirect(url_for('userpage'))
        return render_template('user/signup.html', title=title, signup=signup)


@app.route('/user-edit-display-picture/', methods=['POST','GET'])
@login_required
def change_dp():
    """View controller to edit profile picture"""
    id = session.get('useronline')
    deets = User.query.get(id)
    old_pix = deets.user_picture
    if request.method == 'GET':
        return render_template('user/change_dp.html', deets=deets)
    else:
        dp = request.files.get('dp')
        filename = dp.filename
        if filename == "":
            flash('Please Select a File', category='Error')
            return render_template('user/change_dp.html')
        else:
            name,ext = os.path.splitext(filename)
            allowed=['.jpg','.png','jpeg' ]
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
                flash('upload a .jpeg, .jpg or a .png file',category=('error'))
                return redirect(url_for('change_dp'))


@app.route('/user_edit-profile/', methods=['POST', 'GET'])
@login_required
def edit_profile():
    id = session.get('useronline')
    if request.method == 'GET':
        deets = User.query.get(id)
        user_type = db.session.query(UserType)
        states = db.session.query(State).all()
        lgas = db.session.query(Lga).all()
        return render_template('user/edit_profile.html', deets=deets,user_type=user_type,states=states,lgas=lgas)
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
        flash('Profile Updateds Successfully!', category=('info'))
        return redirect(url_for('user_profile'))


@app.route('/user-page/', methods=['GET', 'POST'])
@login_required
def userpage():
    id = session.get('useronline')
    deets = User.query.get(id)
    all_posts = db.session.query(Report).order_by(Report.report_date.desc()).all()
    report_category = db.session.query(ReportCategory).all()
    comments = db.session.query(Comment).all()
    user_likes = {like.like_report_id: True for like in Like.query.filter_by(like_user_id=id).all()}
    post_likes_count = {like.like_report_id: Like.query.filter_by(like_report_id=like.like_report_id).count() for like in Like.query.all()}
    comments = 
    if request.method == 'GET':
        return render_template('user/user_page.html',deets=deets,report_category=report_category,all_posts=all_posts,comments=comments,user_likes=user_likes,post_likes_count=post_likes_count)
    else:
        post = request.form.get('post')
        category = request.form.get('category')
        anonymous = request.form.get('anonymous')
        # post_pic = request.files.get('post_pic')
        if post == "":
            flash('Write a content and select a category to post a report', category='error')
            return redirect(url_for('userpage'))
        elif category == "":
            flash('You must select a category to post a report', category='error')
            return redirect(url_for('userpage'))
        else:
            report =Report(
                report_user_id = id,
                report_category_id = category,
                report_desc = post,
                report_hide_user = anonymous
                )
            db.session.add(report)
            db.session.commit()
            flash('Report Posted Successfully!', category='info')
            return redirect(url_for('userpage'))        


@app.route('/comment/', methods=['POST'])
@login_required
def comment():
     id = session.get('useronline')
     report_id = request.form.get('report_id')
     comment = request.form.get('comment')
     if comment == "":
         return None
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
def user_profile():
    id = session.get('useronline')
    deets = User.query.get(id)
    reports = db.session.query(Report).filter(Report.report_user_id == id).order_by(Report.report_date.desc()).all()
    return render_template('user/user_profile.html', deets=deets, reports=reports)



@app.route('/profile/<user>}/')
@login_required
def user_select(user):
    id = session.get('useronline')
    deets = User.query.get(id)
    user_select = db.session.query(User).filter(User.user_id == user)
    return render_template('user/user_select.html', deets=deets,user_select=user_select)

@app.route('/user-community-news/')
@login_required
def user_comm_news():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/user_comm_news.html', deets=deets)

@app.route('/user-safety-alerts/')
@login_required
def user_safety_alerts():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/user_safety_alerts.html',deets=deets)

@app.route('/user-emergency-services/')
@login_required
def user_emergency_services():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/user_emerg_serv.html',deets=deets)

@app.route('/user-community-members/')
@login_required
def user_community_members():
    id = session.get('useronline')
    deets = User.query.get(id)
    all_users = db.session.query(User).all()
    return render_template('user/user_comm_member.html',deets=deets,all_users=all_users)

@app.route('/user-schools-nearby/')
@login_required
def schools_nearby():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/user_schools_nearby.html',deets=deets)


@app.route('/user-church-nearby/')
@login_required
def church_nearby():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/church_nearby.html',deets=deets)

@app.route('/user-mosque-nearby/')
@login_required
def mosque_nearby():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/mosque_nearby.html',deets=deets)

@app.route('/user-hospital-nearby/')
@login_required
def hospital_nearby():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/hospital_nearby.html',deets=deets)



@app.route('/user-featured-services/')
@login_required
def user_featured_services():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/user_featured_services.html',deets=deets)


@app.route('/user-upcoming-events/')
@login_required
def user_upcoming_events():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/user_upcoming_events.html', deets=deets)


@app.route('/user-volunter-opportunity/')
@login_required
def user_volunter_opp():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/user_volunter_opp.html', deets=deets)

@app.route('/user-community-forum/')
@login_required
def user_community_forum():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/user_community_forum.html',deets=deets)

@app.route('/user-neighbourhood-watch/')
@login_required
def neighbourhood_watch():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/neighbourhood_watch.html',deets=deets)



@app.route('/user-community-feedback/')
@login_required
def community_feedback():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/community_feedback.html',deets=deets)

@app.route('/user-message/')
@login_required
def user_message():
    id = session.get('useronline')
    deets = User.query.get(id)
    all_users = db.session.query(User).all()
    return render_template('user/user_message.html',deets=deets,all_users=all_users)


@app.route('/send-message/<user>/', methods=['GET','POST'])
@login_required
def send_message(user):
    id = session.get('useronline')
    deets = User.query.get(id)
    receiver = User.query.get(user)
    all_users = db.session.query(User).all()
    message = Message.query.filter(
        ((Message.message_user1_id == id) & (Message.message_user2_id == user)) |
        ((Message.message_user1_id == user) & (Message.message_user2_id == id))
    ).all()
    return render_template('user/send_message.html',all_users=all_users,deets=deets,message=message,receiver=receiver)


    
@app.route('/send/', methods=['POST'])
@login_required
def send():
    sender_id = session.get('useronline')
    msg = request.form.get('message')
    receiver_id = request.form.get('receiver_id')
    if msg == "":
        return
    else:
        message = Message(
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




@app.route('/user-search-page/')
@login_required
def user_search_page():
    id = session.get('useronline')
    deets = User.query.get(id)
    return render_template('user/user_search_page.html',deets=deets)



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


@app.route('/logout/')
@login_required
def logout():
    """Logout route"""
    if session.get('useronline') != None :
        session.pop('useronline',None)
        return redirect(url_for('home'))
