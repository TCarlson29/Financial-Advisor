<!-- src/components/CategorySelect.vue -->

<template>
    <div class="category-select">
        <div class="dropdown-header" @click="open = !open">
            <span>{{ selected || 'Select a category' }}</span>
            <span class="arrow">{{ open ? '▴' : '▾' }}</span>
        </div>

        <ul v-if="open" class="dropdown-list">
            <li v-for="cat in categories" :key="cat.id" class="dropdown-item" @click="select(cat.name)">
                <span class="name">{{ cat.name }}</span>
                <!-- stopPropagation so clicking X doesn’t select -->
                <button class="del-btn" @click.stop="removeCategory(cat.id)">×</button>
            </li>
            <li class="dropdown-item add-new" @click.stop="showDialog = true, open = false">
                + Add new category…
            </li>
        </ul>

        <div v-if="showDialog" class="modal-backdrop">
            <div class="modal">
                <h3>Add a category</h3>
                <input v-model="newCategory" placeholder="My new category" />
                <div class="buttons">
                    <button @click="confirmAdd" :disabled="!newCategory.trim()">Add</button>
                    <button @click="cancelAdd">Cancel</button>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
import { defineProps, defineEmits, ref, watch, onMounted } from 'vue'

const props = defineProps({ modelValue: String })
const emit  = defineEmits(['update:modelValue'])

const BASE = import.meta.env.VITE_API_BASE_URL
const categories = ref([])
const selected = ref(props.modelValue)
const open = ref(false)
const showDialog = ref(false)
const newCategory= ref('')

// keep `selected` in sync with v-model
watch(() => props.modelValue, v => selected.value = v)

// fetch existing categories
async function fetchCategories() {
  const r = await fetch(`${BASE}/api/categories`)
  categories.value = await r.json() // assume each has {id,name}
}
onMounted(fetchCategories)

// emit selection & close dropdown
function select(name) {
  selected.value = name
  emit('update:modelValue', name)
  open.value = false
}

// call API to delete, then refetch (or splice locally)
async function removeCategory(id) {
  await fetch(`${BASE}/api/categories/${id}`, { method: 'DELETE' })
  await fetchCategories()
}
// call API to create, then refetch + select
async function confirmAdd() {
  const name = newCategory.value.trim()
  if (!name) return
  await fetch(`${BASE}/api/categories`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ name })
  })
  newCategory.value = ''
  showDialog.value = false
  await fetchCategories()
  select(name)
}

function cancelAdd() {
  newCategory.value = ''
  showDialog.value = false
}
</script>

<style scoped>
.category-select {
    position: relative;
    width: 300px;
}

/* header bar */
.dropdown-header {
  padding: 0.5em;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  display: flex; justify-content: space-between;
  background: white;
}

/* the floating menu */
.dropdown-list {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 100%; 
  width: auto;
  background: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-top: 4px;
  max-height: 180px;
  overflow-y: auto;
  z-index: 10;
  list-style: none;
  padding: 0;
  white-space: nowrap; 
}

.dropdown-item {
  padding: 0.4em 0.6em;
  cursor: pointer;
  display: flex; 
  justify-content: space-between;
  white-space: nowrap; 
}
.dropdown-item:hover { background: #f0f0f0; }

/* delete button */
.del-btn {
  border: none;
  background: transparent;
  font-size: 1em;
  line-height: 1;
  cursor: pointer;
  color: #900;
}

/* add-new row styling */
.add-new { font-style: italic; color: #007bff; }


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
