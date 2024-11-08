<template>
  <div class="w-screen flex flex-col items-center">
    <div class="flex flex-col h-screen w-screen items-center max-w-5xl p-4">
      <div v-if="isScanning">
        <Loader />
        <p>Scan is still ongoing</p>
      </div>
      <h1 class="mt-10 text-4xl w-full font-black">Report</h1>
      <h1 class="text-4xl w-full font-black mt-10">Found devices</h1>
      <main class="flex flex-col w-full h-full items-center gap-2 mt-6">
        <DeviceComponent v-for="device in sortedDevices" :key="device.id" :device="device"/>
      </main>
    </div>
  </div>
</template>

<script>
import DeviceComponent from "@/components/DeviceComponent.vue";
import axios from "axios";
import Loader from "@/components/Loader.vue";

export default {
  components: {
    Loader,
    DeviceComponent,
  },
  data() {
    return {
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
};

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
</style>