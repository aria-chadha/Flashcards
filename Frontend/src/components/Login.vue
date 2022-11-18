
<template>
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
          <router-link class="nav-link" to="/login">Login</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/register">Register</router-link>
        </li>
      </ul>
    </div>
  </nav>

  <div id="login">
    <div class="vh-100 gradient-custom">
      <div class="container py-5 h-100">
        <div class="row d-flex justify-content-center align-items-center h-100">
          <div class="col-12 col-md-8 col-lg-6 col-xl-5">
            <div class="card bg-dark text-white">
              <div class="card-body p-5 text-center">
                <div class="mb-md-3 mt-md-0 pb-5">
                  <h2 class="fw-bold mb-2 text-uppercase">Log in</h2>

                  <p class="text-white-50 mb-5">
                    Please enter your username and password
                  </p>
              <div v-if="error===true" v-bind="message" class="alert alert-danger" role="alert">
                    {{messag}}
              </div>
                  <form v-on:submit.prevent="submitForm">
                    <div class="form-group form-outline form-white mb-4">
                      <label class="form-label" for="username">Username</label>
                      <input
                        v-model="username"
                        name="username"
                        type="username"
                        id="username"
                        class="form-control form-control-lg"
                      />
                    </div>

                    <div class="form-group form-outline form-white mb-4">
                      <label class="form-label" for="password">Password</label>
                      <input
                        v-model="password"
                        name="password"
                        type="password"
                        id="password"
                        class="form-control form-control-lg"
                      />
                    </div>

                    <button class="btn btn-outline-light btn-lg px-5">
                      Log in
                    </button>
                  </form>
                </div>

                <div>
                  <p class="card-footer text-center">
                    Don't have an account?
                    <a href="/register" class="text-white-50 fw-bold"
                      >Register</a
                    >
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import axios from "axios";

export default {
  name: "Login",
  data() {
    return {
      email: "",
      username: "",
      password: "",
      error:false,
      messag:''
    };
  },

  methods: {
    async submitForm() {
      var formData = new FormData();
      formData.append("username", this.username);
      formData.append("password", this.password);
      await axios
        .post("http://127.0.0.1:8080/login", formData)
        .then((result) => {
          console.log(result.data);
          axios.defaults.headers.common["token"] = result.data.token;
          localStorage.setItem("x-access-token", result.data.token);
          this.$router.push("/dashboard");
        })
        .catch((error) => {
          this.error=true;
          this.messag =error.response.data.message
          console.log(error.response.data.message);
        });
    },
  },
  async created() {
    localStorage.clear();
  },
};
</script>
