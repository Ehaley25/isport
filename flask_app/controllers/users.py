from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.event import Event
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("login.html")

@app.route('/new')
def new_user():
    return render_template('new_user.html')

@app.route('/register',methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
        # if the user hasnt gotten validation send them back so they can register
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        'age':int(request.form['age']),
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    # saves the information into a session and assigns it an id

    return redirect('/home')
    # always redirect when getting information, never render_template
# this route is using the html form and taking in the user inputs
# that we set up a specific way in order for this to work
# every form key matches what we have above, if not we will have PROBLEMS
@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
        # this information is using the post method to get the 
        # email information and to make sure everything is correct
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
        # password information to make sure everything is correct
    session['user_id'] = user.id
    return redirect('/home')
    # if correct send them to the dashboard
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/logout')
    # no session? go back and sign in 
    data ={
        'id': session['user_id']
    }
    return render_template("home.html",user=User.get_by_id(data),events=Event.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
# log out redirecct link