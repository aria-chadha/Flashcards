<template>
  <div>
    <div class="container text-center">
      <form v-on:submit.prevent>
        <div class="form-group form-outline form-white mb-4">
          <label class="form-label text-white" for="newdeckname"
            >Enter a new name for deck:</label
          >
          <input
            v-model="newdeckname"
            name="newdeckname"
            type="newdeckname"
            id="newdeckname"
            class="form-control form-control-lg"
          />
        </div>

        <button
          type="submit"
          @click="submitForm"
          class="btn btn-outline-light btn-lg px-5"
        >
          Save Changes</button
        >&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
        <a @click="onClickCancel" class="btn btn-outline-light btn-lg px-5"
          >Cancel</a
        >
      </form>
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
      newdeckname: "",
    };
  },
  methods: {
    onClickCancel() {
      this.$emit("activeButton", "Empty");
      this.$router.go();
    },
    async submitForm() {
      this.$emit("activeButton", "Empty");
      const token = localStorage.getItem("x-access-token");
      var formData = new FormData();
      formData.append("new_deck_name", this.newdeckname);
      await axios
        .put(
          "http://127.0.0.1:8080/deck/" + window.location.href.substring(29),
          formData,
          {
            headers: {
              "x-access-token": `${token}`,
            },
          }
        )
        .then((result) => {
          console.log(result.data);
          this.$router.go();
        })
        .catch((error) => {
          console.log(error.response.data);
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