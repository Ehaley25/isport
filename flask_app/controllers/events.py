from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.event import Event
from flask_app.models.user import User


@app.route('/new/event')
def new_event():
    if 'user_id' not in session:
        return redirect('/logout') 
    data = {
        "id":session['user_id']
    }
    return render_template('new.html',user=User.get_by_id(data))

@app.route('/create/event',methods=['POST'])
def create_event():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Event.validate_event(request.form):
        return redirect('/new/event')
    data = {
        "event_name": request.form["event_name"],
        "location": request.form["location"],
        "description": request.form['description'],
        "attendees": int(request.form["attendees"]),
        "date": request.form["date"],
        "user_id":session["user_id"]
    }
    Event.save(data)
    return redirect('/home')
@app.route('/edit/event/<int:id>')
def edit_event(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_event.html",edit=Event.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/event',methods=['POST'])
def update_event():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Event.validate_event(request.form):
        return redirect('/new/event')
    data = {
        "event_name": request.form["event_name"],
        "location": request.form["location"],
        "description": request.form["description"],
        "attendees": int(request.form["attendees"]),
        "date": request.form["date"],
        'id' :request.form['id']
    }
    Event.update(data)
    return redirect('/home')

@app.route('/event/<int:id>')
def show_event(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("view_one.html",event=Event.get_one(data),user=User.get_by_id(user_data))

@app.route('/destroy/event/<int:id>')
def destroy_event(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Event.destroy(data)
    return redirect('/home')

@app.errorhandler(404)
def error(incorrect):
    return render_template("error.html")