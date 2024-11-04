<template>
    <div class="container pt-3">
        <div>
            <h2 class="text-center my-4"> Workout Buddy </h2>

            <!-- Tabs Navigation -->
            <ul class="nav nav-tabs" role="tablist">
                <li class="nav-item" @click="activeTab = 1">
                    <a class="nav-link" :class="{ active: activeTab === 1 }" href="#"> Workouts </a>
                </li>
                <li class="nav-item" @click="activeTab = 2">
                    <a class="nav-link" :class="{ active: activeTab === 2 }" href="#"> Exercises </a>
                </li>
                <li class="nav-item" @click="activeTab = 3">
                    <a class="nav-link" :class="{ active: activeTab === 3 }" href="#"> Other </a>
                </li>
            </ul>

            <!-- Tab Content -->
            <div class="tab-content mt-3">
                <div v-if="activeTab === 1" class="tab-pane fade show active">
                    <h3> Workouts List </h3>
                    <workouts></workouts>
                    <div class="d-flex justify-content-center gap-3 py-3">
                        <workoutModal></workoutModal>
                    </div>
                </div>

                <div v-if="activeTab === 2" class="tab-pane fade show active">
                    <h3> Exercises List </h3>
                    <div class="d-flex justify-content-center gap-3 py-3">
                        <exerciseModal></exerciseModal>
                    </div>
                </div>

                <div v-if="activeTab === 3" class="tab-pane fade show active">
                    <h3>Tab 3 Content</h3>
                    <div>This is some content for Tab 3.</div>
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
export default {
    components: {
        exerciseModal,
        workoutModal,
        workouts
    },
    data() {
        return {
            activeTab: 1, // Set the default active tab to Tab 1
        };
    },
};
</script>
