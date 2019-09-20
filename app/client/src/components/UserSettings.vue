<template>
    <div class="container">
    <div class="row">
      <div class="col-12" id="serverBoard">
          <hr>
        <h4 class="request_board">Connections</h4>
        <hr>
      </div>
    </div>
     <div class="row dashboardRow">
        <div class="col-4">
            <vs-card color="dark">
                <div slot="header">
                  Server
                </div>
                <!--  Request Card Info -->
                <div class="row buttonRow">
                <vs-button class="updateButton" ref="serverButton" color="gray" @click="testServerConnection()">Ping</vs-button>
                    </div>
                <div slot="footer">
                  <vs-row vs-justify="flex-end">
                    <vs-chip class="connectedChip" color="#4eb3d3" v-if="server_connected">
                        Connected
                   </vs-chip>
                      <vs-chip class="connectedChip" color="gray" v-if="!server_connected">
                        Not connected
                   </vs-chip>
                      <vs-chip class="connectedChip" color="#4eb3d3" v-if="server_error">
                        Sockets failed
                   </vs-chip>
                  </vs-row>
                </div>
            </vs-card>
        </div>
         <div class="col-4">
            <vs-card color="dark">
                <div slot="header">
                  MongoDB @ Server
                </div>
                <!--  Request Card Info -->
                <div class="row buttonRow">
                <vs-button class="updateButton" color="gray" @click="testDatabaseConnection()">Ping</vs-button>
                    </div>
                <div slot="footer">
                  <vs-row vs-justify="flex-end">
                    <vs-chip class="connectedChip" color="#4eb3d3" v-if="database_connected">
                        Connected
                   </vs-chip>
                      <vs-chip class="connectedChip" color="gray" v-if="!database_connected">
                        Not connected
                   </vs-chip>
                      <vs-chip class="connectedChip" color="#4eb3d3" v-if="server_error">
                        Sockets failed
                   </vs-chip>
                  </vs-row>
                </div>
            </vs-card>
        </div>
    </div>
    </div>
</template>

<script>

export default {
  name: 'UserSettings',
  data() {
    return {

        // Server
        server_connected: false,
        server_error: false,

        // Database on server
        database_connected: false,


    }
  },
  sockets: {
      connect_error() {
          this.server_connected = false;
          this.database_connected = false;
          this.server_error = true;
      },
      // Polling sockets continuously

      server_pong() {
          if (!this.server_connected){
            this.server_connected = true;
            this.notify('Server connected.', 'black')
          }
      },

      db_pong(data) {
          if (data.connected){
            this.database_connected = true;
            this.notify('Database connected.', 'black')
          } else {
              this.database_connected = false;
              this.notify('Database failed to connect.', 'red')
          }
      }

  },
  methods: {

      notify(msg, color) {
        this.$vs.notify({
            text: msg,
            color: color,
            position: 'bottom-right',
            time: 1000,
          });
      },


      // Test connection methods:

      testDatabaseConnection() {
          this.database_connected = false;
          this.$socket.emit('db_ping')
      },
      testServerConnection() {

          this.$vs.loading({
            background: '#fff',
            color: "#000",
            type: "point",

          });
          setTimeout( ()=> {
            this.$vs.loading.close()
          }, 2000);

        this.server_connected = false;
        this.$socket.emit('server_ping')
      }
  },
  created() {
      this.$socket.emit('server_ping')
  },
};
</script>


<style>
.dashboardRow {
    margin-top:3rem;
    margin-bottom:3rem;
}
.buttonRow {
    margin-top: 2rem;
    margin-left: 5.5rem;
}

.updateButton {
    width: 60%;
}

.connectedChip{
    margin-top: 2rem
}

</style>
