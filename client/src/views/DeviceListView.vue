<template>
  <div class="flex flex-col h-screen w-screen items-center">
    <main class="flex flex-col w-full h-full justify-center items-center gap-2">
      <DeviceComponent v-for="device in devices" :key="device.id" :device="device" />
    </main>
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
            { port: 22, ifVulnerable: true, name: "SSH" }
          ]
        },
        {
          id: 2,
          name: "Device 2",
          ip: "192.168.1.2",
          mac: "00:1A:2B:3C:4D:5F",
          services: [
            { port: 443, ifVulnerable: false, name: "HTTPS" },
            { port: 21, ifVulnerable: true, name: "FTP" }
          ]
        }
      ]
    }
  },
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