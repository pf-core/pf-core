<template>
  <div class="container">
    <a>{{ msg }}</a>
  </div>
</template>

<script>

export default {
  name: 'MainAbout',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      return 'About message.'
    },
  },
  created() {
    this.msg = this.getMessage();
  },
};
</script>
