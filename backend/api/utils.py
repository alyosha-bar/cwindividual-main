from .models import Plan, Workout, Exercise

def get_all_workouts(workouts):
    """ 
    This is a utility function to help get workout data
    in bulk.
    """
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
            "date": workout.date.isoformat(),
            "completed": workout.completed,
            "exercises": exercises_with_details
        })

    return workout_details

def get_all_exercises(exercises):
    """ 
    This is a utility function to help get exercise data
    in bulk.
    """
    exercise_data = [
    {
        "id": ex.id, 
        "name": ex.name,
        "description": ex.description,
        "weight": ex.weight,
        "level": ex.difficuly_rating
        } 
    for ex in exercises]

    return exercise_data
