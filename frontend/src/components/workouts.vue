<template>
    <div v-if="workouts.length > 0" class="">
        <ul class="d-flex flex-row flex-wrap py-4">
            <li v-for="workout in workouts" :key="workout.workout_id" class="list-group-item border flex-fill m-2 p-4" style="min-width: 250px;">
                <h3>{{ workout.workout_name }}</h3>
                <p>{{ workout.workout_description }}</p>
                <div class="mt-3">
                        <h5 class="text-muted">Exercises</h5>
                        <ul class="list-group mb-3">
                            <li
                                v-for="exercise in workout.exercises"
                                :key="exercise.id"
                                class="list-group-item px-3 py-2"
                            >
                                <div class="d-flex justify-content-between">
                                <div>
                                    <strong>{{ exercise.name }}</strong> - {{ exercise.description }}
                                    <p class="mb-1"><strong>Difficulty:</strong> {{ exercise.difficulty_rating }}</p>
                                    <p class="mb-1"> <strong>Weight:</strong> {{ exercise.weight}}</p>
                                </div>
                                <div>   
                                    <div class="text-end px-4 py-2 rounded hover-effect" @click="openRepsUpdate(workout.workout_id, exercise.id, exercise.name, workout.name)">
                                        <p class="mb-1"><strong>Reps:</strong> {{ exercise.reps }}</p>
                                        <p class="mb-1"><strong>Sets:</strong> {{ exercise.sets }}</p>
                                    </div>
                                    <button @click="deleteExercise(workout.workout_id, exercise.id)" class="w-100 btn btn-danger my-2"> Delete </button>
                                </div>
                                
                                </div>
                            </li>
                            </ul>
                    </div>
                <div class="d-flex align-items-center justify-content-between border p-3 rounded">
                    <div class="d-flex align-items-center justify-content-between w-50">
                        <p class="mb-1"><strong>Date:</strong> {{ new Date(workout.date).toLocaleDateString() }}</p>
                        <span
                        v-if="workout.completed"
                        class="badge bg-success p-2"
                        @click="completed(workout.workout_id)"
                        >
                        Completed
                        </span>
                        <span
                        v-else
                        class="badge bg-danger p-2"
                        @click="completed(workout.workout_id)"
                        >
                        Not Completed
                        </span>
                    </div>
                    <div>
                        <button @click="openUpdateScreen(workout.workout_id, workout.exercises)" class="btn btn-amber btn-sm m-2">Update</button>
                        <button @click="deleteWorkout(workout.workout_id)" class="btn btn-danger btn-sm m-2">Delete</button>
                    </div>  
                </div>
            </li>
        </ul>
    </div>
    <div v-else>
        <p>No workouts available.</p>
    </div>
    <div class="d-flex justify-content-center gap-3 py-3">
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">Add Workout</button>
        <workoutModal
        @createWorkout="createWorkout"></workoutModal>
    </div>
    <workoutUpdate 
        :show="showModal" 
        :id="selectedWorkoutId"
        :selectedExercises="selectedExercises" 
        @close="showModal = false"
        @updateWorkout="updateWorkout"></workoutUpdate>
    <repsUpdate 
        :show="showRepsModal" 
        :workout_id="selectId" 
        :ex_id="exId" 
        :exName="exName"
        :workoutName="workoutName"
        @close="showRepsModal = false"
        @updatePlan="updateReps"></repsUpdate>
</template>

<script>
import workoutUpdate from './workoutUpdate.vue';
import repsUpdate from './repsUpdate.vue';
import workoutModal from './workoutModal.vue';

