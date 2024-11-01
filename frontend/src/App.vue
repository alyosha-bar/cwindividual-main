<template>
    <div class="container pt-3">
        <div class="h1 text-center border rounded bg-light p-4 mb-3">
            Workout Buddy
        </div>
        <div class="mb-3">
            <h2>Workout List</h2>             
        </div>
        <workouts></workouts>

        <!-- Button trigger modal -->
        <div class="d-flex justify-content-center gap-3 py-3">
            <exerciseModal></exerciseModal>
            <workoutModal></workoutModal>
        </div>

    </div>
</template>
  
<script>
import exerciseModal from './components/exerciseModal.vue';
import workoutModal from './components/workoutModal.vue';
import Workouts from './components/workouts.vue';
import workouts from './components/workouts.vue';
export default {
    components: {
        exerciseModal,
        workoutModal,
        workouts
    },
};
</script>
