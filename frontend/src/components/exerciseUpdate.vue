<template>
    <div v-if="show" class="modal fade show d-block" style="background-color: rgba(0, 0, 0, 0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Modal Title</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateExercise" class="container p-4 border rounded shadow-sm">   
              <div class="mb-3">
                <label for="name" class="form-label">Name:</label>
                <input v-model="exName" type="text" name="name" class="form-control" placeholder="Updated name / Leave Blank"/>
              </div>
              <div class="mb-3">
                <label for="desc" class="form-label">Description:</label>
                <textarea v-model="exDesc" name="desc" class="form-control" rows="3" placeholder="Updated description / Leave Blank"></textarea>
              </div>
              <div class="mb-3">
                <label for="weight" class="form-label">Weight:</label>
                <input v-model="exWeight" type="number" name="weight" class="form-control" placeholder="Updated Weight / Leave Blank"/>
              </div>
              <div class="mb-3">
                <label for="difficulty" class="form-label">Difficulty:</label>
                <input v-model="exDiff" type="number" name="difficulty" class="form-control" placeholder="Updated Difficulty / Leave Blank"/>
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
            exName: "",
            exDesc: "",
            exWeight: undefined,
            exDiff: undefined,
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
      async updateExercise() {
        // prepare body with updated values
        const body = {
            id: this.id,
            name: this.exName,
            description: this.exDesc,
            weight: this.exWeight,
            difficulty: this.exDiff
        };
        // prepare request options
        const requestOptions = {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ body })
        };

        // make fetch request 
        const response = await fetch('http://localhost:8000/api/exercises', requestOptions);

        if (!response.ok) {
            throw new Error("Error occurred.");
        }
        
        // handle response
        await response.json();
        this.exName = "";
        this.exDesc = "";
        this.exWeight = undefined;
        this.exDiff = undefined;
      }
    },
  };
  </script>
  
  <style scoped>
  .modal.fade.show {
    display: block;
  }
  </style>
  