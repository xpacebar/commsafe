from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    user_fname = db.Column(db.String(30))
    user_lname = db.Column(db.String(30))
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_pwd = db.Column(db.String(255), nullable=False)
    user_gender = db.Column(db.Enum('male','female'))
    user_picture = db.Column(db.String(30))
    user_phone = db.Column(db.String(20))
    user_desc = db.Column(db.Text())
    user_address = db.Column(db.Text())
    user_opr_hours = db.Column(db.Text())
    user_website = db.Column(db.String(50))
    user_type_id = db.Column(db.Integer(), db.ForeignKey('usertype.usertype_id'))
    user_lga_id = db.Column(db.Integer(), db.ForeignKey('lga.lga_id'))
    user_state_id = db.Column(db.Integer(), db.ForeignKey('state.state_id'))
    user_status = db.Column(db.Enum('0', '1'), default='0')
    user_date_reg = db.Column(db.DateTime(), default=datetime.utcnow)
    user_profile_lastedit = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    user_last_login = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    user_usertype_deets = db.relationship("UserType", back_populates="usertype_deets")
    user_lga_deets = db.relationship('Lga', back_populates='lga_deets')
    user_state_deets = db.relationship('State', back_populates='state_deets')
    user_message_deets = db.relationship('Message', primaryjoin="User.user_id == Message.message_user1_id", back_populates='message_deets')
    user_report_deets = db.relationship('Report', back_populates='report_user_deets')


class UserType(db.Model):
    __tablename__ = 'usertype'
    usertype_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    usertype_type = db.Column(db.String(100), nullable=False)
    usertype_deets = db.relationship('User', back_populates='user_usertype_deets')

class Lga(db.Model):
    __tablename__ = 'lga'
    lga_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    lga_name = db.Column(db.String(100), nullable=False)
    lga_state_id = db.Column(db.Integer(), db.ForeignKey('state.state_id'))
    lga_state_deets = db.relationship('State', back_populates='state_lga_deets')
    lga_deets = db.relationship('User', back_populates='user_lga_deets')

class State(db.Model):
    __tablename__ = 'state'
    state_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    state_name = db.Column(db.String(100), nullable=False)
    state_lga_deets = db.relationship('Lga', back_populates='lga_state_deets')
    state_deets = db.relationship('User', back_populates='user_state_deets')
    
class Message(db.Model):
    __tablename__ = 'message'
    message_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    message_user1_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'), nullable=False)
    message_user2_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'), nullable=False)
    message_content = db.Column(db.Text(), nullable = False)
    message_created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    message_updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    message_deets = db.relationship('User', primaryjoin="Message.message_user1_id == User.user_id", back_populates='user_message_deets')


class Report(db.Model):
    __tablename__ = 'report'
    report_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    report_user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'))
    report_category_id = db.Column(db.Integer(), db.ForeignKey('report_category.report_category_id'))
    report_location = db.Column(db.String(255))
    report_desc = db.Column(db.Text(), nullable=False)
    report_file_name = db.Column(db.String(100))
    report_status = db.Column(db.Enum('0', '1'), default='0')
    report_hide_user = db.Column(db.Enum('on'))
    report_date = db.Column(db.DateTime(), default=datetime.utcnow)
    report_lastedit = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    report_user_deets = db.relationship('User', back_populates='user_report_deets')
    report_cat_deets = db.relationship('ReportCategory', back_populates='report_deets')


class ReportCategory(db.Model):
    __tablename__ = 'report_category'
    report_category_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    report_category_name =db.Column(db.String(120), nullable=False)
    report_deets = db.relationship('Report', back_populates='report_cat_deets')


class QuickContact(db.Model):
    __tablename__ = 'quick_contact'
    quick_contact_id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    quick_contact_name = db.Column(db.String(80), nullable=False)
    quick_contact_email = db.Column(db.String(60), nullable=False)
    quick_contact_message = db.Column(db.Text(), nullable=False)
    quick_contact_date = db.Column(db.DateTime(), default=datetime.utcnow)
