<template>
    <div v-if="exercises.length > 0" class="">
        <ul class="d-flex flex-row flex-wrap py-4">
            <div> YO </div>
            <li v-for="exercise in exercises" :key="exercise.id" class="list-group-item border flex-fill m-2 p-4" style="min-width: 250px;">
                <h3>{{ exercise.name }}</h3>
                <p>{{ exercise.description }}</p>
                <div class="d-flex align-items-center justify-content-between border p-3 rounded">
                    <div class="d-flex flex-column">
                        <span
                        v-if="workout.completed"
                        class="badge bg-success p-2"
                        @click="completed(workout.id)"
                        >
                        Completed
                        </span>
                        <span
                        v-else
                        class="badge bg-danger p-2"
                        @click="completed(workout.id)"
                        >
                        Not Completed
                        </span>
                    </div>
                    <div>
                        <button @click="openUpdateScreen(id)" class="btn btn-amber btn-sm m-2">Update</button>
                        <button @click="deleteWorkout(workout.id)" class="btn btn-danger btn-sm m-2">Delete</button>
                    </div>  
                </div>
            </li>
        </ul>
    </div>
    <div v-else>
        <p>No exercises available.</p>
    </div>
</template>

<script>
export default {
    data() {
        return {
            exercises: [],
        };
    },
    methods: {
        async deleteExercise(id) {
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

            const response = await fetch('http://localhost:8000/api/exercises',requestOptions)
            if (!response.ok) {
                throw new Error("Could not delete workout!")
            }
            const message = response.json().message

        }
    },
    async mounted() {
        try {
                const exerciseResponse = await fetch('http://localhost:8000/api/exercises');
                if (!exerciseResponse.ok) {
                    throw new Error(`HTTP error! status: ${exerciseResponse.status}`);
                }
                
                const exerciseData = await exerciseResponse.json();
                console.log(exerciseData)
                this.allExercises = exerciseData.exercises || [];
                console.log(this.allExercises)
            } catch (error) {
                console.error("Error fetching exercises:", error);
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

</style>
