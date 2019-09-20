<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10" id="docInfo">
        <br><br><br><br>
        <hr>
          <vue-markdown>### Documentation</vue-markdown>\
          <hr>
      </div>
    </div>
  </div>
</template>

<script>

import VueMarkdown from 'vue-markdown'

export default {
  name: 'MainDocs',
    components: {
    'vue-markdown': VueMarkdown
    },
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      return 'Docs message.'
    }
  },
  created() {
    this.msg = this.getMessage();
  },
};
</script>

<style>
  #docInfo {
    margin-top: 20px;
  }
  .card {
    margin-top: 10px;
  }
</style>
