from flask import Flask, make_response
from flask_migrate import Migrate

from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/workouts')
def get_workouts():
    pass

@app.route('/workouts/<int:id>')
def get_workout_by_id(id):
    pass

@app.route('/workouts', methods=['POST'])
def add_workout():
    pass

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    pass

@app.route('/exercises')
def get_exercises():
    pass

@app.route('/exercises/<int:id>')
def get_exercise_by_id(id):
    pass

@app.route('/exercises', methods=['POST'])
def add_exercise():
    pass

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    pass

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    pass

if __name__ == '__main__':
    app.run(port=5555, debug=True)