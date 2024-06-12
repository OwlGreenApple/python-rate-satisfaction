<template>
  <div class="feedback-container">
    <h2>How would you rate your satisfaction with our product?</h2>
    <div class="stars">
      <span
        v-for="star in 5"
        :key="star"
        :class="{ filled: star <= selectedRating }"
        @click="setRating(star)"
      >
        &#9733;
      </span>
    </div>
    <div class="labels">
      <span>Very dissatisfied</span>
      <span>Very satisfied</span>
    </div>
    <button @click="submitFeedback">Submit</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedRating: 0,
    };
  },
  methods: {
    setRating(rating) {
      this.selectedRating = rating;
    },
    async submitFeedback() {
      try {
        const response = await fetch('http://localhost:8000/feedback', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ score: this.selectedRating }),
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        alert(data.message);
      } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
      }
    },
  },
};
</script>

<style scoped>
.feedback-container {
  text-align: center;
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
}

h2 {
  margin-bottom: 20px;
}

.stars {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.stars span {
  font-size: 2rem;
  cursor: pointer;
  margin: 0 5px;
  color: #ccc;
}

.stars span.filled {
  color: #ffcc00;
}

.labels {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

button {
  padding: 10px 20px;
  font-size: 1rem;
  color: #fff;
  background-color: #6200ea;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #3700b3;
}
</style>
