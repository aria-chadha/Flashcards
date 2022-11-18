<template>
  <div>
    <nav class="navbar navbar-expand navbar-dark bg-dark fixed-top">
      <div class="container">
        <div class="navbar-brand">Flashcards</div>
        <ul class="navbar-nav ms-auto">
          <li class="nav-item active">
            <router-link class="nav-link" to="/dashboard"
              >Dashboard</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>

          
          <li class="nav-item">
            <router-link class="nav-link" v-on:click="logout" to="/"
              >Logout</router-link
            >
          </li>
        </ul>
      </div>
    </nav>

    <h1>{{deckname}}</h1>
    <div class="container">
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
          Cards created by user are displayed here.
        </caption>
        <thead class="table-dark">
          <tr>
            <th scope="col">No.</th>
            <th scope="col">Question</th>
            <th scope="col">Answer</th>
            <th scope="col">Edit</th>
            <th scope="col">Delete</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(data, index) of responsedata" :key="card_id">
            <td v-if="data.front">{{ index + 1 }}</td>
            <td v-if="data.front">{{ data.front }}</td>
            <td v-if="data.front">{{ data.back }}</td>
            <td v-if="data.front">
              <a v-on:click="editcard(data.card_id)" class="btn btn-dark btn-sm"
                >Edit</a
              >
            </td>
            <td v-if="data.front">
              <a
                v-on:click="deletecard(data.card_id)"
                class="btn btn-dark btn-sm"
                >Delete</a
              >
            </td>
          </tr>
        </tbody>
      </table>
      <div class="text-center">
        <button class="btn btn-light btn-md" @click="createcard();scrollToEl();">
          Create Card</button
        >&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
        <button class="btn btn-light btn-md" v-on:click="deletedeck">
          Delete Deck</button
        >&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
        <button class="btn btn-light btn-md" v-on:click="editdeck();scrollToEl();">
          Edit Deck
        </button>
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
        <button v-if="responsedata[0]" class="btn btn-light btn-md">
          <download-csv  :data="responsedata">
        Export to .csv file
      </download-csv>
        </button>
      </div>
      <br>
      <div class="container text-center">
      
      </div>
      <create-card v-if="changeButton === 'CreateCard'"></create-card>
      <edit-deck v-if="changeButton === 'EditDeck'"></edit-deck>
    </div>
    <br>
  </div>
</template>

<script lang="ts">
import Empty from "../components/Empty.vue";
import CreateCard from "../components/CreateCard.vue";
import EditCard from "../components/EditCard.vue";
import EditDeck from "../components/EditDeck.vue";
import DownloadCsv from "../components/JsonCSV.vue"
import axios from "axios";
import EditDeck1 from "./EditDeck.vue";
export default {
  name: "Cards",
  data() {
    return {
      responsedata: [],
      deck_id: window.location.href.substring(29),
      deckname:'',
      changeButton: "",
      card_id: "",
      error: false,
      messag: "",
    };
  },
  components: {
    Empty,
    CreateCard,
    EditCard,
    EditDeck,
    DownloadCsv,
    EditDeck1
},
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push("/");
    },
    scrollToEl(){
      window.scrollTo(0, document.body.scrollHeight);
    },
    editcard(cardid) {
      this.$router.push("/card/?" + cardid);
    },
    async createcard() {
      this.changeButton = "CreateCard";
    },
    editdeck() {
      this.changeButton = "EditDeck";
    },
    async deletedeck() {
      const token = localStorage.getItem("x-access-token");
      const URL =
        "http://localhost:8080/deck/" + window.location.href.substring(29);

      await axios
        .delete(URL, { headers: { "x-access-token": `${token}` } })
        .then((result) => {
          this.$router.push("/dashboard");

        })
        .catch((error) => {
          this.error = true;
          this.messag = error.response.data.message;
          console.log(error.response.data.message);
        });
    },
    async deletecard(cardid) {
      const token = localStorage.getItem("x-access-token");
      const URL = "http://localhost:8080/card/" + cardid;
      await axios
        .delete(URL, { headers: { "x-access-token": `${token}` } })
        .then((result) => {
          this.error = false;
          this.$router.go();
        })
        .catch((error) => {
          this.error = true;
          this.messag = error.response.data.message;
          console.log(error.response.data.message);
        });
    },
  },

  async created() {
    const token = localStorage.getItem("x-access-token");
    const URL =
      "http://localhost:8080/cards/" + window.location.href.substring(29);

    await axios
      .get(URL, { headers: { "x-access-token": `${token}` } })
      .then((result) => {
        this.responsedata = result.data;
        console.log(result.data);
      })
      .catch((error) => {
        this.error = true;
        this.messag = error.response.data.message;
        console.log(error.response.data.message);
      });
    
    const URD =
      "http://localhost:8080/" + this.deck_id;

    await axios
      .get(URD, { headers: { "x-access-token": `${token}` } })
      .then((result) => {
        this.deckname = result.data.deckname;
        console.log(this.deckname);
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
.down{
  font-size: 18px;
  font-weight: medium;
}
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
</style>