<template>
        <div>
    <full-page ref="fullpage" :options="options" id="fullpage">
    <div class="section" id="section1">
          <div id="slide1">
                <img src="../assets/hexlogin.png" alt="HexLogin" style="width:12%">
              <p style="margin-top: 3rem">Template</p>
                <div class="login_wrapper">
                    <div class="login_field">
                        <vs-input label-placeholder="User" v-model="email" color="dark" type="email" icon="face"></vs-input>
                    </div>
                    <div class="login_field">
                        <vs-input label-placeholder="Password" v-model="password" color="dark" icon="lock" type="password"></vs-input>
                    </div>
                </div>
                <div class="login_wrapper">

                    <div class="login_button">
                        <vs-button line-origin="left" color="dark" type="line" @click="login">Login</vs-button>
                    </div>
                </div>
        </div>
    </div>
        <div class="section" id="section2">
      Third section ...
    </div>
        <div class="section" id="section3">
      Fourth section ...
    </div>
  </full-page>
        </div>
</template>

<script>


import firebase from 'firebase/app';

export default {
  name: 'PublicLogin',
  data() {
    return {
      msg: '',
      email: '',
      password: '',
        options: {
            verticalCentered: true,
            resize: true,
            scrollingSpeed: 700,
            easing: 'easeInQuart',
            loopBottom: true,
            loopTop: false,
            menu: true,
            css: true,
      },
    };
  },
  methods: {
    login() {
      this.$vs.loading({
          color: 'dark'
      });
      firebase.auth().signInWithEmailAndPassword(this.email, this.password).then(
          () => { // Arrow functions inherits this from scope
            this.$vs.loading.close();
            this.$vs.notify({
                text: 'Login successful!',
                color: 'dark',
                position: 'bottom-right',
                time: 2000,
            });
            this.$router.replace('home');
            this.$parent.navbar = true;
          },
          (err) => {
            this.$vs.loading.close();
            this.$vs.notify({
                text: err,
                color: 'dark',
                position: 'bottom-right',
                time: 2000,
            })
          }
      );
    },
  },
  created() {
      this.$parent.$data.navbar = false;
  },
};
</script>

<style>


/* Defining each section background and styles
* --------------------------------------- */

#section1 {
    margin-top: 10rem;
}


.login_wrapper {
    text-align: center;
}
.login_field {
    display: inline-block;
    margin: 1rem;
}
.login_button {
    display: inline-block;
    margin: 1rem;
}
</style>
