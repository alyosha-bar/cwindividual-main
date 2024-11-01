<template>
    <div v-if="workouts.length > 0" class="">
        <ul class="d-flex flex-row flex-wrap py-4">
            <li v-for="workout in workouts"  :key="workout.id" class="list-group-item border flex-fill m-2 p-4" style="min-width: 250px;">
                <h3>{{ workout.name }}</h3>
                <p>{{ workout.description }}</p>
                <div class="d-flex align-items-center justify-content-between border p-3 rounded">
                    <div class="d-flex flex-column">
                        <p class="mb-1"><strong>Date:</strong> {{ new Date(workout.date).toLocaleDateString() }}</p>
                        <span class="badge bg-success p-2">Completed: true</span>
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
        <p>No workouts available.</p>
    </div>
</template>

<script>
export default {
    data() {
        return {
            workouts: [],
        };
    },
    methods: {
        openUpdateScreen(id) {
            console.log("Opening Update Screen.")
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
                    id: id
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
        try {
            const workoutResponse = await fetch('http://localhost:8000/api/workouts');
            if (!workoutResponse.ok) throw new Error(`HTTP error! status: ${workoutResponse.status}`);
            const workoutData = await workoutResponse.json();
            this.workouts = workoutData.workouts || [];
        } catch (error) {
            console.error("Error fetching workouts:", error);
        }
    }
}
</script>

<style>
    /* .btn-amber {
        background-color: #ffca28 !important;
        color: white !important;
    }

    .btn-amber:hover {
        background-color: #ffb300 !important;
        color: white !important;
    } */

    .btn.btn-amber {
  background-color: #ffca28;
  color: white;
}

.btn.btn-amber:hover {
  background-color: #ffb300;
  color: white;
}

</style>
