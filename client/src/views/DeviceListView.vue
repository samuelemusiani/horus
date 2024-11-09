<template>

  <div class="w-screen flex flex-col items-center pb-8">
    <div class="flex flex-col w-screen items-center max-w-5xl p-4">
      <div v-if="isScanning">
        <div class="flex gap-6 justify-center items-center">
          <span class="loader"></span>
          <p class="text-lg">Scan is still ongoing</p>
        </div>
      </div>
      <div class="flex w-full mt-10 items-end">
        <h1 class=" text-4xl font-black">Report</h1>
        <hr>
      </div>
      <div class="flex w-full gap-4">
        <ReportComponent :devices="filteredDevices"/>
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
  <ChatComponent v-if="showChat" :initial-message="initialMessage" style="position: fixed; bottom: 20px; right: 20px;"
                 @close="closeChat"/>
</template>

<script>
import DeviceComponent from "@/components/DeviceComponent.vue";
import axios from "axios";
import Loader from "@/components/Loader.vue";
import ReportComponent from "@/components/ReportComponent.vue";
import ChatComponent from "@/components/ChatComponent.vue";

export default {
  components: {
    Loader,
    DeviceComponent,
    ReportComponent,
    ChatComponent
  },
  data() {
    return {
      showChat: false,
      initialMessage: [],
      devices: [],
      isScanning: false
    }
  },
  mounted() {
    this.getScan();
  },
  watch: {
    isScanning(newValue) {
      if (newValue) {
        setTimeout(() => this.getScan(), 2000);
      }
    }
  },
  methods: {
    async getScan() {
      const response = await axios.get("http://localhost:8000/scan");
      this.isScanning = response.data.status;
      this.devices = JSON.parse(response.data.scan);
      if (this.isScanning)
        setTimeout(() => this.getScan(), 2000);
    },
    openChat(service) {
      this.initialMessage = ['user', `Explain to me what ${service.name} is.`];
      this.showChat = true;
    },
    closeChat() {
      this.showChat = false;
    }
  },
  computed: {
    sortedDevices() {
      return this.filteredDevices.sort((a, b) => {
        const aVulnerable = a.services.some(service => service.ifVulnerable);
        const bVulnerable = b.services.some(service => service.ifVulnerable);
        return bVulnerable - aVulnerable;
      });
    },
    filteredDevices() {
      return this.devices.map(device => {
        const uniqueServices = new Map();
        device.services.forEach(service => {
          const key = `${service.name}-${service.port}-${service.version}`;
          if (!uniqueServices.has(key) || service.ifVulnerable) {
            uniqueServices.set(key, service);
          }
        });
        return {
          ...device,
          services: Array.from(uniqueServices.values())
        };
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
