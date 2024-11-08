<template>
  <AuroraBackground class="flex flex-col h-screen w-screen items-center">
    <main class="flex flex-col h-full justify-center items-center gap-20">
      <div class="flex items-center justify-center gap-4">
        <img :src="eyeIcon" alt="icon" class="w-28 h-28">
        <h1 class="text-6xl font-black">Horus</h1>
      </div>
      <button class="bg-black rounded-r-full rounded-l-full text-white px-10 py-4 mt-20 pulse font-bold text-xl">Start
        Scan
      </button>
    </main>
  </AuroraBackground>
</template>

<script>
import eyeIcon from '@/assets/eye_icon.png';
import AuroraBackground from "@/components/AuroraBackground.vue";

export default {
  components: {
    AuroraBackground,
    Meteors,
  },
  data() {
    return {
      eyeIcon,
    };
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