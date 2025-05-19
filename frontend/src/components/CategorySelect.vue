<!-- src/components/CategorySelect.vue -->

<template>
    <div class="category-select">
        <select :value="modelValue" @change="onSelect">
            <option disabled value="">Select a category</option>
            <option value="__add__">+ Add new category…</option>
            <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
        </select>

        <div v-if="showDialog" class="modal-backdrop">
            <div class="modal">
                <h3>Add a category</h3>
                <input v-model="newCategory" placeholder="My new category" />
                <div class="buttons">
                    <button @click="confirmAdd" :disabled="!newCategory.trim()">
                        Add
                    </button>
                    <button @click="cancelAdd">Cancel</button>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
import { defineProps, defineEmits, ref, watch } from 'vue'
import { categories } from '@/config/categories.js'

const props = defineProps({
    modelValue: String
})

const emit = defineEmits(['update:modelValue'])

const BASE = import.meta.env.VITE_API_BASE_URL
const selected = ref(props.modelValue)
const showDialog = ref(false)
const newCategory = ref('')

watch(
    () => props.modelValue,
    val => selected.value = val
)

// POST category
async function createCategory(name) {
    const opts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    }
    return fetch(`${BASE}/api/categories`, opts).then(r => r.json())
}

// DELETE category
async function deleteCategory(id) {
    await fetch(`${BASE}/api/categories/${id}`, { method: 'DELETE' })
    expenses.value = expenses.value.filter(a => a.id !== id)
}


function onSelect(e) {
    const v = e.target.value
    if (v === '__add__') {
        showDialog.value = true
        selected.value = props.modelValue // Undo the select
    } else {
        emit('update:modelValue', v)
    }
}

function confirmAdd() {
    const name = newCategory.value.trim()
    if (!name) return
    categories.value.push(name)
    createCategory(name)
    selected.value = name
    emit('update:modelValue', name) // new selected
    newCategory.value = ''
    showDialog.value = false
}

function cancelAdd() {
    newCategory.value = ''
    showDialog.value = false
}
</script>

<style scoped>
.category-select {
    position: relative;
}

select {
    padding: 0.5em;
    border-radius: 0.25em;
}

.modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal {
    background: white;
    padding: 1rem;
    border-radius: 6px;
    min-width: 200px;
}

.modal .buttons {
    margin-top: 0.5rem;
    display: flex;
    justify-content: flex-end;
    color: black;
    gap: 0.5rem;
}
</style>
