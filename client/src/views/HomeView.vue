<template>
  <div class="h-screen w-screen">
    <!--<AuroraBackground/>-->
    <main id="main" class="flex flex-col h-full justify-center items-center gap-20 p-10 z-10">
      <div class="flex items-center justify-center gap-4">
        <img :src="eyeIcon" alt="icon" class="w-28 h-28">
        <h1 class="text-6xl font-black">Horus</h1>
      </div>
      <div class="flex justify-center items-center gap-2 px-6 py-2 rounded-r-full rounded-l-full bg-gray-500 text-white">
        <v-icon id="wifi-icon" name="io-wifi" scale="1.75"/>
        <h3 class="text-xl"> {{ networkName }} </h3>
      </div>
      <button class="hover:cursor-pointer bg-black rounded-r-full rounded-l-full text-white px-10 py-4 mt-20 pulse font-bold text-xl" @click.stop="startScan">
        Start Scan
      </button>
    </main>
    <Loader v-if="displayLoader" :messages="['Scanning network...', 'Detecting devices...', 'Analyzing vulnerabilities...']"/>
  </div>
</template>

<script>
import eyeIcon from '@/assets/eye_icon.png';
import AuroraBackground from "@/components/AuroraBackground.vue";
import Loader from "@/components/Loader.vue";

export default {
  components: {
    AuroraBackground,
    Loader
  },
  data() {
    return {
      eyeIcon,
      networkName: "Network Name",
      displayLoader: false
    };
  },
  methods: {
    startScan() {
      console.log("Scanning network...");
      document.querySelector("#main").remove();
      this.displayLoader = true;
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