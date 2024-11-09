<template>
  <div class="border shadow-md bg-white  rounded-lg p-4 w-full">
    <div class="flex items-center justify-between gap-2">
      <div class="flex items-center">
        <v-icon :class="[{ '-rotate-90': !expanded }, 'hover:cursor-pointer']" name="md-expandmore-round" scale="1.5"
                fill="gray" class="mr-2" @click.stop="expanded = !expanded"/>
        <v-icon v-if="isVulnerable" name="md-error" fill="red" scale="1.5"/>
        <v-icon v-else name="bi-check-circle-fill" fill="green" scale="1.5"/>
        <h2 class="text-2xl font-bold text-gray-900 mx-2">{{ device.name }}</h2>
      </div>
      <div class="flex gap-2 items-center">
        <button @click="openModal" class="bg-blue-500 text-white pl-2 pr-4 py-2 rounded-lg items-center flex">
          <v-icon name="md-search" scale="1.5" class="mr-2"/>
          Find
        </button>
      </div>
    </div>
    <div v-if="expanded">
      <div class="flex w-full gap-4 mt-3 ml-1">
        <p class="text-gray-700"><strong>IP:</strong> {{ device.ip }}</p>
        <p class="text-gray-700"><strong>MAC:</strong> {{ device.mac }}</p>
      </div>
      <ul class="flex gap-2 mt-3 flex-wrap">
        <li v-for="(service, index) in sortedServices" :key="index"
            :class="['px-4 py-2 rounded-lg mb-2 flex', service.ifVulnerable ? 'bg-red-100' : 'bg-green-50']">
          <div>
            <p class="text-gray-800"><strong>Service:</strong> {{ service.name }}</p>
            <p class="text-gray-800"><strong>Version:</strong> {{ service.version }}</p>
            <p class="text-gray-800"><strong>Port:</strong> {{ service.port }}</p>
            <p class="text-gray-800"><strong>Vulnerable:</strong> {{ service.ifVulnerable ? 'Yes' : 'No' }}</p>
          </div>
          <div class="ml-8 flex flex-col items-center justify-center">
            <button :class="[service.ifVulnerable ? 'bg-red-400' : 'bg-green-400', 'p-3 rounded-lg']" @click="openChat(service)">
              <v-icon name="md-questionanswer" fill="white"/>
            </button>
          </div>
        </li>
      </ul>
    </div>
    <ModalComponent v-if="showModal" @close="closeModal">
      <template v-slot:header>
        <h3 class="text-lg font-bold text-gray-700">Find The Device (IP: {{ device.ip }})</h3>
      </template>
      <template v-slot:body>
        <Loader :messages="['Contacting the server...']" class="w-full py-16" v-if="loading"/>
        <div v-else>
          <ol class="list-decimal list-inside space-y-2">
            <li>Make a list of all the devices that could potentially be the one you're looking for.</li>
            <li>Disconnect one device from your network that you think might be the culprit.</li>
            <li>Use the "Scan" feature to check if the device is online.</li>
            <li>If the device is still found, go back to step 2 and try disconnecting another device.</li>
            <li>Continue this process until the scan feature says it's no longer online in the results.</li>
          </ol>
          <div class="flex gap-2 align-center">
            <button @click="scanDevice" class="bg-blue-500 text-white px-4 py-2 rounded mt-4">
              <v-icon name="md-networkcheck" fill="white"/>
              Scan
            </button>
            <div v-if="scanResult"
                 :class="[scanResult === 'offline' ? 'text-emerald-500': 'text-red-500', 'mt-4 bg-gray-200 px-4 py-2 rounded']">
              Scan Result: <span
                :class="['font-bold', 'text-lg']">{{
                scanResult
              }}</span></div>
          </div>
        </div>
      </template>
      <template v-slot:footer>
        <button @click="closeModal" class="bg-gray-500 text-white px-4 py-2 rounded">Close</button>
      </template>
    </ModalComponent>
  </div>
</template>

<script>
import ModalComponent from "@/components/ModalComponent.vue";
import axios from "axios";
import Loader from "@/components/Loader.vue";

export default {
  emits: ['open-chat'],
  components: {
    Loader,
    ModalComponent
  },
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
                service.name &&
                service.version
            )
        );
      }
    }
  },
  data() {
    return {
      expanded: false,
      scanResult: null,
      showModal: false,
      loading: false,
    };
  },
  computed: {
    isVulnerable() {
      return this.device.services.some(service => service.ifVulnerable);
    },
    sortedServices() {
      return this.device.services.sort((a, b) => b.ifVulnerable - a.ifVulnerable);
    },
  },
  methods: {
    openModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.scanResult = null;
    },
    async scanDevice() {
      try {
        this.loading = true;
        const response = await axios.get(`http://localhost:8000/isonline/${this.device.ip}`);
        this.scanResult = response.data.status;
      } catch (error) {
        this.scanResult = 'error';
      }
      this.loading = false;
    },
    openChat(service) {
      this.$emit('open-chat', service);
    }
  }
};
</script>
