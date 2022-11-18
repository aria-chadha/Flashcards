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
            <router-link class="nav-link" to="/about">About</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-on:click="logout" to="/"
              >Logout</router-link
            >
          </li>
        </ul>
      </div>
    </nav>
    <div>
      <div class="container">
        <h1>Dashboard</h1>
        <div
          v-if="error === true"
          v-bind="message"
          class="alert alert-danger text-center"
          role="alert"
        >
          {{ messag }}
        </div>
        <table
          class="table table-light table-striped table-borderless table-hover"
        >
          <caption class="text-center">
            Decks created by user are displayed here.
          </caption>
          <thead class="table-dark">
            <tr>
              <th scope="col">No.</th>
              <th scope="col">Deck Name</th>
              <th scope="col">Creator</th>
              <th scope="col" class="text-center">Score</th>
              <th scope="col" class="text-center">Last Reviewed</th>
              <th scope="col" class="text-center">Review</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(data, index) of responsedata" :key="deck_id">
              <td>{{ index + 1 }}</td>
              <td>
                <a class="pointing" v-on:click="gotocards(data.deck_id)"
                  >{{ data.deck_name }}
                </a>
              </td>
              <td>{{ data.creator }}</td>
              <td class="text-center" v-if="data.score">{{ data.score }}</td>
              <td class="text-center" v-else>-</td>
              <td class="text-center" v-if="data.last_reviewed">
                {{ data.last_reviewed }}
              </td>
              <td class="text-center" v-else>-</td>
              <td class="text-center">
                <a class="btn btn-dark btn-sm" @click="gotoreview(data.deck_id)"
                  >Review</a
                >
              </td>
            </tr>
          </tbody>
        </table>
        <div class="text-center">
          <button class="btn btn-light btn-md" v-on:click="activeTab">
            Create Deck
          </button>
          <create-deck v-if="activeButton === 'CreateDeck'"></create-deck>
          <empty v-if="activeButton === 'Empty'"></empty>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import axios from "axios";
import CreateDeck from "../components/CreateDeck.vue";
import Empty from "../components/Empty.vue";

export default {
  name: "Dash",
  components: {
    CreateDeck,
    Empty,
  },
  data() {
    return {
      responsedata: [],
      activeButton: "",
      deck_id: "",
      error: false,
      messag: "",
    };
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push("/");
    },
    gotocards(deckid) {
      this.$router.push("/cards/?" + deckid);
    },
    gotoreview(deckid) {
      this.$router.push("/review/?" + deckid);
    },
    activeTab() {
      this.activeButton = "CreateDeck";
    },
  },
  async created() {
    const token = localStorage.getItem("x-access-token");
    await axios
      .get("http://127.0.0.1:8080/decks", {
        headers: {
          "x-access-token": `${token}`,
        },
      })
      .then((result) => {
        this.responsedata = result.data;
        console.log(result.data);
      })
      .catch((error) => {
        this.error = true;
        this.messag = error.response.data.message;
        console.log(error.response.data.message);
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
.table {
  margin-top: 5vh;
}
.pointing {
  cursor: pointer;
  color: black;
}
</style>