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
          <li class="nav-item active">
            <router-link class="nav-link" to="/dashboard"
              >Dashboard</router-link
            >
          </li>
          <li class="nav-item">
            <router-link class="nav-link" v-on:click="logout" to="/"
              >Logout</router-link
            >
          </li>
        </ul>
      </div>
    </nav>
    <ul class="flashcard-list">
      <li v-for="(card, index) in responsedata" :key="card_id">
        <div class="vh-100 gradient-custom">
          <div class="container h-100" ref="page">
            <div class="row justify-content-center align-items-center h-100">
              <div class="col-12 col-md-8 col-lg-6 col-xl-5">
                <div
                  class="card bg-dark text-white"
                  v-on:click="toggleCard(card)"
                >
                  <div class="card-body p-5 text-center">
                    <div class="mb-md-3 mt-md-0">
                      <br /><br /><br />
                      <transition name="flip">
                        <p v-bind:key="card.flipped" class="bg-dark text-white">
                          {{ card.flipped ? card.back : card.front }}
                        </p>
                      </transition>
                      <br /><br /><br /><br /><br /><br />

                      <form v-on:submit.prevent="submitForm">
                        <div>
                          <button
                            class="btn btn-success"
                            @click="easy(card.card_id, index)"
                            value="10"
                            name="partialscore"
                            id="partialscore"
                          >
                            Easy</button
                          >&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                          <button
                            class="btn btn-warning"
                            @click="medium(card.card_id, index)"
                            value="5"
                            name="partialscore"
                            id="partialscore"
                          >
                            Medium</button
                          >&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                          <button
                            class="btn btn-danger"
                            @click="hard(card.card_id, index)"
                            value="2"
                            name="partialscore"
                            id="partialscore"
                          >
                            Hard</button
                          >&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
                <br>
                <div align="center"><img
                v-if="responsedata[index + 1]"
                src="../assets/down-arrow.png"
                style="object-fit: fill; width: 70px; height: 65px"
                @click="scrollToElement(index)"
              /></div>
              </div>
              
              <div class="text-center" v-if="!responsedata[index + 1]">
                <button @click="dash" class="btn btn-light btn-lg px-5">
                  I'm done
                </button>
                
              </div>
              
            </div>
            
          </div>
        </div>
      </li>
    </ul>

    <br /><br /><br />
  </div>
</template>

<script lang="ts">
import axios from "axios";
export default {
  name: "Review",
  data() {
    return {
      responsedata: [],
    };
  },
  components: {},
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push("/");
    },
    toggleCard(card) {
      card.flipped = !card.flipped;
    },
    dash() {
      this.$router.push("/dashboard");
    },

    scrollToElement(index) {
      var container = this.$refs.page;
      
      if (container[index + 1]) {console.log(container[index + 1]);
        window.scrollTo(900, container[index + 1].offsetTop);
      }
      else{ }
    },

    async easy(cardid, index) {
      const token = localStorage.getItem("x-access-token");
      var formData = new FormData();
      formData.append("partialscore", "10");
      await axios
        .post("http://127.0.0.1:8080/review/" + cardid, formData, {
          headers: {
            "x-access-token": `${token}`,
          },
        })
        .then((result) => {
          console.log(result.data);
          this.scrollToElement(index);
        })
        .catch((error) => {
          console.log(error.response.data);
        });
    },
    async medium(cardid, index) {
      const token = localStorage.getItem("x-access-token");
      var formData = new FormData();
      formData.append("partialscore", "5");
      await axios
        .post("http://127.0.0.1:8080/review/" + cardid, formData, {
          headers: {
            "x-access-token": `${token}`,
          },
        })
        .then((result) => {
          console.log(result.data);
          this.scrollToElement(index);
        })
        .catch((error) => {
          console.log(error.response.data);
        });
    },
    async hard(cardid, index) {
      const token = localStorage.getItem("x-access-token");
      var formData = new FormData();
      formData.append("partialscore", "2");
      await axios
        .post("http://127.0.0.1:8080/review/" + cardid, formData, {
          headers: {
            "x-access-token": `${token}`,
          },
        })
        .then((result) => {
          console.log(result.data);
          this.scrollToElement(index);
        })
        .catch((error) => {
          console.log(error.response.data);
        });
    },
  },
  async created() {
    const token = localStorage.getItem("x-access-token");
    const URL =
      "http://localhost:8080/cards/" + window.location.href.substring(30);

    await axios
      .get(URL, {
        headers: {
          "x-access-token": `${token}`,
        },
      })
      .then((result) => {
        this.responsedata = result.data;
        console.log(this.responsedata);
      })
      .catch((e) => {
        this.$router.push("/cards/" + window.location.href.substring(29));
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
</style>