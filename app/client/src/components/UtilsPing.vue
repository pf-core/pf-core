<template>
  <div class="container">
    <button type="button" class="btn btn-primary">{{ msg }}</button>
  </div>
</template>

<script>

export default {
  name: 'UtilsPing',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {

    },
  },
  created() {
    this.getMessage();
  },
};
</script>
