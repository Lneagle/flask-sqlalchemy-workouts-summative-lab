from flask import Flask, make_response, request
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/workouts')
def get_workouts():
    return make_response(WorkoutSchema(many=True).dump(Workout.query.all()), 200)

@app.route('/workouts/<int:id>')
def get_workout_by_id(id):
    workout = Workout.query.filter_by(id=id).first()
    if workout:
        return make_response(WorkoutSchema().dump(workout), 200)
    else:
        return make_response({'message': f'Workout {id} not found'}, 404)

@app.route('/workouts', methods=['POST'])
def add_workout():
    data = request.json
    new_workout = WorkoutSchema().load(data)
    db.session.add(new_workout)
    db.session.commit()
    return make_response({'message': 'Workout created'}, 201)

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.filter_by(id=id).first()
    if workout:
        db.session.delete(workout)
        db.session.commit()
        return make_response({'message': f'Workout {id} deleted'}, 200)
    else:
        return make_response({'message': f'Workout {id} not found'}, 404)

@app.route('/exercises')
def get_exercises():
    return make_response(ExerciseSchema(many=True).dump(Exercise.query.all()), 200)

@app.route('/exercises/<int:id>')
def get_exercise_by_id(id):
    exercise = Exercise.query.filter_by(id=id).first()
    if exercise:
        return make_response(ExerciseSchema().dump(exercise), 200)
    else:
        return make_response({'message': f'Exercise {id} not found'}, 404)

@app.route('/exercises', methods=['POST'])
def add_exercise():
    data = request.json
    new_exercise = ExerciseSchema().load(data)
    db.session.add(new_exercise)
    db.session.commit()
    return make_response({'message': 'Exercise created'}, 201)

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.filter_by(id=id).first()
    if exercise:
        db.session.delete(exercise)
        db.session.commit()
        return make_response({'message': f'Exercise {id} deleted'}, 200)
    else:
        return make_response({'message': f'Exercise {id} not found'}, 404)

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.filter_by(id=workout_id).first()
    exercise = Exercise.query.filter_by(id=exercise_id).first()

    if not workout:
        return make_response({'message': f'Workout {workout_id} not found'}, 404)
    if not exercise:
        return make_response({'message': f'Exercise {exercise_id} not found'}, 404)
    
    data = request.json
    # Can't get this part to work yet
    # we_data = {"reps": data["reps"], "sets": data["sets"], "duration_seconds": data["duration_seconds"], "workout": WorkoutSchema().dump(workout), "exercise": ExerciseSchema().dump(exercise)}
    # new_workout_exercise = WorkoutExerciseSchema().load(we_data)
    new_workout_exercise = WorkoutExercise(reps=data["reps"], sets=data["sets"], duration_seconds=data["duration_seconds"], workout=workout, exercise=exercise)

    db.session.add(new_workout_exercise)
    db.session.commit()
    return make_response({'message': f'Exercise {exercise_id} added to workout {workout_id}'}, 201)

if __name__ == '__main__':
    app.run(port=5555, debug=True)