<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-20">
    <div class="bg-white rounded-lg overflow-hidden w-1/2">
      <div class="p-4 border-b">
        <slot name="header"></slot>
      </div>
      <div class="p-4">
        <slot name="body"></slot>
      </div>
      <div class="p-4 border-t flex justify-end">
        <slot name="footer"></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  emits: ['close'],
  methods: {
    close() {
      this.$emit('close');
    }
  }
};
</script>