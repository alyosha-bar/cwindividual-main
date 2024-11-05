<template>
    <div v-if="exercises.length > 0" class="py-4">
        <ul class="d-flex flex-row flex-wrap">
        <li
            v-for="exercise in exercises"
            :key="exercise.id"
            class="list-group-item border rounded flex-fill m-2 p-3 d-flex flex-column justify-content-between"
            style="min-width: 200px; max-width: 250px;"
        >
            <div>
            <h5 class="mb-1 py-2">{{ exercise.name }}</h5>
            <p class="small text-muted py-2">{{ exercise.description }}</p>
            </div>
            
            <div class="d-flex justify-content-around">
            <button
                @click="openUpdateScreen(exercise.id)"
                class="btn btn-sm btn-amber"
            >
                Update
            </button>
            <button
                @click="deleteExercise(exercise.id)"
                class="btn btn-danger btn-sm"
            >
                Delete
            </button>
            </div>
        </li>
        </ul>
        </div>
        <div v-else>
        <p>No exercises available.</p>
    </div>
    <exerciseUpdate :show="showModal" :id="selectedId" @close="showModal = false"></exerciseUpdate>
</template>

<script>
import exerciseUpdate from './exerciseUpdate.vue';

export default {
    components: {
        exerciseUpdate
    },
    data() {
        return {
            exercises: [],
            isConfirmed: false,
            showModal: false,
            selectedId: -1,
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

        },
        openUpdateScreen(id) {
            this.showModal = true;
            this.selectedId = id;
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
            this.exercises = exerciseData.exercises || [];
            console.log("YO")
            console.log(this.exercises)
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
