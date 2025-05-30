<!-- src/components/CategorySelect.vue -->

<template>
  <div class="category-select" v-bind="$attrs">
    <button ref="trigger" type="button" class="dropdown-header" role="combobox" :aria-expanded="String(open)" tabindex="0"
      aria-controls="cat-list" @click="toggle()" @keydown.enter.prevent="toggle()" @keydown.space.prevent="toggle()"
      @keydown.down.prevent="focusItem(0)">
      <span>{{ selected || 'Select a category' }}</span>
      <span class="arrow">{{ open ? '▴' : '▾' }}</span>
    </button>

    <ul v-if="open" id="cat-list" class="dropdown-list" role="listbox" @keydown.escape.prevent="close()"
      @keydown.up.prevent="focusPrev()" @keydown.down.prevent="focusNext()">
      <li v-for="cat in categories" :key="cat.id" role="option" :aria-selected="String(cat.name === selected)"
        tabindex="-1" class="dropdown-item" @click="select(cat.name)" @keydown.enter.prevent="select(cat.name)"
        ref="items">
        <span class="name" tabindex="0">{{ cat.name }}</span>
        <!-- stopPropagation so clicking X doesn’t select -->
        <button type="button" class="del-btn" aria-label="Delete category" @click.stop="removeCategory(cat.id)">×</button>
      </li>
      <li class="dropdown-item add-new" tabindex="0" @keydown.enter.prevent="openAddDialog()"
        @click.stop="showDialog = true, open = false">
        + Add new category…
      </li>
    </ul>

    <div v-if="showDialog" class="modal-backdrop">
      <div class="modal">
        <h3>Add a category</h3>
        <input v-model="newCategory" placeholder="My new category" />
        <div class="buttons">
          <button type="button" @click="confirmAdd" :disabled="!newCategory.trim()">Add</button>
          <button type="button" @click="cancelAdd">Cancel</button>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { defineProps, defineEmits, ref, watch, onMounted,  nextTick } from 'vue'

const props = defineProps({ modelValue: String })
const emit = defineEmits(['update:modelValue'])

const BASE = import.meta.env.VITE_API_BASE_URL
const categories = ref([])
const selected = ref(props.modelValue)
const currentIdx = ref(0)
const open = ref(false)
const showDialog = ref(false)
const newCategory = ref('')
const items = ref([])
const trigger = ref(null)


defineOptions({ inheritAttrs: true })

// keep `selected` in sync with v-model
watch(() => props.modelValue, v => selected.value = v)

// grab all the <li> refs whenever the list re-renders
onMounted(async () => {
  await fetchCategories()
})

// when `open` flips to true, collect your item-refs after the DOM updates
watch(open, async val => {
  if (val) {
    await nextTick()
    items.value = Array.from(
      document.querySelectorAll('.dropdown-list [role=option]')
    )
    focusItem(0)
  }
})

// fetch existing categories
async function fetchCategories() {
  const r = await fetch(`${BASE}/api/categories`)
  categories.value = await r.json() // assume each has {id,name}
}

function toggle() {
  open.value = !open.value
  if (open.value) {
    nextTick(() => focusItem(0))
  }
}

function close() {
  open.value = false
  trigger.value?.focus()
}

// when you select, remember to close()
function select(name) {
  selected.value = name
  emit('update:modelValue', name)
  close()
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
    headers: { 'Content-Type': 'application/json' },
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

function openAddDialog() {
  showDialog.value = true
  open.value = false
}

// keyboard movers
function focusItem(i) {
  const el = items.value[i]
  if (el) el.focus()
  currentIdx.value = i
}
function focusNext() {
  const i = (currentIdx.value + 1) % items.value.length
  focusItem(i)
}
function focusPrev() {
  const i = (currentIdx.value + items.value.length - 1) % items.value.length
  focusItem(i)
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
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
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

.dropdown-item:hover {
  background: #f0f0f0;
}

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
.add-new {
  font-style: italic;
  color: #007bff;
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
  border-radius: 1px;
  min-width: 200px;
}

.modal .buttons {
  margin-top: 0.5rem;
  display: flex;
  justify-content: flex-end;
  color: black;
  gap: 0.5rem;
}

button {
  color: black;
}
</style>
