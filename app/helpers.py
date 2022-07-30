from flask_login import current_user, login_manager
from flask import session, flash, redirect, url_for, render_template
from functools import wraps
from app.models import Hospital
from app import db, mail, app
from flask_mail import Message
from threading import Thread


# Defining admin_required
# We check if user is admin
# If not, notify that they must login to access the page

def admin_required(fn):
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if not is_admin():
            flash('You must log in to access this page.')
            return redirect(url_for('staff_login'))
        return fn(*args, **kwargs)
    return decorated_view


# Defining is admin by returning that admin is in session
def is_admin():
    return "is_admin" in session


def admin_login():
    session["is_admin"] = ""


def admin_logout():
    session.pop("is_admin")

# Defining function find, which takes in department as an argument


def find(department):

    # Query table hospital filtering by the department provided
    client_ticket = Hospital.query.filter_by(department=department, was_served=False).all()
    return client_ticket

# Defining find_user which takes in department as an argument


def find_user(department):

    # Finding ticket by filtering using the current user's username and the department provided
    client_ticket = Hospital.query.filter_by(username=current_user.username, department=department, was_served=False).first()
    return client_ticket

# Removing ticket from table hospital by taking  department as an argument

def remove(department):

    # Query table hospital filtering by the department provided
    ticket = Hospital.query.filter_by(department=department, was_served=False).first()

    # If the ticket is there, delete it else flash no user in line
    if ticket:
        ticket.was_served=True
        db.session.commit()
    else:
        flash("No user in Line")
    return True


# Enabling users to delete their own tickets

def delete(department):

    # Checking if their are tickets to delete
    ticket = Hospital.query.filter_by(username=current_user.username, department=department, was_served=False).first()

    # if their are tickets, delete else flash no ticket
    if ticket:
        ticket.was_served=True
        db.session.commit()
    else:
        flash("No Ticket")
    return True


# Sending reset passwords emails
def send_reset_email(user):

    # first get token from user model
    token = user.get_reset_token()

    # send email, using the first admin, recipient being the users email
    send_email('[QSol] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# Sending actual email, with subject, sender, recipient, and body


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()