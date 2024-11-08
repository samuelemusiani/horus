<script setup>
import {defineProps} from 'vue';

const props = defineProps({
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
});
</script>

<template>
  <div class="border shadow-md bg-white dark:bg-gray-800 rounded-lg p-4 m-2 w-11/12">
    <div class="flex items-center space-x-4 p-4 dark:bg-gray-700 rounded-lg">
      <v-icon name="" />
      <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100">{{ device.name }}</h2>
      <p class="text-gray-700 dark:text-gray-300"><strong>IP:</strong> {{
          device.ip
        }}</p>
      <p class="text-gray-700 dark:text-gray-300"><strong>MAC:</strong> {{
          device.mac
        }}</p>
    </div>
    <ul>
      <li v-for="(service, index) in device.services" :key="index"
          class="bg-gray-100 dark:bg-gray-700 p-2 rounded mb-2">
        <p class="text-gray-800 dark:text-gray-200"><strong>Service Name:</strong> {{ service.name }}</p>
        <p class="text-gray-800 dark:text-gray-200"><strong>Port:</strong> {{ service.port }}</p>
        <p class="text-gray-800 dark:text-gray-200"><strong>Vulnerable:</strong> {{
            service.ifVulnerable ? 'Yes' : 'No'
          }}</p>
      </li>
    </ul>
  </div>
</template>