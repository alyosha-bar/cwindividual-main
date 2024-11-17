<template>
    <div v-if="show" class="modal fade show d-block" style="background-color: rgba(0, 0, 0, 0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Modal Title</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="$emit('updateExercise', body, id)" class="container p-4 border rounded shadow-sm">   
              <div class="mb-3">
                <label for="name" class="form-label">Name:</label>
                <input v-model="body.exName" type="text" name="name" class="form-control" placeholder="Updated name / Leave Blank"/>
              </div>
              <div class="mb-3">
                <label for="desc" class="form-label">Description:</label>
                <textarea v-model="body.exDesc" name="desc" class="form-control" rows="3" placeholder="Updated description / Leave Blank"></textarea>
              </div>
              <div class="mb-3">
                <label for="weight" class="form-label">Weight:</label>
                <input v-model="body.exWeight" type="number" name="weight" class="form-control" placeholder="Updated Weight / Leave Blank"/>
              </div>
              <div class="mb-3">
                <label for="difficulty" class="form-label">Difficulty:</label>
                <input v-model="body.exDiff" type="number" name="difficulty" class="form-control" placeholder="Updated Difficulty / Leave Blank"/>
              </div>
              <button type="submit" class="btn btn-primary w-100">Update Exercise</button>
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
                id: null,
                exName: "",
                exDesc: "",
                exWeight: null,
                exDiff: null
            }
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
  