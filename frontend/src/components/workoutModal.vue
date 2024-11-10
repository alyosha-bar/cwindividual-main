<template>
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">Add Workout</button>

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
</template>


<script>

    export default {
        data() {
            return {
                name: "",
                description: "",
                date: "",
                exercises: [],
                allExercises: [],
                searchQuery: "",
                selectedExercises: []
            }
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

                const response = await fetch('http://localhost:8000/api/workouts', requestOptions);

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