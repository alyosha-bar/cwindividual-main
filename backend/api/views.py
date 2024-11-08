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

    if request.method == "GET":
        # Retrieve all workouts
        workouts = Workout.objects.all()
        
        # Build a list to hold workout data
        workout_details = []
        
        # Loop through each workout to collect details
        for workout in workouts:
            # Query Plan to get each exercise linked to this workout
            plans = Plan.objects.filter(workout=workout).select_related('exercise')
            
            # Collect each exercise's details from Plan and Exercise
            exercises_with_details = [
                {
                    "id": plan.exercise.id,
                    "name": plan.exercise.name,
                    "description": plan.exercise.description,
                    "difficulty_rating": plan.exercise.difficuly_rating,
                    "weight": plan.exercise.weight,
                    "reps": plan.reps,
                    "sets": plan.sets
                }
                for plan in plans
            ]
            
            # Add workout data and its exercises to the list
            workout_details.append({
                "workout_id": workout.id,
                "workout_name": workout.name,
                "workout_description": workout.description,
                "date": workout.date.isoformat(),  # Ensure date is JSON serializable
                "completed": workout.completed,
                "exercises": exercises_with_details
            })
        
        # Return JSON response
        return JsonResponse(workout_details, safe=False)

    

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
    
    # need to have a PUT request for two things lol --> marking completed and editing information.
    # make use of flag maybe to differentiate between use cases
    if request.method == "PUT":
        data = json.loads(request.body)
        
        if data["body"].get("full_flag") == False:
            workout_id = data["body"].get("id")
            # Fetch the workout instance by its ID
            workout = get_object_or_404(Workout, id=workout_id)
            
            # Flip the completed status
            workout.completed = not workout.completed
            
            # Save the changes to the database
            workout.save()
            
            # Return a JSON response with the new status
            return JsonResponse({"completed": workout.completed})
        else:
            workout_id = data["body"].get("workoutId")
            name = data["body"].get("name")
            description = data["body"].get("description")
            date_input = data.get("date")
            date = date_input if date_input else None
            exercises = data["body"].get("exercises")

            workout = get_object_or_404(Workout, id=workout_id)

            print(exercises)

            if name != "":
                workout.name = name
                workout.save()
            
            if description != "":
                workout.description = description
                workout.save()

            if date != None:
                workout.date = date
                workout.save()

            
            for exercise in exercises:
                e = get_object_or_404(Exercise, id=exercise['id'])
                plan = Plan.objects.create(workout=workout, exercise=e, reps=10, sets=3)
                plan.save()

            return JsonResponse({
                "Message": "Workout updated."
            })



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

        data = json.loads(request.body)
        exercise_id = data["body"].get("id")

        # delete workout on ID
        exercise = get_object_or_404(Exercise, id=exercise_id)
        exercise.delete()

        return JsonResponse({"message": "Exercise Deleted."})
    

    if request.method == "PUT":
        print("Updating Exercise")
        
        data = json.loads(request.body)
        id = data["body"].get("id")
        name = data["body"].get("name")
        description = data["body"].get("description")
        weight = data["body"].get("weight")
        diff = data["body"].get("difficulty")


        #debug
        print(name)
        print(description)
        print(weight)
        print(diff)



        # fetch exercise with that id.
        exercise = get_object_or_404(Exercise, id=id)

        # update the correct fields --> if empty keep the same?
        if name != "":
            print("changing name.")
            exercise.name = name
            exercise.save()

        if description != "":
            exercise.description = description
            exercise.save()

        if weight != None:
            exercise.weight = weight
            exercise.save()

        if diff != None:
            exercise.difficuly_rating = diff
            exercise.save()

        return JsonResponse({
            "message": "Updated Exercise"
        })
    


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


# move to POST in all workouts
def create_workout(request):
    # get data from req.body
    print("Adding Data.")

    if request.method == "POST":
        data = json.loads(request.body)
        name = data["body"].get("name")
        description = data["body"].get("description")
        date = data["body"].get("date")
        exercises = data["body"].get("exercises") # contains ids of the associated exercises

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


def updatePlan(request):

    if request.method == "GET":
        return JsonResponse({
            "message": "YO"
        })

    if request.method == "PUT":
        # decode body
        data = json.loads(request.body)
        workout_id = data["body"].get("workout_id")
        exercise_id = data["body"].get("exercise_id")
        newReps = data["body"].get("newReps")
        newSets = data["body"].get("newSets")

        # fetch workout by id
        workout = get_object_or_404(Workout, id=workout_id)
        
        #fetch exerise by id
        print(exercise_id)
        exercise = get_object_or_404(Exercise, id=exercise_id)

        # fetch plan
        plan = Plan.objects.get(workout=workout, exercise=exercise)

        if newReps != None:
            plan.reps = newReps
            plan.save()

        if newSets != None:
            plan.sets = newSets
            plan.save()

        return JsonResponse({
            "Message": "Workout Plan Updated."
        })

    if request.method == "DELETE":
        print("Deleting Exercise")
        data = json.loads(request.body)
        workout_id = data["body"].get("workout_id")
        exercise_id = data["body"].get("exercise_id")

        print(workout_id)
        print(exercise_id)

        plan = Plan.objects.filter(workout_id=workout_id, exercise_id=exercise_id)
        plan.delete()

        return JsonResponse({
            "message": "Deleted Successfully."
        })
