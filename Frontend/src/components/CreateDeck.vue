<template>
  <div>
    <div class="container">
      <form v-on:submit.prevent="submitForm">
        <div class="form-group form-outline form-white mb-4">
          <div
            v-if="error === true"
            v-bind="message"
            class="alert alert-danger text-center"
            role="alert"
          >
            {{ messag }}
          </div>
          <label class="form-label text-white" for="deck_name"
            >Enter name for deck:</label
          >
          <input
            v-model="deck_name"
            name="deck_name"
            type="deck_name"
            id="front"
            class="form-control form-control-lg"
          />
        </div>

        <a
          type="submit"
          @click="submitForm"
          class="btn btn-outline-light btn-lg px-5"
          >Create New Deck</a
        >&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
        <a v-on:click="onClickCancel" class="btn btn-outline-light btn-lg px-5"
          >Cancel</a
        >
      </form>
    </div>
  </div>
</template>


<script lang="ts">
import axios from "axios";
export default {
  name: "CreateDeck",
  data() {
    return {
      responsedata: [],
      deck_name: "",
      deck_id: "",
      error: false,
      messag: "",
    };
  },
  methods: {
    onClickCancel() {
      this.$emit("activeButton", "Empty");
      this.$router.go();
    },

    async submitForm() {
      const token = localStorage.getItem("x-access-token");
      var formData = new FormData();
      formData.append("deck_name", this.deck_name);
      await axios
        .post("http://127.0.0.1:8080/deck", formData, {
          headers: {
            "x-access-token": `${token}`,
          },
        })
        .then((result) => {
          console.log(result.data.deck_id);
          this.$emit("activeButton", "Empty");
          this.deck_id = result.data.deck_id;
          this.$router.push("/cards/?" + this.deck_id);
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