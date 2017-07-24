
      var link = '/services/'

      var app = new Vue({
      el: '#app',
      delimiters: ['[[', ']]'],
      data: {
        message: 'Hello Vue!'
      },
      methods: {

        getServices: function(){

            this.$http.get()

        }


      }

    })