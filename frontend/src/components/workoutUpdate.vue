<template>
    <div v-if="show" class="modal fade show d-block" style="background-color: rgba(0, 0, 0, 0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title"> Update Workout </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateWorkout" class="container p-4 border rounded shadow-sm">
                        <div class="mb-3">
                            <label for="name" class="form-label">Name:</label>
                            <input v-model="name" type="text" name="name" class="form-control" placeholder="Enter workout name">
                        </div>
                        <div class="mb-3">
                            <label for="desc" class="form-label">Description:</label>
                            <textarea v-model="description" name="desc" class="form-control" rows="3" placeholder="Enter workout description"></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="date" class="form-label">Date:</label>
                            <input v-model="date" type="date" name="date" class="form-control">
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
            <button @click="console.log(id)"> Show ID </button>
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
            // selected exercises has to be already those in the workout --> thus removing them is editing the workout that way
            selectedExercises: []
        }
    },  
    props: {
      show: {
        type: Boolean,
        required: true,
      },
      id: {
        type: Number,
        required: true
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
      closeModal() {
        // Emit a close event to notify the parent to hide the modal
        this.$emit("close");
      },
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
        updateWorkout(id) {
            console.log("Updating Workout.")

            // prep body

            // prep request options


            // make fetch request


            // handle response


            // reset values


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
  };
  </script>
  
  <style scoped>
  .modal.fade.show {
    display: block;
  }
  </style>
  