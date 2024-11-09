<template>
  <div class="w-screen flex flex-col items-center pb-8">
    <div class="flex flex-col w-screen items-center max-w-5xl p-4">
      <div class="flex w-full mt-10 items-end">
        <h1 class=" text-4xl font-black">Report</h1>
        <hr>
      </div>
      <div class="flex w-full gap-4">
        <ReportComponent :devices="devices" />
      </div>
      <div class="flex w-full mt-12 items-end">
        <h1 class="flex-2 text-4xl font-black">Found devices</h1>
        <hr class="flex-1">
      </div>
      <main class="flex flex-col w-full h-full items-center gap-2 mt-8">
        <DeviceComponent v-for="device in sortedDevices" :key="device.id" :device="device" @open-chat="openChat"/>
      </main>
    </div>
  </div>
  <ChatComponent v-if="showChat" :initial-message="initialMessage" style="position: fixed; bottom: 20px; right: 20px;" @close="closeChat" />
</template>

<script>
import DeviceComponent from "@/components/DeviceComponent.vue";
import ReportComponent from "@/components/ReportComponent.vue";
import ChatComponent from "@/components/ChatComponent.vue";

export default {
  components: {
    DeviceComponent,
    ReportComponent,
    ChatComponent
  },
  data() {
    return {
      devices: [
        {
          id: 1,
          name: "Device 1",
          ip: "192.168.1.1",
          mac: "00:1A:2B:3C:4D:5E",
          services: [
            { port: 80, ifVulnerable: false, name: "HTTP" },
            { port: 22, ifVulnerable: false, name: "SSH" }
          ]
        },
        {
          id: 2,
          name: "Device 2",
          ip: "192.168.1.2",
          mac: "00:1A:2B:3C:4D:5F",
          services: [
            { port: 443, ifVulnerable: true, name: "HTTPS" },
            { port: 21, ifVulnerable: false, name: "FTP" }
          ]
        }
      ],
      showChat: false,
      initialMessage: []
    }
  },
  methods: {
    openChat(service){
      this.initialMessage = ['user', `Explain to me what ${service.name} is.`];
      this.showChat = true;
    },
    closeChat(){
      this.showChat = false;
  }
},
  computed: {
    sortedDevices() {
      return this.devices.sort((a, b) => {
        const aVulnerable = a.services.some(service => service.ifVulnerable);
        const bVulnerable = b.services.some(service => service.ifVulnerable);
        return bVulnerable - aVulnerable;
      });
    }
  }
}

</script>

<style scoped>
.pulse {
  animation: pulse-animation 2s infinite;
}

@keyframes pulse-animation {
  0% {
    box-shadow: 0 0 0 0px rgba(0, 0, 0, 0.2);
  }

  100% {
    box-shadow: 0 0 0 20px rgba(0, 0, 0, 0);
  }
}

hr {
  border: 1px solid black;
  margin-bottom: 0.4em;
  margin-left: 0.5em;
  width: 100%;
}
</style>