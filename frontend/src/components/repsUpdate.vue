<template>
    <div v-if="show" class="modal fade show d-block" style="background-color: rgba(0, 0, 0, 0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title"> Update Reps & Sets </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <h4 class="p-2"> Updating <i> {{ exName }} </i> in <i> {{ workoutName }} </i> </h4>
            <form @submit.prevent="$emit('updatePlan', body, workout_id, ex_id)" class="d-flex flex-column align-items-center justify-content-between border p-3 rounded">
                <div class="d-flex align-items-center justify-content-between p-3 w-75">
                    <label for="reps">Reps: </label>
                    <input class="w-75 p-2" v-model="body.newReps" type="number" name="reps" placeholder="Updated reps / leave blank">
                </div>
                <div class="d-flex align-items-center justify-content-between p-3 w-75">
                    <label for="sets">Sets: </label>
                    <input class="w-75 p-2" v-model="body.newSets" type="text" name="sets" placeholder=" Updated sets / leave blank">
                </div>
                <button type="submit" class="btn btn-primary w-50"> Update </button>
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
              rs_flag: true,
              newReps: null,
              newSets: null 
            }       
        }
    },  
    props: {
      show: {
        type: Boolean,
        required: true,
      },
      workout_id: {
        type: Number,
        required: true
      },
      ex_id: {
        type: Number,
        required: true
      },
      exName: {
        type: String,
        required: true,
      },
      workoutName: {
        type: String,
        required: true,
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
  