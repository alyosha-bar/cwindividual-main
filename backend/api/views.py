from django.shortcuts import render
from django.http import JsonResponse
from .models import Plan, Workout, Exercise
from datetime import datetime
import json
from django.shortcuts import get_object_or_404
from .utils import get_all_exercises, get_all_workouts

def all_workouts(request):
    """
    This is a view function for the /api/workouts route.
    It handles all requests based on the request.method.
    """

    if request.method == "GET":
        # get all workouts
        workouts = Workout.objects.all()
        
        # use the util function
        workout_details = get_all_workouts(workouts)
        
        return JsonResponse(workout_details, safe=False)

    if request.method == "POST":
        # get data from req.body
        print("Adding Data.")

        data = json.loads(request.body)
        name = data["body"].get("name")
        description = data["body"].get("description")
        date = data["body"].get("date")
        exercises = data["body"].get("selectedExercises")

        print(name)
        print(description)
        print(date)
        print(exercises)

        # add into db

        # create new Workout model
        workout = Workout.objects.create(name=name, description=description, date=date)
        defaultReps=10
        defaultSets=3
        for ex in exercises:
            exercise = get_object_or_404(Exercise, id=ex.get('id'))
            plan = Plan.objects.create(exercise=exercise, workout=workout, reps=defaultReps, sets=defaultSets)
            plan.save()

        workouts = Workout.objects.all()
        workout_details = get_all_workouts(workouts)

        return JsonResponse(workout_details, safe=False)    

    if request.method == "DELETE":
        print("Deleting workout")

        data = json.loads(request.body)
        workout_id = data["body"].get("id")

        # delete workout on ID
        workout = get_object_or_404(Workout, id=workout_id)
        workout.delete()

        workouts = Workout.objects.all()
        workout_details = get_all_workouts(workouts)


        return JsonResponse(workout_details, safe=False)
    
    if request.method == "PUT":
        data = json.loads(request.body)
        
        print(data)

        if data["body"].get("full_flag") == False:
            workout_id = data["body"].get("id")
            # get specific workout
            workout = get_object_or_404(Workout, id=workout_id)
            
            # flip the completed status boolean value
            workout.completed = not workout.completed
            workout.save()

            # return new status for reactivity
            return JsonResponse({"completed": workout.completed})
        else:
            workout_id = data["body"].get("id")
            name = data["body"].get("name")
            description = data["body"].get("description")
            date_str = data["body"].get("date") 

            workout = get_object_or_404(Workout, id=workout_id)

            if name != "":
                workout.name = name
                workout.save()
            
            if description != "":
                workout.description = description
                workout.save()

            workouts = Workout.objects.all()
            workout_details = get_all_workouts(workouts)

            return JsonResponse({
                "workouts": workout_details
            })

def all_exercises(request):
    """
    This is a view function for the /api/exercises route.
    It handles all requests based on the request.method.
    """
    
    if request.method == "GET":
        print("Here.")
        exercises = Exercise.objects.all()

        exercise_data = get_all_exercises(exercises)

        return JsonResponse(exercise_data, safe=False)
     
    if request.method == "DELETE":
        print("Deleting Exercise")

        data = json.loads(request.body)
        exercise_id = data["body"].get("id")

        # delete workout on ID
        exercise = get_object_or_404(Exercise, id=exercise_id)
        exercise.delete()

        exercises = Exercise.objects.all()
        exercise_data = get_all_exercises(exercises)

        return JsonResponse(exercise_data, safe=False)
    
    if request.method == "PUT":
        print("Updating Exercise")
        
        data = json.loads(request.body)
        id = data["body"].get("id")
        name = data["body"].get("exName")
        description = data["body"].get("exDesc")
        weight = data["body"].get("exWeight")
        diff = data["body"].get("exDiff")


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


        # return all exercises
        exercises = Exercise.objects.all()
        exercise_data = get_all_exercises(exercises)

        return JsonResponse(exercise_data, safe=False)
    
    if request.method == "POST":
        data = json.loads(request.body)
        name = data["body"].get("exName")
        description = data["body"].get("exDesc")
        weight = data["body"].get("exWeight")
        diff = data["body"].get("exDiff")

        # add into db - exercises model
        exercise = Exercise(name=name, description=description, weight=weight, difficuly_rating=Exercise.DifficultyLevel.MEDIUM)
        exercise.save()


        # return all exercises
        exercises = Exercise.objects.all()
        exercise_data = get_all_exercises(exercises)

        return JsonResponse(exercise_data, safe=False)

def update_plan(request):
    """
    This is a view function for the /api/plan route.
    It handles all requests based on the request.method.
    """

    if request.method == "PUT":
        # decode body
        data = json.loads(request.body)
        rs_flag = data['body'].get('rs_flag')

        if rs_flag == True:
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

            workouts = Workout.objects.all()
            workout_details = get_all_workouts(workouts)

            return JsonResponse({
                "workouts": workout_details
            })
        else:
            # adding an exercise into a workout
            exercise_id = data["body"].get("exercise_id")
            workouts = data["body"].get("workouts")

            print(exercise_id)
            print(workouts)

            defaultReps=10
            defaultSets=3

            # fetch exercise by id
            exercise = get_object_or_404(Exercise, id=exercise_id)

            # add to all workout ids in the workouts list
            # add by making a plan object and saving that
            for workout in workouts:
                w = get_object_or_404(Workout, id=workout['workout_id'])
                plan = Plan.objects.create(workout=w, exercise=exercise, reps=defaultReps, sets=defaultSets)
                plan.save()

            workouts = Workout.objects.all()
            workout_details = get_all_workouts(workouts)

            return JsonResponse({
                "workouts": workout_details
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

        workouts = Workout.objects.all()
        workout_details = get_all_workouts(workouts)

        return JsonResponse(workout_details, safe=False)