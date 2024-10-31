<template>
    <div class="modal fade" id="exerciseModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">Add Exercise</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="createExercise" class="container p-4 border rounded shadow-sm">
              <div class="mb-3">
                <label for="name" class="form-label">Name:</label>
                <input v-model="exName" type="text" name="name" class="form-control" placeholder="Enter exercise name" required />
              </div>
              <div class="mb-3">
                <label for="desc" class="form-label">Description:</label>
                <textarea v-model="exDesc" name="desc" class="form-control" rows="3" placeholder="Enter exercise description" required></textarea>
              </div>
              <div class="mb-3">
                <label for="weight" class="form-label">Weight:</label>
                <input v-model="exWeight" type="number" name="weight" class="form-control" placeholder="0 (bodyweight)" required />
              </div>
              <div class="mb-3">
                <label for="difficulty" class="form-label">Difficulty:</label>
                <input v-model="exDiff" type="number" name="difficulty" class="form-control" placeholder="1, 2, or 3" required />
              </div>
              <button type="submit" class="btn btn-primary w-100">Add Exercise</button>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
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
        };
    },
    methods: {
        async createExercise() {
            const body = {
                name: this.exName,
                description: this.exDesc,
                weight: this.exWeight,
                difficulty: this.exDiff
            };

            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ body })
            };

            const response = await fetch('http://localhost:8000/api/addexercise', requestOptions);

            if (!response.ok) {
                throw new Error("Error occurred.");
            }

            await response.json();
            this.exName = "";
            this.exDesc = "";
            this.exWeight = undefined;
            this.exDiff = undefined;
        }
    },
    async mounted() {
        console.log("Mounted Exercise Modal.")
    }
}

</script>