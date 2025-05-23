<script setup>
import { onMounted, ref, computed } from 'vue'
const BASE = import.meta.env.VITE_API_BASE_URL

let id = 0
const newName = ref('')
const chosenCategory = ref('')
const newCost = ref(0)
const expenses = ref([])
const totalCost = computed(() =>
    expenses.value.reduce((sum, e) => sum + (e.cost ?? 0), 0)
)

const maxRows = ref(7);
// expense list row height for styling
const rowHeightPx = 40;

// POST expense
async function createExpense(name, category, cost) {
    const opts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, category, cost })
    }
    return fetch(`${BASE}/api/expenses`, opts).then(r => r.json())
}

// DELETE expense
async function deleteExpense(id) {
    await fetch(`${BASE}/api/expenses/${id}`, { method: 'DELETE' })
    expenses.value = expenses.value.filter(a => a.id !== id)
}

async function addExpense() {
    const newAct = await createExpense(
        newName.value,
        chosenCategory.value,
        newCost.value
    );
    expenses.value.push(newAct)
    newName.value = ''
    chosenCategory.value = ''
    newCost.value = 0
}

async function removeExpense(id) {
    await deleteExpense(id)
}

onMounted(async () => {
    await fetchExpenses();
})

// GET expenses
async function fetchExpenses() {
    const res = await fetch(`${BASE}/api/expenses`)
    expenses.value = await res.json()
}
</script>

<template>
    <div id="expense-tracker">
        <h1>Expenses Tracker</h1>
        <form @submit.prevent="addExpense">
            <input v-model="newName" placeholder="Expense name" required />
            <CategorySelect v-model="chosenCategory" required />
            <input v-model.number="newCost" type="number" placeholder="Cost" required />
            <button type="submit" id="add-expense-button">Add</button>
        </form>

        <h2>
            Total: {{ totalCost.toFixed(2) }}
        </h2>
        <div class="expense-list">
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
                    <tr v-for="act in expenses" :key="act.id">
                        <td>{{ act.name }}</td>
                        <td>{{ act.category }}</td>
                        <td>{{ act.cost.toFixed(2) }}</td>
                        <td>
                            <button @click="removeExpense(act.id)">X</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

    </div>
</template>


<style scoped>
#expense-tracker {
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

input, select, button {
  /* give them all the same base sizing */
  min-width: 120px;
  padding: 0.5rem;
  text-align: center;    /* center the placeholder / typed text */
  border-radius: 5px;
  border: 1px solid #999;
}


#add-expense-button {
  max-width: 80px;
}

/* this is your scrollable container */
.expense-list {
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
.expense-list table {
    width: 100%;
    border-collapse: collapse;
}

.expense-list thead th {
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