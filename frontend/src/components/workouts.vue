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
    <workoutUpdate 
        :show="showModal" 
        :id="selectedWorkoutId"
        :selectedExercises="selectedExercises" 
        @close="showModal = false"></workoutUpdate>
    <repsUpdate 
        :show="showRepsModal" 
        :workout_id="selectId" 
        :ex_id="exId" 
        :exName="exName"
        :workoutName="workoutName"
        @close="showRepsModal = false"></repsUpdate>
</template>

<script>
import workoutUpdate from './workoutUpdate.vue';
import repsUpdate from './repsUpdate.vue';

export default {
    components: {
        workoutUpdate,
        repsUpdate
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

                // Check if the response is successful (status code 200–299)
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json(); // Parse JSON response

                console.log("Completed status updated:", data);

                this.workouts.forEach((workout) => {
                    if (workout.workout_id === id) {
                        workout.completed = data.completed;
                    }
                });

                

                return data;  // Return the data for further processing if needed
            } catch (error) {
                console.error("Error updating completed status:", error);
                // Handle errors or show error notification to the user if needed
            }

        },
        async deleteExercise(workout_id, exercise_id) {

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

            const message = response.json()
            return message

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
            console.log("Deleting")

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
            const message = response.json().message

        }
    },
    async mounted() {

        // must fetch better --> all workouts with exercises - DONE

        // pass into workoutUpdate as props

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
