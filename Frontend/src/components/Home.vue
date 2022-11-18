<template>
  <body>
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
    <div class="container">
      <h1>Welcome to Flashcards</h1>
      <h6><i>Refresh your memory!</i></h6>
      <br />
      <p>
        Flashcards are small note cards used for testing and improving memory
        through practiced information retrieval. Flashcards are typically
        two sided, with the prompt on one side and the information about the
        prompt on the other.
      </p>
      <p align="center">
        <img src="../assets/facts.gif" />
      </p>
      <br />
      <p><a href="/register">Register</a> with us and get started!</p>
      <p>
        If you are registered already, <a href="/login">Login</a> to your
        account.
      </p>
    </div>
  </body>
</template>
<script lang="ts">
export default {
  name: "Home",

  async created() {
    localStorage.clear();
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
h6 {
  color: whitesmoke;
  font-weight: medium;
  text-align: center;
}
p {
  padding-left: 10%;
  padding-right: 10%;
  color: whitesmoke;
  font-weight: light;
  text-align: center;
}
a {
  color: rgb(113, 139, 196);
  font-weight: light;
}
</style>
