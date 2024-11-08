<template>
  <div class="border shadow-md bg-white  rounded-lg p-4 w-full">
    <div class="flex items-center justify-between gap-2">
      <div class="flex items-center">
        <v-icon :class="[{'-rotate-90': !expanded}, 'hover:cursor-pointer']" name="md-expandmore-round" scale="1.5" fill="gray" class="mr-2" @click.stop="expanded=!expanded"/>
        <v-icon v-if="isVulnerable" name="md-error" fill="red" scale="1.5"/>
        <v-icon v-else name="bi-check-circle-fill" fill="green" scale="1.5"/>
        <h2 class="text-2xl font-bold text-gray-900 mx-2">{{ device.name }}</h2>
      </div>
      <div class="flex gap-2 items-center text-sm">
        <p class="text-gray-700 "><strong>IP:</strong> {{ device.ip }}</p>
        <p class="text-gray-700"><strong>MAC:</strong> {{ device.mac }}</p>
      </div>
    </div>
    <ul class="flex gap-2 mt-3" v-if="expanded">
      <li v-for="(service, index) in sortedServices" :key="index" :class="['px-4 py-2 rounded-lg mb-2', service.ifVulnerable ? 'bg-red-100' : 'bg-green-50']">
        <p class="text-gray-800"><strong>Service:</strong> {{ service.name }}</p>
        <p class="text-gray-800"><strong>Port:</strong> {{ service.port }}</p>
        <p class="text-gray-800"><strong>Vulnerable:</strong> {{ service.ifVulnerable ? 'Yes' : 'No' }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    device: {
      type: Object,
      required: true,
      validator: (value) => {
        return (
          value.name &&
          value.ip &&
          value.mac &&
          Array.isArray(value.services) &&
          value.services.every(service =>
            service.port &&
            service.ifVulnerable !== undefined &&
            service.name
          )
        );
      }
    }
  },
  data() {
    return {
      expanded: false
    };
  },
  computed: {
    isVulnerable() {
      return this.device.services.some(service => service.ifVulnerable);
    },
    sortedServices() {
      return this.device.services.sort((a, b) => b.ifVulnerable - a.ifVulnerable);
    }
  }
};
</script>
