<template>
  <div class="w-screen flex flex-col items-center">
    <div class="flex flex-col h-screen w-screen items-center max-w-5xl p-4">
      <h1 class="mt-10 text-4xl w-full font-black">Report</h1>
      <h1 class="text-4xl w-full font-black mt-10">Found devices</h1>
      <main class="flex flex-col w-full h-full items-center gap-2 mt-6">
      <DeviceComponent v-for="device in sortedDevices" :key="device.id" :device="device" />
    </main>
  </div>
  </div>
</template>

<script>
import DeviceComponent from "@/components/DeviceComponent.vue";

export default {
  components: {
    DeviceComponent,
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
      ]
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