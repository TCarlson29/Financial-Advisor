<script setup>
import { onMounted, ref, computed } from 'vue'
const BASE = import.meta.env.VITE_API_BASE_URL

let id = 0
const newName = ref('')
const newAmount = ref(0)
const newTimeSaved = ref(0)
const newTimeSavedUnit = ref('')
const newRate = ref(0)
const newRateType = ref('')
const newRateTimeUnit = ref('')
const savings = ref([])

const totalCost = computed(() =>
    savings.value.reduce((sum, e) => sum + (e.cost ?? 0), 0)
)

// POST saving
async function createSaving(name, category, cost) {
    const opts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, category, cost })
    }
    return fetch(`${BASE}/api/savings`, opts).then(r => r.json())
}

// DELETE saving
async function deleteSaving(id) {
    await fetch(`${BASE}/api/savings/${id}`, { method: 'DELETE' })
    savings.value = savings.value.filter(a => a.id !== id)
}

async function addSaving() {
    const newSave = await createSaving(
        newName.value,
        newAmount.value,
        newTimeSaved.value,
        newTimeSavedUnit.value,
        newRate.value,
        newRateType.value,
        newRateTimeUnit.value
    );
    savings.value.push(newSave)
    newName.value = ''
    newAmount.value = 0
    newTimeSaved.value = 0
    newTimeSavedUnit.value = ''
    newRate.value = 0
    newRateType.value = ''
    newRateTimeUnit.value = ''
}

async function removeSaving(id) {
    await deleteSaving(id)
}

onMounted(async () => {
    await fetchSavings();
})

// GET savings
async function fetchSavings() {
    const res = await fetch(`${BASE}/api/savings`)
    savings.value = await res.json()
}
</script>

<template>
    <div id="savings-tracker">
        <h1>Savings Tracker</h1>
        <form @submit.prevent="addSaving">
            <div id = "savings-data">
                <input v-model="newName" placeholder="Saving name" required />
                <input v-model.number="newAmount" type="number" placeholder="Amount" required />
                <input v-model.number="newTimeSaved" type="number" placeholder="Time Saved" required />
                <input v-model="newTimeSavedUnit" placeholder="Time Saved Unit" required />
                <input v-model.number="newRate" type="number" placeholder="Rate" required />
                <input v-model="newRateType" placeholder="Rate Type" required />
                <input v-model="newRateTimeUnit" placeholder="Rate Time Unit" required />
            </div>
            <div id="calculated-data">
            </div>
            <button type="submit" id="add-saving-button">Add</button>
        </form>

        <h2>
            Total: {{ totalCost.toFixed(2) }}
        </h2>
        <div class="saving-list">
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Category</th>
                        <th>Cost</th>
                        <th>Remove</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="s in savings" :key="s.id">
                        <td>{{ s.name }}</td>
                        <td>{{ s.category }}</td>
                        <td>{{ s.cost.toFixed(2) }}</td>
                        <td>
                            <button @click="removeSaving(s.id)">X</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

    </div>
</template>


<style scoped>
#saving-tracker {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 10px auto;
    padding: 1rem;
}


form {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    /* flex-direction: row; */
    border: 2px solid #ccc;
    border-radius: 34px;
    padding: 2rem 1rem;
    background: rgba(255, 255, 255, 0.1);
}

input,
select,
button {
    /* give them all the same base sizing */
    min-width: 120px;
    padding: 0.5rem;
    text-align: center;
    /* center the placeholder / typed text */
    border-radius: 5px;
    border: 1px solid #999;
}


#add-saving-button {
    max-width: 80px;
}

/* this is your scrollable container */
.saving-list {
    max-height: 350px;
    flex: 1 1 auto;
    /* take up all remaining space */
    overflow-y: auto;
    /* scroll only when needed */
    /* optional visual styling */
    border-top: 1px solid #ddd;
    margin-top: 1rem;
}

/* make the table fill its wrapper */
.saving-list table {
    width: 100%;
    border-collapse: collapse;
}

.saving-list thead th {
    position: sticky;
    top: 0;
    background: white;
    z-index: 10;
    border-bottom: 2px solid #ccc;
}

th,
td {
    border: 1px solid #ccc;
    padding: 0.5rem;
}
</style>