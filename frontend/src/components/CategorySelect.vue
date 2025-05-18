<!-- src/components/CategorySelect.vue -->
<script setup>
import { defineProps, defineEmits } from 'vue'
import { CATEGORIES } from '@/config/categories.js'

const props = defineProps({
  modelValue: String
})

const emit = defineEmits(['update:modelValue'])

function onChange(e) {
  emit('update:modelValue', e.target.value)
}
</script>

<template>
  <select :value="modelValue" @change="onChange">
    <option disabled value="">Select a category</option>
    <option v-for="c in CATEGORIES" :key="c" :value="c">{{ c }}</option>
  </select>
</template>

<style scoped>
select {
  padding: 0.5em;
  border-radius: 0.25em;
}
</style>
