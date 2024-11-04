from django.shortcuts import render
from django.http import JsonResponse
from .models import Plan, Workout, Exercise
import json
from django.shortcuts import get_object_or_404

def test_api_view(request):
    return JsonResponse({
        'message': 'Good response!'
    })


def all_workouts(request):
    # Query all workouts
    # workouts = Workout.objects.all()

    # # Serialize workouts into a list of dictionaries
    # workouts_data = []
    # for workout in workouts:
    #     # Gather the exercises associated with each workout
    #     exercises_data = []
    #     plans = Plan.objects.filter(workout=workout)  # Get all plans for the current workout

    #     for plan in plans:
    #         exercises_data.append({
    #             "exercise_id": plan.exercise.id,
    #             "exercise_name": plan.exercise.name,
    #             "exercise_description": plan.exercise.description,
    #             "difficulty_rating": plan.exercise.difficuly_rating,
    #             "weight": plan.exercise.weight,
    #             "reps": plan.reps,
    #             "sets": plan.sets,
    #         })

    #     workouts_data.append({
    #         "id": workout.id,
    #         "name": workout.name,
    #         "description": workout.description,
    #         "date": workout.date.strftime("%Y-%m-%d"),  # Convert date to string
    #         "exercises": exercises_data
    #     })
    if request.method == "GET":
        workouts = Workout.objects.all()

        workout_data = [{
                "id": workout.id,
                "name": workout.name,
                "description": workout.description,
                "date": workout.date,
                "completed": workout.completed
            }
            for workout in workouts
        ]

        # Return serialized data as JSON
        return JsonResponse({
            "workouts": workout_data
        })
    if request.method == "DELETE":
        print("Deleting workout")

        data = json.loads(request.body)
        workout_id = data["body"].get("id")

        # delete workout on ID
        workout = get_object_or_404(Workout, id=workout_id)
        workout.delete()

        return JsonResponse({
            "message": "Deleted Workout."
        })
    if request.method == "PUT":
        data = json.loads(request.body)
        

        workout_id = data["body"].get("id")
        # Fetch the workout instance by its ID
        workout = get_object_or_404(Workout, id=workout_id)
        
        # Flip the completed status
        workout.completed = not workout.completed
        
        # Save the changes to the database
        workout.save()
        
        # Return a JSON response with the new status
        return JsonResponse({"completed": workout.completed})



def all_exercises(request):
    if request.method == "GET":
        exercises = Exercise.objects.all()
        exercise_data = [
            {
                "id": ex.id, 
                "name": ex.name,
                "description": ex.description,
                "weight": ex.weight,
                "level": ex.difficuly_rating
                } 
            for ex in exercises]
        return JsonResponse({"exercises": exercise_data})
    

    
    if request.method == "DELETE":
        print("Deleting Exercise")
        return
    if request.method == "PUT":
        print("Updating Exercise")
        return
    if request.method == "POST":
        data = json.loads(request.body)
        name = data["body"].get("name")
        description = data["body"].get("description")
        weight = data["body"].get("weight")
        diff = data["body"].get("difficulty")

        # add into db - exercises model
        exercise = Exercise(name=name, description=description, weight=weight, difficuly_rating=Exercise.DifficultyLevel.MEDIUM)
        exercise.save()
        return JsonResponse({
            "message": "exercise added."
        })


def create_workout(request):
    # get data from req.body
    print("Adding Data.")

    if request.method == "POST":
        data = json.loads(request.body)
        name = data["body"].get("name")
        description = data["body"].get("description")
        date = data["body"].get("date")
        exercises = data["body"].get("exercises") # contains ids of the associated exercises

        # still need a way to make the reps and sets FOR EACH EXERCISE

    print(name)
    print(description)
    print(date)
    print(exercises)

    # add into db

    # create new Workout model
    workout = Workout.objects.create(name=name, description=description, date=date)
    # create new plan for every exercise
    # loop through exercise,
        # find the exercise corresponing to id
        # use it to create a membership
        # add default values for reps and sets
    defaultReps=10
    defaultSets=3
    for id in exercises:
        exercise = get_object_or_404(Exercise, id=id)
        plan = Plan.objects.create(exercise=exercise, workout=workout, reps=defaultReps, sets=defaultSets)
        plan.save()


    return JsonResponse({
        "message": "sup dude"
    })
