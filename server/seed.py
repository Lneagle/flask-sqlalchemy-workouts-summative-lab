#!/usr/bin/env python3

from app import app
from models import *

import datetime
from random import choice as rc, randint
from faker import Faker

fake = Faker()

with app.app_context():
    # Delete data
    Exercise.query.delete()
    Workout.query.delete()
    WorkoutExercise.query.delete()

    categories = ["Aerobic", "Strength", "Flexibility", "Balance", "Other"]

    # Add exercises
    e1 = Exercise(name="Running", category="Aerobic", equipment_needed=False)
    e2 = Exercise(name="Bench Press", category="Strength", equipment_needed=True)
    e3 = Exercise(name="Sideways Bend", category="Flexibility", equipment_needed=False)
    e4 = Exercise(name="Single Leg Balance", category="Balance", equipment_needed=False)
    e5 = Exercise(name="Boxing", category="Other", equipment_needed=True)
    db.session.add_all([e1, e2, e3, e4, e5])
    db.session.commit()

    # Add workouts
    w1 = Workout(date=datetime.datetime(2025, 5, 17), duration_minutes=randint(5, 60), notes=fake.text())
    w2 = Workout(date=datetime.datetime(2025, 6, 3), duration_minutes=randint(5, 60), notes=fake.text())
    w3 = Workout(date=datetime.datetime(2025, 6, 20), duration_minutes=randint(5, 60), notes=fake.text())
    w4 = Workout(date=datetime.datetime(2025, 7, 12), duration_minutes=randint(5, 60), notes=fake.text())
    db.session.add_all([w1, w2, w3, w4])
    db.session.commit()

    # Add workout_exercises
    we1 = WorkoutExercise(reps=randint(1, 20), sets=randint(1, 10), duration_seconds=randint(30, 600), workout=w3, exercise=e5)
    we2 = WorkoutExercise(reps=randint(1, 20), sets=randint(1, 10), duration_seconds=randint(30, 600), workout=w1, exercise=e4)
    we3 = WorkoutExercise(reps=randint(1, 20), sets=randint(1, 10), duration_seconds=randint(30, 600), workout=w4, exercise=e3)
    we4 = WorkoutExercise(reps=randint(1, 20), sets=randint(1, 10), duration_seconds=randint(30, 600), workout=w2, exercise=e2)
    we5 = WorkoutExercise(reps=randint(1, 20), sets=randint(1, 10), duration_seconds=randint(30, 600), workout=w3, exercise=e1)
    we6 = WorkoutExercise(reps=randint(1, 20), sets=randint(1, 10), duration_seconds=randint(30, 600), workout=w3, exercise=e3)
    we7 = WorkoutExercise(reps=randint(1, 20), sets=randint(1, 10), duration_seconds=randint(30, 600), workout=w2, exercise=e4)
    we8 = WorkoutExercise(reps=randint(1, 20), sets=randint(1, 10), duration_seconds=randint(30, 600), workout=w1, exercise=e5)
    db.session.add_all([we1, we2, we3, we4, we5, we6, we7, we8])
    db.session.commit()