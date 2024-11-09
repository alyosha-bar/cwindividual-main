<template>
    <div v-if="show" class="modal fade show d-block" style="background-color: rgba(0, 0, 0, 0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Modal Title</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addToWorkout" class="container p-4 border rounded shadow-sm">   
            <div>
                <h3>All Workouts</h3>
                <ul class="list-group mb-3">
                    <li v-for="(workout, index) in workouts" :key="index" class="list-group-item d-flex justify-content-between align-items-center">
                    {{ workout.workout_name }}
                    <button @click="addWorkout(workout)" :disabled="selectedWorkouts.includes(workout)" class="btn btn-sm btn-outline-primary">
                        Add
                    </button>
                    </li>
                </ul>
                </div>

                <!-- Display selected workouts -->
                <div>
                <h3>Selected Workouts</h3>
                <ul class="list-group mb-3">
                    <li v-for="(workout, index) in selectedWorkouts" :key="index" class="list-group-item d-flex justify-content-between align-items-center">
                    {{ workout.workout_name }}
                    <button @click="removeWorkout(workout)" class="btn btn-sm btn-outline-danger">
                        Remove
                    </button>
                    </li>
                </ul>
            </div>
            <button type="submit" class="btn btn-primary w-100">Update Exercise</button>
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
            selectedWorkouts: [],
            searchQuery: "",
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
      },
      workouts: {
        type: Array,
        required: true
      }
    },
    methods: {
        addWorkout(workout) {
            // Add workout to selectedWorkouts if it isn't already added
            if (!this.selectedWorkouts.includes(workout)) {
                this.selectedWorkouts.push(workout);
            }
        },
        removeWorkout(workout) {
            // Remove workout from selectedWorkouts
            this.selectedWorkouts = this.selectedWorkouts.filter(
                (w) => w !== workout
            );
        },
      closeModal() {
        this.$emit("close");
      },
      async addToWorkout() {
        // prepare body with updated values
        const body = {
            exercise_id: this.id,
            workouts: this.selectedWorkouts 
        };
        // prepare request options
        const requestOptions = {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({body})
        };

        // make fetch request 
        const response = await fetch('http://localhost:8000/api/plan', requestOptions);
        
        // handle response
        if (!response.ok) {
            throw new Error("Error occurred.");
        }

        await response.json();
        
      }
    },
  };
  </script>
  
  <style scoped>
  .modal.fade.show {
    display: block;
  }
  </style>
  