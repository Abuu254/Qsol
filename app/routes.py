
from os import error
from flask import render_template, url_for, redirect, flash, request
from sqlalchemy import desc, func
from sqlalchemy.orm import session
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
from app.forms import LoginForm, RegistrationForm, hospitalform, departments,staff, ChangePasswordForm, ResetRequestForm, ResetForm, ChangeUsernameForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Hospital
from werkzeug.urls import url_parse
from app.helpers import is_admin, admin_login, admin_logout, admin_required, find, remove, send_reset_email, delete, find_user


@app.context_processor
def utility_processor():
    return dict(is_admin=is_admin)


@app.route('/')
@app.route('/index')
@login_required
def index():
    """ Display clients active bookings on the homepage """
    # Check if a user has active tickets
    client_ticket = Hospital.query.filter_by(username=current_user.username, was_served=False).all()

    # If user has no active tickets, you display the message
    if not client_ticket:
        message = "You have no active bookings"
        return render_template('index.html', title='Home Page', message=message)

    # If user has active bookings, display a table showing the bookings
    message = "My Active Bookings"
    mylist = []

    # Check if the user has bookings in all the section and add the bookings into a list
    sections = ['Inquiry', 'Admissions', 'Consultation', 'Laboratory', 'Pharmacy']
    for section in sections:
        rows = Hospital.query.filter_by(department=section, was_served=False).all()
        if rows:
            mylist.append(rows)
    return render_template('index.html', title='Home Page', message=message, client_ticket=client_ticket, mylist=mylist)


@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    """ Loging users into the web app """
    # See if user is alreader logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # If a user is not logged in, you display the login form
    form = LoginForm()
    if form.validate_on_submit():

        # When login form is submitted, check if the client's credential are authentic else raise errors
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        # Creating a variable next page to represent the page user wanted to access before logging in
        next_page = request.args.get('next')

        # If no next page is available, redirect user to index page,
        # Also, use url parse to ensure a user does not try to use a malicius site as the next page
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    """ Logging users out """
    logout_user()
    return redirect(url_for('login'))


@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    """ Regestering users into the web app """
    # First check if the current user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # If not, you display the regestration form
    form = RegistrationForm()

    # If the form is validated on submission
    if form.validate_on_submit():

        # Insert into table users with the users data, the username and the email
        client = User(username=form.username.data, email=form.email.data)

        # Use the function set_password defined in user model
        client.set_password(form.password.data)

        # Then add the user into the database
        db.session.add(client)
        db.session.commit()
        flash('Registration Successful!')
        return redirect(url_for('login'))
    return render_template('auth/register.html', title='Register', form=form)


@app.route('/account/<username>')
@login_required
def account(username):
    """ Displaying users information """

    # We query user filtering by the username
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('account.html', user=user)


@app.route('/change_username', methods=['GET', 'POST'])
@login_required
def change_username():
    """ Changing users' usernames """

    # display the form when the user clicks this route
    form = ChangeUsernameForm()

    # If form is validated, check if the password is correct
    if form.validate_on_submit():
        if not check_password_hash(current_user.password_hash, request.form.get('password')):
            flash('Incorrect Password')

        # if password is correct, add the new username into the database
        current_user.username = request.form.get('username')
        db.session.commit()
        flash("Username changed successfully")
        return redirect(url_for('account', username=current_user.username))
    return render_template('auth/change_username.html', form=form)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """ Changing users' passwords """

    form = ChangePasswordForm()
    if form.validate_on_submit():

        # check if the current password is correct
        if not check_password_hash(current_user.password_hash, request.form.get('old_password')):
            flash('Incorrect Old Password')
            return redirect(request.referrer)
        # Hash the password, and then add it to the database
        current_user.password_hash = generate_password_hash(request.form.get('password'))
        db.session.commit()
        flash("password changed successfully")
        return redirect(url_for('account', username=current_user.username))
    return render_template('change_password.html', form=form)


@app.route('/hospital', methods=['GET', 'POST'])
@login_required
def hospital():
    """ Regestration of users into different departments of a hospital"""

    # First, display a form where users choose a hospital
    form = hospitalform()
    if form.validate_on_submit():

        # If a user does not choose a hospital, raise an error
        if (hospital := request.form.get('hospital')) == 'None':
            flash("choose a hospital")
            return redirect(request.referrer)

        # If a user does not choose a department, raise an error
        if (section := request.form.get('department')) == 'None':
            flash("Choose a department")
            return redirect(request.referrer)

        # Check if a user exists in the queue of that specific departement
        exists = Hospital.query.filter_by(username=current_user.username, name=hospital, department=section, was_served=False).first() is not None

        # If the user exists, flash already in line
        if exists:
            flash("Already in line")
            return redirect(request.referrer)

        # Add a booking into the table hospital
        booking = Hospital(username=current_user.username, name=hospital, department=section, user_id=current_user.id, was_served=False)
        db.session.add(booking)
        db.session.commit()


        # Getting the added ticket
        client_ticket = Hospital.query.filter_by(username=current_user.username, name=hospital, department=section, was_served=False).first_or_404()

        # finding the total number of tickets already in queue
        queue = Hospital.query.filter_by(name=hospital, department=section, was_served=False).order_by(Hospital.timestamp).all()

        # Finding the size of the queue
        size = len(queue)

        # Finding the position of the user in the queue
        index = queue.index(client_ticket)
        head = "Regestration Successful"

        return render_template('success.html', head=head, people_ahead=index, size=size, ticket=client_ticket.id, department=client_ticket.department, institution=hospital)

    return render_template('hospital.html', form=form)


