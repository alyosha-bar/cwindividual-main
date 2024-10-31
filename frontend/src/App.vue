<template>
    <div class="container pt-3">
        <div class="h1 text-center border rounded bg-light p-4 mb-3">
            Workout Buddy
        </div>
        <div class="mb-3">
            <h2>Workout List</h2>             
        </div>
        
        <div v-if="workouts.length > 0" class="">
            <ul class="d-flex flex-row flex-wrap py-4">
                <li v-for="workout in workouts" :key="workout.id" class="list-group-item border flex-fill m-2 p-4" style="min-width: 250px;">
                    <h3>{{ workout.name }}</h3>
                    <p>{{ workout.description }}</p>
                    <p><strong>Date:</strong> {{ new Date(workout.date).toLocaleDateString() }}</p>
                </li>
            </ul>
        </div>
        <div v-else>
            <p>No workouts available.</p>
        </div>

        <!-- Button trigger modal -->
        <div class="d-flex justify-content-center gap-3 py-3">
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exerciseModal">
            Add Exercise
            </button>
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">Add Workout</button>
        </div>

        <!-- Workout Modal -->
        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Add Workout </h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="createWorkout" class="container p-4 border rounded shadow-sm">
                        <div class="mb-3">
                            <label for="name" class="form-label">Name:</label>
                            <input v-model="name" type="text" name="name" class="form-control" placeholder="Enter workout name" required>
                        </div>
                        <div class="mb-3">
                            <label for="desc" class="form-label">Description:</label>
                            <textarea v-model="description" name="desc" class="form-control" rows="3" placeholder="Enter workout description" required></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="date" class="form-label">Date:</label>
                            <input v-model="date" type="date" name="date" class="form-control" required>
                        </div>
                       <!-- Exercise Search and Selection -->
                            <div class="mb-3">
                                <label class="form-label">Search Exercises:</label>
                                <input
                                    v-model="searchQuery"
                                    type="text"
                                    class="form-control"
                                    placeholder="Search exercises"
                                />
                            </div>

                            <!-- Filtered Exercises List -->
                            <ul class="list-group mb-3">
                                <li
                                    v-for="exercise in filteredExercises"
                                    :key="exercise.id"
                                    class="list-group-item d-flex justify-content-between align-items-center"
                                >
                                    {{ exercise.name }}
                                    <button
                                        type="button"
                                        class="btn btn-sm btn-outline-primary"
                                        @click="addExercise(exercise)"
                                    >
                                        Add
                                    </button>
                                </li>
                            </ul>

                            <!-- Selected Exercises List -->
                            <div class="mb-3">
                                <label class="form-label">Selected Exercises:</label>
                                <ul class="list-group">
                                    <li
                                        v-for="exercise in selectedExercises"
                                        :key="exercise.id"
                                        class="list-group-item d-flex justify-content-between align-items-center"
                                    >
                                        {{ exercise.name }}
                                        <button
                                            type="button"
                                            class="btn btn-sm btn-outline-danger"
                                            @click="removeExercise(exercise.id)"
                                        >
                                            Remove
                                        </button>
                                    </li>
                                </ul>
                            </div>
                        <button type="submit" class="btn btn-primary w-100">Add Workout</button>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
                </div>
            </div>
        </div>
        
        <!-- Exercise Modal -->
        <div class="modal fade" id="exerciseModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="exampleModalLabel">Add Exercise </h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <form @submit.prevent="createExercise" class="container p-4 border rounded shadow-sm">
                    <div class="mb-3">
                        <label for="name" class="form-label">Name:</label>
                        <input v-model="exName" type="text" name="name" class="form-control" placeholder="Enter exercise name" required>
                    </div>
                    <div class="mb-3">
                        <label for="desc" class="form-label">Description:</label>
                        <textarea v-model="exDesc" name="desc" class="form-control" rows="3" placeholder="Enter exercise description" required></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="weight" class="form-label">Weight:</label>
                        <input v-model="exWeight" type="number" name="weight" class="form-control" placeholder="0 (bodyweight)" required>
                    </div>
                    <div class="mb-3">
                        <label for="difficulty" class="form-label">Difficulty:</label>
                        <input v-model="exDiff" type="number" name="difficulty" class="form-control" placeholder="1, 2, or 3" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Add Exercise</button>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            </div>
            </div>
        </div>
        </div>

    </div>
</template>
  
<script>
export default {
    data() {
        return {
            name: "",
            description: "",
            date: "",
            exercises: [], // Ensure exercises remains an array
            exName: "",
            exDesc: "",
            exWeight: undefined,
            exDiff: undefined,
            allExercises: [],
            workouts: [],
            searchQuery: "",
            selectedExercises: []
        };
    },
    computed: {
        filteredExercises() {
            return this.allExercises.filter(exercise =>
                exercise.name.toLowerCase().includes(this.searchQuery.toLowerCase())
            );
        },
    },
    methods: {
        handleExerciseAdded(exercise) {
            // Handle the new exercise data
            console.log("Exercise Added:", exercise);
            // For example, add it to a list of exercises or send it to the server
        },
        addExercise(exercise) {
            if (!this.exercises.includes(exercise.id)) {
                this.exercises.push(exercise.id);
                this.selectedExercises.push(exercise);
            }
        },
        removeExercise(exerciseId) {
            this.exercises = this.exercises.filter(id => id !== exerciseId);
            this.selectedExercises = this.selectedExercises.filter(ex => ex.id !== exerciseId);
        },
        async createWorkout() {
            const body = {
                name: this.name,
                description: this.description,
                date: this.date,
                exercises: this.exercises
            };

            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ body })
            };

            const response = await fetch('http://localhost:8000/api/addworkout', requestOptions);

            if (!response.ok) {
                throw new Error("Error occurred.");
            }

            await response.json();
            this.name = "";
            this.description = "";
            this.date = "";
            this.exercises = [];
            this.selectedExercises = [];
        },
        async createExercise() {
            const body = {
                name: this.exName,
                description: this.exDesc,
                weight: this.exWeight,
                difficulty: this.exDiff
            };

            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ body })
            };

            const response = await fetch('http://localhost:8000/api/addexercise', requestOptions);

            if (!response.ok) {
                throw new Error("Error occurred.");
            }

            await response.json();
            this.exName = "";
            this.exDesc = "";
            this.exWeight = undefined;
            this.exDiff = undefined;
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

        try {
            const exerciseResponse = await fetch('http://localhost:8000/api/exercises');
            if (!exerciseResponse.ok) throw new Error(`HTTP error! status: ${exerciseResponse.status}`);
            const exerciseData = await exerciseResponse.json();
            this.allExercises = exerciseData.exercises || [];
        } catch (error) {
            console.error("Error fetching exercises:", error);
        }
    }
};
</script>
