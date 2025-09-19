from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import CheckConstraint
from marshmallow import Schema, fields

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')

    workouts = association_proxy('workout_exercises', 'workout', creator=lambda workout_obj: WorkoutExercise(workout=workout_obj))

    @validates('category')
    def validate_category(self, key, value):
        if value not in ["Aerobic", "Strength", "Flexibility", "Balance", "Other"]:
            raise ValueError('Category must be one of: "Aerobic", "Strength", "Flexibility", "Balance", "Other"')
        return value
    
    def __repr__(self):
        return f'<Exercise {self.id} {self.name} {self.category} equip={self.equipment_needed}>'
    
class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String()
    category = fields.String()
    equipment_needed = fields.Boolean()

    workout_exercises = fields.List(fields.Nested(lambda: WorkoutExerciseSchema(exclude=('exercise',))))
    workouts = fields.List(fields.Nested(lambda: WorkoutSchema(exclude=('workout_exercises', 'exercises'))))

class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, db.CheckConstraint("duration_minutes < 1440")) # Constraint: duration is less than one day
    notes = db.Column(db.Text)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')

    exercises = association_proxy('workout_exercises', 'exercise', creator=lambda exercise_obj: WorkoutExercise(exercise=exercise_obj))

    def __repr__(self):
        return f'<Workout {self.id} {self.date} {self.duration_minutes} {self.notes}>'

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.DateTime()
    duration_minutes = fields.Int()
    notes = fields.String()

    workout_exercises = fields.List(fields.Nested(lambda: WorkoutExerciseSchema(exclude=('workout',))))
    exercises = fields.List(fields.Nested(lambda: ExerciseSchema(exclude=('workout_exercises', 'workouts'))))

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')
    
    @validates('reps', 'sets', 'duration_seconds')
    def validate_summary(self, key, value):
        if value <= 0:
            raise ValueError("Reps, sets, and duration must be greater than 0")
        return value
    
    def __repr__(self):
        return f'<WorkoutExercise {self.id} reps={self.reps} sets={self.sets} {self.duration_seconds}>'
    
class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()

    workout = fields.Nested(WorkoutSchema(exclude=("workout_exercises",)))
    exercise = fields.Nested(ExerciseSchema(exclude=("workout_exercises",)))