@app.route("/history")
@login_required
def ticket_history():
    """ Displaying users' ticket history """

    # Get number of pages from query string argument or 1 as a default
    page = request.args.get('page', 1, type=int)

    # Getting the users all time bookings and paginating them
    bookings = Hospital.query.filter_by(username=current_user.username, was_served=True).order_by(Hospital.timestamp.desc()).paginate(
        page, app.config['TICKETS_PER_PAGE'], False)

    # Find the next url if the bookings have next numbers after paginating
    next_url = url_for('ticket_history', page=bookings.next_num) if bookings.has_next else None

    # Finding the previous url if the bookings have previous numbers
    prev_url = url_for('ticket_history', page=bookings.prev_num) if bookings.has_prev else None
    return render_template('history.html', bookings=bookings.items, next_url=next_url, prev_url=prev_url)


@app.route("/choose_section")
@login_required
def sector():
    return render_template('sector.html')


@app.route("/track_tickets", methods=['POST'])
@login_required
def track():
    """ Enabling users to delete their tickets """

    # Get the department which the user wants to track bookings
    name = request.form.get('name')

    # Including an option for users to delete their tickets if need to
    if name in ['Inquiry', 'Admissions', 'Consultation', 'Laboratory', 'Pharmacy']:
        delete(name)
        flash('Ticket Deleted')
    return redirect(request.referrer)


@app.route('/tracking/<name>')
@login_required
def tracking(name):
    """ Enabling users to track their tickets """

    # Find the clients ticket using defined function find_user
    client_ticket = find_user(name)

    # check if the ticket really exists
    if client_ticket:

        # Find total number of people in line by quering all users active in that department

        people_in_line = Hospital.query.filter_by(department=name, was_served=False).order_by(Hospital.timestamp).all()

        # Find the total number of people in line
        size = len(people_in_line)

        # Find the index of the user
        index = people_in_line.index(client_ticket)

        # Check if the index is not equal to 0, then the users position is the index plus 1
        if index == 0:
            position = "Being Served"
        else:
            position = index + 1
        return render_template('track_display.html', client_ticket=client_ticket, name=name, position=position, size=size)
    return render_template('track_display.html')


@app.route('/track_tickets')
@login_required
def select_department():
    return render_template('track.html')


@app.route('/admin', methods=['POST', 'GET'])
def staff_login():
    """ Logging of staff users or administrators """

    # Check if user is admin
    if is_admin():
        return redirect(url_for('staff_view'))

    form = staff()
    # when login form is submitted, check if the staff credential are authentic else raise errors
    if request.method == 'POST':
        if form.password.data == app.config["ADMIN_PASS"]:
            admin_login()
        else:
            flash("Incorrect password")
            return redirect(request.referrer)

        # creating a variable next page to represent the page user wanted to access before logging in
        next_page = request.args.get('next')

        # if no next page is available, redirect user to index page,
        # also, use url parse to ensure a user does not try to use a malicius site as the next page
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('staff_view')
            return redirect(next_page)
    return render_template('staff/admin_login.html', form=form)


@app.route('/display_queues', methods=['GET', 'POST'])
@admin_required
def display_queues():
    """ Displaying all time users to the administrators"""
    form = departments()
    if form.validate_on_submit():
        sections = ['inquiry', 'admissions', 'consultation', 'laboratory', 'pharmacy']

        # Check if the section submitted is in the above, if it is , find all the bookings of that department from table history
        for section in sections:
            if request.form.get(section):
                client_ticket = Hospital.query.filter_by(department=request.form.get(section)).all()

                return render_template('staff/ticket_history.html', client_ticket=client_ticket)
        message = "No Bookings!"
        return render_template('staff/no_queue.html', error=message)
    return render_template('staff/display.html', form=form)


@app.route('/admin_index')
@admin_required
def staff_view():
    return render_template('staff/staff_index.html')


@app.route('/serve', methods=['POST'])
@admin_required
def serve():
    """ Enabling staff to serve clients by removing them from the queue """

    name = request.form.get('name')
    if name in ['Inquiry', 'Admissions', 'Consultation', 'Laboratory', 'Pharmacy']:
        remove(name)
        flash('Client Served')
    return redirect(request.referrer)


@app.route('/admin_logout')
def staff_logout():
    """ Staff logout """
    if is_admin:
        admin_logout()
    return redirect(url_for('staff_login'))


@app.route('/serving/<name>')
@admin_required
def serving(name):

    # Find client ticket using function find defined in helpers
    client_ticket = find(name)
    return render_template('staff/queue_display.html', client_ticket=client_ticket, name=name)


@app.route('/select_section')
@admin_required
def select_section():
    return render_template('staff/serve.html')


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """ Sending users an email with link to reset their passwords """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetRequestForm()
    if form.validate_on_submit():

        # Display the form. and then filter by the email provided to check if it is authentic
        user = User.query.filter_by(email=form.email.data).first()
        if user:

            # Send email to the user
            send_reset_email(user)
        flash('Check your email to reset your password')
        return redirect(url_for('login'))
    return render_template('auth/reset_pass.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """ Checking if users' password reset tokens are valid"""

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # check if the token is valid
    user = User.check_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetForm()

    # If it is, provide users with form to reset their passwords
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('auth/reset_password.html', form=form)