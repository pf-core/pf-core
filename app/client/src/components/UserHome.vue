<template>
<div id="home">
</div>
</template>

<style>

</style>

<script>

export default {
  name: 'UserHome',
  data() {
    return {
    };
  },
  methods: {
    getMessage() {
      return 'Home message.'
    },
  },
  created() {
    this.msg = this.getMessage();
  },
};
</script>
