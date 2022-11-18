<template>
  <div>
    <nav class="navbar navbar-expand navbar-dark bg-dark fixed-top">
      <div class="container">
        <div class="navbar-brand">Flashcards</div>
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item active">
            <router-link class="nav-link" to="/dashboard">Dashboard</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-on:click="logout" to="/"
              >Logout</router-link
            >
          </li>
        </ul>
      </div>
    </nav>
    <div class="container">
                   
      <form v-on:submit.prevent="submitForm">
        <div class="form-group form-outline form-white mb-4">
          <label class="form-label text-white" for="front"
            >Enter a new Question:</label
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
          <label class="form-label text-white" for="back"
            >Enter a new Answer:</label
          >
          <input
            v-model="back"
            name="back"
            type="back"
            id="back"
            class="form-control form-control-lg"
          />
        </div>
         <div v-if="error===true" v-bind="message" class="alert alert-danger" role="alert">
                    {{messag}}
              </div>
        <button type="submit" class="btn btn-outline-light btn-lg px-5">
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
      front: "",
      back: "",
      error:false,
      messag:''
    };
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push("/");
    },
    onClickCancel() {
      this.$emit("activeButton", "Empty");
      this.$router.go(-1);
    },
    async submitForm() {
      const token = localStorage.getItem("x-access-token");
      var formData = new FormData();
      formData.append("front", this.front);
      formData.append("back", this.back);
      await axios
        .put(
          "http://127.0.0.1:8080/card/" + window.location.href.substring(28),
          formData,
          {
            headers: {
              "x-access-token": `${token}`,
            },
          }
        )
        .then((result) => {
          console.log(result.data.deck_id)
          let deck_id = result.data.deck_id;
          this.$router.push("/cards/?" + deck_id);
        })
        .catch((error) => {
           this.error=true;
          this.messag =error.response.data.message
          console.log(error.response.data.message);
        });
    },
  },
  async created() {
    const token = localStorage.getItem("x-access-token");
    const URL =
      "http://localhost:8080/carde/" + window.location.href.substring(28);

    await axios
      .get(URL, {
        headers: {
          "x-access-token": `${token}`,
        },
      })
      .then((result) => {
        console.log(result.data);
        this.front=result.data.front;
        this.back=result.data.back;
      })
      .catch((e) => {
      });
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