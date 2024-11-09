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
                <input v-model="name" type="text" name="name" class="form-control" placeholder="Updated name / Leave blank">
              </div>
              <div class="mb-3">
                <label for="desc" class="form-label">Description:</label>
                <textarea v-model="description" name="desc" class="form-control" rows="3" placeholder="Updated description / Leave blank"></textarea>
              </div>
              <div class="mb-3">
                <label for="date" class="form-label">Date:</label>
                <input v-model="date" type="date" name="date" class="form-control">
              </div>
              <button type="submit" class="btn btn-primary w-100"> Update Workout </button>
            </form>
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
        date: ""
      };
    },
    props: {
      show: {
        type: Boolean,
        required: true,
      },
      id: {
        type: Number,
        required: true,
      },
    },
    methods: {
      closeModal() {
        this.$emit("close");
      },
      async updateWorkout() {
        console.log("Updating Workout.");

        console.log(this.date)

        // prepare body
        const body = {
            full_flag: true, 
            workoutId: this.id,
            name: this.name,
            description: this.description,
            date: this.date
        }

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

        const message = response.json()
        return message
      },
    },
  };
  </script>
  
  <style scoped>
  .modal.fade.show {
    display: block;
  }
  </style>
  