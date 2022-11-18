<template>
  <div>
    <div class="container text-center">
      <form v-on:submit.prevent>
        <div class="form-group form-outline form-white mb-4">
          <div
            v-if="error === true"
            v-bind="message"
            class="alert alert-danger text-center"
            role="alert"
          >
            {{ messag }}
          </div>
          <label class="form-label text-white" for="front"
            >Enter Question:</label
          >
          <input
            v-model="front"
            name="front"
            type="front"
            id="front"
            class="form-control form-control-lg"
          />
        </div>

        <div class="form-group form-outline form-white mb-4">
          <label class="form-label text-white" for="back">Enter Answer:</label>
          <input
            v-model="back"
            name="back"
            type="back"
            id="back"
            class="form-control form-control-lg"
          />
        </div>

        <button
          type="submit"
          @click="submitForm"
          class="btn btn-outline-light btn-lg px-5"
        >
          Create New Card</button
        >&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
        <a v-on:click="onClickCancel" class="btn btn-outline-light btn-lg px-5"
          >Cancel</a
        >
      </form>
      <br />
    </div>
  </div>
</template>


<script lang="ts">
import axios from "axios";
export default {
  name: "Cards",
  data() {
    return {
      responsedata: [],
      front: "",
      back: "",
      error: false,
      messag: "",
    };
  },
  methods: {
    onClickCancel() {
      this.$emit("changeButton", "Empty");
      this.$router.go();
    },
    async submitForm() {
      this.$emit("changeButton", "Empty");
      const token = localStorage.getItem("x-access-token");
      var formData = new FormData();
      formData.append("front", this.front);
      formData.append("back", this.back);
      await axios
        .post(
          "http://127.0.0.1:8080/newcard/" + window.location.href.substring(29),
          formData,
          {
            headers: {
              "x-access-token": `${token}`,
            },
          }
        )
        .then((result) => {
          this.$router.go();
        })
        .catch((error) => {
          this.error = true;
          this.messag = error.response.data.message;
          console.log(error.response.data.message);
        });
    },
  },
};
</script>

<style scoped>
h1,
h3 {
  margin-top: 10vh;
  color: whitesmoke;
  font-size: 50px;
  font-weight: medium;
  text-align: center;
}

form {
  margin-top: 10vh;
}
</style>