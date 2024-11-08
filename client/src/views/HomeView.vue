<template>
  <div class="flex flex-col h-screen w-screen items-center">
    <main class="flex flex-col h-full justify-center items-center gap-20">
      <div class="flex items-center justify-center gap-4">
        <img :src="eyeIcon" alt="icon" class="w-20 h-20">
      <h1 class="text-5xl font-black">Horus</h1>
      </div>
    <button class="bg-black rounded-r-full rounded-l-full text-white px-10 py-3 mt-20 pulse font-bold text-lg">Start Scan</button>
    </main>
  </div>
</template>

<script>
import eyeIcon from '@/assets/eye_icon.png';

export default {
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