export default {
    components: {
        workoutUpdate,
        repsUpdate,
        workoutModal
    },
    data() {
        return {
            workouts: [],
            showModal: false,
            selectId: -1,
            showRepsModal: false,
            exId: -1,
            exName: "",
            workoutName: "",
            selectedWorkoutId: null,
            selectedExercises: []
        };
    },
    methods: {
        async completed(id) {
            console.log(`Flipping completed status for id: ${id}`)
            
            const body = {
                "full_flag": false,
                "id": id,
            }

            const requestOptions = {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ body })
            };

            try {
                const response = await fetch('http://localhost:8000/api/workouts', requestOptions);

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();

                console.log("Completed status updated:", data);

                this.workouts.forEach((workout) => {
                    if (workout.workout_id === id) {
                        workout.completed = data.completed;
                    }
                });

                

                return data;
            } catch (error) {
                console.error("Error updating completed status:", error);
            }

        },
        async deleteExercise(workout_id, exercise_id) {
            
            // confirm delete
            const isConfirmed = confirm("Are you sure you want to delete this exercise from this workout?");

            if (!isConfirmed) {
                return   
            }

            console.log(exercise_id)

            const body = {
                workout_id: workout_id,
                exercise_id: exercise_id,
            }


            const requestOptions = {
                method: "DELETE",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({body})
            }

            const response = await fetch('http://localhost:8000/api/plan', requestOptions)

            if (!response.ok) {
                throw new Error("Error Deleting Exercise")
            }

            const data = await response.json()
            this.workouts = data

        },
        openUpdateScreen(id, exercises) {
            this.showModal = true;
            this.selectedWorkoutId = id;
            this.selectedExercises = exercises

            console.log('Opening Update Screen')
            console.log(id, exercises)


        },
        openRepsUpdate(workout_id, exId, exName, workoutName) {
            console.log(workout_id)
            console.log(exId)

            this.selectId = workout_id
            this.exId = exId
            this.exName = exName
            this.workoutName = workoutName
            this.showRepsModal = true
        },
        async deleteWorkout(id) {
            // are you sure dialog
            const isConfirmed = confirm("Are you sure you want to delete this workout?");

            if (!isConfirmed) {
                return   
            }
            
            // send request to server to delete the workout with designated id
            const body = {
                "id": id
            };

            const requestOptions = {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ body })
            };

            const response = await fetch('http://localhost:8000/api/workouts',requestOptions)
            if (!response.ok) {
                throw new Error("Could not delete workout!")
            }
            const data = await response.json()
            this.workouts = data
        },
        async updateWorkout(body, id) {
            console.log("Updating Workout.");
            
            body.id = id

            console.log(body.date)

            // prepare request options
            const requestOptions = {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({body})
            }

            // make fetch request
            const response = await fetch("http://localhost:8000/api/workouts", requestOptions)

            if (!response.ok) {
                throw new Error("Error updating workout")
            }
            
            // close workout update modal
            this.showModal = false;
            
            
            // get workouts as the return
            const data = await response.json()
            const workouts = data.workouts

            // replace workouts array
            this.workouts = workouts
            
            // add to workouts
            return "Workout updated."
        },
        async updateReps(body, workout_id, ex_id) {
            console.log("updating plan")

            console.log(ex_id)
            console.log(workout_id)

            // prepare the body
            body.workout_id = workout_id
            body.exercise_id = ex_id
            
            // prepare the request options
            const requestOptions = {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({body})
            }

            // fetch request
            const response = await fetch("http://localhost:8000/api/plan", requestOptions)

            if (!response.ok) {
                throw new Error("Error occured.")
            }


            const data = await response.json()

            this.workouts = data.workouts

            this.showRepsModal = false
            this.workout_id = null
            this.exercise_id = null
            this.newReps = null
            this.newSets = null
        },
        async createWorkout(body) {
            console.log(body)

            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ body })
            };

            const response = await fetch('http://localhost:8000/api/workouts', requestOptions);

            if (!response.ok) {
                throw new Error("Error occurred.");
            }

            const data = await response.json();
            this.workouts = data

            this.name = "";
            this.description = "";
            this.date = "";
            this.exercises = [];
            this.selectedExercises = [];
        },
    },
    async mounted() {
        try {
            const workoutResponse = await fetch('http://localhost:8000/api/workouts');
            if (!workoutResponse.ok) throw new Error(`HTTP error! status: ${workoutResponse.status}`);
            const workoutData = await workoutResponse.json();
            console.log(workoutData)
            this.workouts = workoutData || [];
        } catch (error) {
            console.error("Error fetching workouts:", error);
        }
    }
}
</script>

<style>
    .btn.btn-amber {
        background-color: #ffca28;
        color: white;
    }

    .btn.btn-amber:hover {
        background-color: #ffb300;
        color: white;
    }

    .hover-effect {
        cursor: pointer;
        transition: background-color 0.2s ease;
    }

    .hover-effect:hover {
        background-color: rgba(0, 123, 255, 0.1); /* Light blue background on hover */
    }


</style>
