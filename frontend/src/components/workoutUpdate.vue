<template>
    <div v-if="show" class="modal fade show d-block" style="background-color: rgba(0, 0, 0, 0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title"> Update Workout </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="$emit('updateWorkout', body, id)" class="container p-4 border rounded shadow-sm">
              <div class="mb-3">
                <label for="name" class="form-label">Name:</label>
                <input v-model="body.name" type="text" name="name" class="form-control" placeholder="Updated name / Leave blank">
              </div>
              <div class="mb-3">
                <label for="desc" class="form-label">Description:</label>
                <textarea v-model="body.description" name="desc" class="form-control" rows="3" placeholder="Updated description / Leave blank"></textarea>
              </div>
              <div class="mb-3">
                <label for="date" class="form-label">Date:</label>
                <input v-mode l="body.date" type="date" name="date" class="form-control">
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
        body: {
          full_flag: true,
          id: null,
          name: "",
          description: "",
          date: ""
        }
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
    },
  };
  </script>
  
  <style scoped>
  .modal.fade.show {
    display: block;
  }
  </style>
  