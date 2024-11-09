<template>
  <div class="h-screen w-screen">
    <AuroraBackground />
    <main id="main" class="absolute inset-0 flex flex-col h-5/6 justify-center items-center gap-20 p-10 z-10">
      <div class="flex items-center justify-center gap-4">
        <img :src="eyeIcon" alt="icon" class="w-32 h-32">
        <div class="flex flex-col">
          <h1 id="title" class="font-black text-8xl">Horus</h1>
          <h3 class="text-2xl ml-2 text-gray-800">Network analysis for everyone</h3>
        </div>
      </div>
      <div class="flex flex-col justify-center items-center mt-10">
        <div
          class="flex justify-center items-center gap-2 px-6 py-2 rounded-r-full rounded-l-full bg-white border-2 border-black">
          <v-icon v-if="networkName === 'Ethernet'" id="cable-icon" name="md-cable" scale="1.75" />
          <v-icon v-else id="wifi-icon" name="io-wifi" scale="1.75" />
          <h3 class="text-xl"> {{ networkName }} </h3>
        </div>
        <div class="text-center rounded-lg bg-slate-100 p-4 mt-4 text-gray-600 border-2 border-gray-300 shadow-md">
          <p>We have found your network!</p> 
          <p>Click the button below to start scanning for devices.</p>
        </div>
      </div>
      <button
        class="hover:cursor-pointer bg-black rounded-r-full rounded-l-full text-white px-10 py-4 mt-20 pulse font-bold text-xl"
        @click.stop="startScan">
        Start scan
      </button>
    </main>
    <Loader v-if="displayLoader"
      class="absolute w-full inset-0 flex flex-col h-5/6 justify-center items-center gap-20 p-10 z-10"
      :messages="['Scanning network...', 'Detecting devices...', 'Analyzing vulnerabilities...']" />
  </div>
</template>

<script>
import eyeIcon from '@/assets/eye_icon.png';
import AuroraBackground from "@/components/AuroraBackground.vue";
import Loader from "@/components/Loader.vue";
import axios from "axios";
import router from "@/router/index.js";
import { useRouter } from "vue-router";

export default {
  components: {
    AuroraBackground,
    Loader
  },
  data() {
    return {
      eyeIcon,
      networkName: "",
      displayLoader: false,
      router: useRouter()
    };
  },
  methods: {
    async scanFetcher() {
      const response = await axios.get("http://localhost:8000/scan")
      response.data.scan !== "[]" ? await router.push("/list") : setTimeout(() => this.scanFetcher(), 2000);
    },
    startScan() {
      axios.post("http://localhost:8000/start")
      document.querySelector("#main").remove();
      this.displayLoader = true;
      setTimeout(() => this.scanFetcher(), 2000);
    }
  },
  mounted() {
    axios.get("http://localhost:8000/ssid")
      .then(response => {
        this.networkName = response.data;
      })
      .catch(error => {
        console.error(error);
        this.networkName = "Unknown";
      });
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