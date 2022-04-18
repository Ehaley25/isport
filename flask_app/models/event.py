from calendar import c
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Event:
    db_name = 'isports'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.event_name = db_data['event_name']
        self.location = db_data['location']
        self.attendees = db_data['attendees']
        self.description = db_data['description']
        self.date = db_data['date']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def save(cls,data):
        query = "insert into events (event_name , location , attendees,description, date , user_id) values( %(event_name)s, %(location)s , %(attendees)s,%(description)s, %(date)s ,%(user_id)s)"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "Select * from events"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_events = []
        for row in results:
            print(row['date'])
            all_events.append(cls(row))
        return all_events

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM events WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def update(cls, data):
        query = "UPDATE events SET event_name=%(event_name)s,location=%(location)s, attendees=%(attendees)s, description=%(description)s,date=%(date)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM events WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_event(event):
        is_valid = True
        if len(event['event_name']) < 3:
            is_valid = False
            flash("Event name has to be longer than three characters" , "event")
        if len(event['location']) < 3:
            is_valid = False
            flash("The location needs to be at least 3 characters long","event")
        if int(event['attendees']) < 1:
            is_valid = False
            flash("Please provide at least 1 person to attend the event" , 'event')
        return is_valid