<template>
    <div class="container pt-3">
        <div>
            <h2 class="text-center my-4"> Aleksej's Workout Buddy </h2>

            <!-- Tabs Navigation -->
            <ul class="nav nav-tabs" role="tablist">
                <li class="nav-item" @click="activeTab = 1">
                    <a class="nav-link" :class="{ active: activeTab === 1 }" href="#"> Workouts </a>
                </li>
                <li class="nav-item" @click="activeTab = 2">
                    <a class="nav-link" :class="{ active: activeTab === 2 }" href="#"> Exercises </a>
                </li>
            </ul>

            <!-- Tab Content -->
            <div class="tab-content mt-3">
                <div v-if="activeTab === 1" class="tab-pane fade show active">
                    <h3> Workouts List </h3>
                    <workouts></workouts>
                </div>

                <div v-if="activeTab === 2" class="tab-pane fade show active">
                    <h3> Exercises List </h3>
                    <exercises></exercises>
                </div>
            </div>
        </div>

    </div>
</template>
  
<script>
import exerciseModal from './components/exerciseModal.vue';
import workoutModal from './components/workoutModal.vue';
import Workouts from './components/workouts.vue';
import workouts from './components/workouts.vue';
import exercises from './components/exercises.vue';
export default {
    components: {
        exerciseModal,
        workoutModal,
        workouts,
        exercises
    },
    data() {
        return {
            activeTab: 1,
        };
    },
};
</script>
