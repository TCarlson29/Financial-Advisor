<template>
  <select v-model="selected">
    <option disabled value="">— select category —</option>
    <option
      v-for="cat in categories"
      :key="cat.value"
      :value="cat.value"
    >
      {{ cat.label }}
    </option>
  </select>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
  categories: {
    type: Array,
    default: () => [
      { value: 'food', label: 'Food' },
      { value: 'transport', label: 'Transport' },
      { value: 'entertainment', label: 'Entertainment' },
      // …any defaults you like
    ]
  }
})

const emit = defineEmits(['update:modelValue'])

// keep an internal ref in sync with the outside v-model
const selected = ref(props.modelValue)

watch(() => props.modelValue, v => {
  selected.value = v
})

watch(selected, v => {
  emit('update:modelValue', v)
})
</script>

<style scoped>
select {
  padding: 0.5em;
  border-radius: 0.25em;
}
</style>
