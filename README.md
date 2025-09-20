# Personal Trainer's Workout API
Use this API to keep track of individual workouts and exercises done.  

## Installation
Use pipenv to install required packages
```bash
pipenv install
pipenv shell
```

Change into the `server` directory and configure the `FLASK_APP` and `FLASK_RUN_PORT` environment variables:
```bash
$ cd server
$ export FLASK_APP=app.py
$ export FLASK_RUN_PORT=5555
```

Initialize the database
```bash
flask db init
flask db migrate -m 'message about your migration here'
flask db upgrade head
```

Run `python app.py` from the `server` directory

## Usage
The following endpoints are available for retrieving data, adding workouts or exercises, or deleting workouts/exercises:
* GET /workouts
  * List all workouts
* GET /workouts/<id>
  * Show a single workout with its associated exercises and reps/sets/duration
* POST /workouts
  * Create a workout
* DELETE /workouts/<id>
  * Delete a workout (and associated data)
* GET /exercises
  * List all exercises
* GET /exercises/<id>
  * Show an exercise and associated workouts
* POST /exercises
  * Create an exercise
* DELETE /exercises/<id>
  * Delete an exercise (and associated data)
* POST workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
  * Add an exercise to a workout, including reps/sets/duration
 
## Notes for grader
I feel like I'm returning too much data from the serialization schema, and that prevented me from using the WorkoutExerciseSchema in the final endpoint.  I'd like feedback on this if possible.
