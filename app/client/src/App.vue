<template>
  <div id="app">
      <nav class="navbar navbar-expand-lg navbar-dark bg-primary" v-if="navbar">
          <a class="navbar-brand">
                <vs-button @click="active=!active" color="dark" icon="storage" class="sidebarButton"></vs-button></a>
          <div class="collapse navbar-collapse" id="navbarColor02">
            <ul class="navbar-nav mr-auto">
              <li class="nav-item active">
                <a class="nav-link" href="/">Template<span class="sr-only">(current)</span></a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="/docs">Docs</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="/about">About</a>
              </li>
            </ul>
          </div>
          <div class="navbar-collapse collapse w-100 order-3 dual-collapse2">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                    <a class="nav-link" href="#">Contact</a>
                </li>
              <li class="nav-item">
                <a class="nav-link" v-on:click="logout()">Logout</a>
              </li>

            </ul>
        </div>
        </nav>
      <div id="parentx" style="margin: 5rem" v-if="navbar">
            <vs-sidebar parent="body" default-index="1" class="sidebar" color="dark" spacer v-model="active">

              <div class="header-sidebar" slot="header">
                <vs-avatar color="dark" icon="developer_board" size="large" class="role"></vs-avatar>
                <h4>Eike</h4>
              </div>

              <vs-sidebar-item index="1" to="/user/home" icon="developer_board">Dashboard</vs-sidebar-item>
                <vs-divider position="center"></vs-divider>
              <vs-sidebar-item index="2" icon="library_books">Assemblies</vs-sidebar-item>
                <vs-sidebar-item index="3" icon="library_books">Pipelines</vs-sidebar-item>
                <vs-sidebar-item index="4" icon="library_books">Protocols</vs-sidebar-item>

                <vs-divider position="center"></vs-divider>

                <vs-sidebar-item index="5" icon="library_books">Database</vs-sidebar-item>


                <vs-divider position="center"></vs-divider>
                <vs-sidebar-item index="7" icon="account_box">Profile</vs-sidebar-item>
                <vs-sidebar-item index="8" icon="settings" to="/user/settings">Settings</vs-sidebar-item>

            </vs-sidebar>
          </div>
      <router-view/>
  </div>
</template>

<script>

import firebase from 'firebase';

export default {
  name: 'App',
  data() {
    return {
      server: 'localhost:5000',
      navbar: true,
      active: false,
    };
  },
  methods: {
      logout() {
          firebase.auth().signOut().then(() => {
                this.$router.replace('login')
            }
          )
      }
  },
}
</script>

<style>

#app {
  font-family: Consolas, monaco, monospace;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.sidebarButton {
    margin-bottom: 0.3rem;
}

.role {
  margin-bottom: 1rem;
}

.header-sidebar {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  width: 100%
  }
.header-sidebar h4{
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
  }
</style>
