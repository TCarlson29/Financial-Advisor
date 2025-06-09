<script setup>
import { onMounted, ref, computed, reactive, watch } from 'vue'
import CategorySelect from './CategorySelect.vue'
import Charts from './Charts.vue'
const BASE = "http://localhost:8000"

let id = 0
const searchTerm = ref('')
const newName = ref('')
const chosenCategory = ref('')
const newCost = ref('')
const expenses = ref([])
const totalCost = computed(() =>
    expenses.value.reduce((sum, e) => sum + (e.cost ?? 0), 0)
)

const currentlyEditing = ref(false)
const editExpenseId = ref(null)

const filters = reactive({
    name: '',
    category: '',
    cost_min: '',
    cost_max: ''
})

const chartData = computed(() => {
    const map = {}
    for (const expense of expenses.value) {
        const cat = expense.category
        map[cat] = (map[cat] || 0) + expense.cost
    }
    return Object.entries(map).map(([label, value]) => ({ label, value }))
})


async function createExpense(name, category, cost) {
    const opts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, category, cost })
    }
    return fetch(`${BASE}/api/expenses`, opts).then(r => r.json())
}

async function updateExpense(id, name, category, cost) {
    const ops = {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, category, cost })
    }
    const response = await fetch(`${BASE}/api/expenses/${id}`, ops)
    return await response.json()
}

async function deleteExpense(id) {
    await fetch(`${BASE}/api/expenses/${id}`, { method: 'DELETE' })
    expenses.value = expenses.value.filter(a => a.id !== id)
}

async function addExpense() {
    const costNum = parseFloat(newCost.value)
    if (currentlyEditing.value) {
        const updatedExpenses = await updateExpense(
            editExpenseId.value,
            newName.value,
            chosenCategory.value,
            costNum
        )
        const index = expenses.value.findIndex(e => e.id === editExpenseId.value)
        if (index !== -1) expenses.value.splice(index, 1, updatedExpenses)

        currentlyEditing.value = false
        editExpenseId.value = null
    } else {
        const newAct = await createExpense(newName.value, chosenCategory.value, costNum)
        expenses.value.push(newAct)
    }
    newName.value = ''
    chosenCategory.value = ''
    newCost.value = ''
}

function editExpense(expense) {
    newName.value = expense.name
    chosenCategory.value = expense.category
    newCost.value = expense.cost
    currentlyEditing.value = true
    editExpenseId.value = expense.id
}

async function removeExpense(id) {
    await deleteExpense(id)
}

async function fetchExpenses() {
    const url = new URL(`${BASE}/api/expenses`)
    if (filters.name) url.searchParams.set("name", filters.name)
    if (filters.category) url.searchParams.set("category", filters.category)
    if (filters.cost_min) url.searchParams.set("cost_min", filters.cost_min)
    if (filters.cost_max) url.searchParams.set("cost_max", filters.cost_max)

    const res = await fetch(url)
    expenses.value = await res.json()
}


watch(filters, fetchExpenses)

onMounted(async () => {
    await fetchExpenses();
})
</script>

<template>
    <h1>Expenses Tracker</h1>
    <div id="expense-tracker">
        <div class="expense-data">

            <div class="expense-head">
                <form @submit.prevent="addExpense">
                    <input v-model="newName" placeholder="Expense name" required />
                    <CategorySelect v-model="chosenCategory" required />
                    <input class="cost-input" v-model.number="newCost" type="number" step="any" placeholder="Cost"
                        inputmode="decimal" required />
                    <button type="submit" id="add-expense-button">
                        {{ currentlyEditing ? 'Update' : 'Add' }}
                    </button>
                </form>

                <h2>
                    Total: {{ totalCost.toFixed(2) }}
                </h2>
            </div>

            <div class="expense-summary">

                <div class="expense-list">
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Category</th>
                                <th>Cost</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>
                                    <input class="table-filter" v-model="filters.name" placeholder="Search Name" />
                                </td>
                                <td>
                                    <input class="table-filter" v-model="filters.category"
                                        placeholder="Search Category" />
                                </td>
                                <td>
                                    <input class="table-filter table-filter--half" v-model.number="filters.cost_min"
                                        type="number" step="any" placeholder="Min Cost" />
                                    <input class="table-filter table-filter--half" v-model.number="filters.cost_max"
                                        type="number" step="any" placeholder="Max Cost" />
                                </td>
                                <td></td>
                            </tr>
                            <tr v-for="act in expenses" :key="act.id">
                                <td>{{ act.name }}</td>
                                <td>{{ act.category }}</td>
                                <td class="cost-col">{{ act.cost.toFixed(2) }}</td>
                                <td class="action-col">
                                    <button class="action-btn" @click="editExpense(act)">✎</button>
                                    <button class="action-btn" @click="removeExpense(act.id)">🗑</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <div class="expense-chart">
            <Charts :chartInput="chartData" />
        </div>
    </div>
</template>


<style scoped>
html,
body {
    height: 100%;
    margin: 0;
    padding: 0;
    overflow: hidden;
}

#expense-tracker {
    transform: scale(0.8);
    transform-origin: 0 0;
    width: calc(100% / 0.8);
    display: flex;
    flex: 0 0 auto;
    flex-direction: row;
    align-items: center;
    margin: 10px auto;
    padding: 1rem;
}

.expense-data {
    display: flex;
    flex-direction: column;
    align-items: center;
}


form {

    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    border: 2px solid #ccc;
    border-radius: 34px;
    padding: 2rem 1rem;
    background: rgba(255, 255, 255, 0.1);
    z-index: 20;
}

input,
select,
button {
    min-width: 30px;
    padding: 0.5rem;
    border-radius: 5px;
    border: 1px solid #999;
}



#add-expense-button {
    max-width: 80px;
}

.expense-head {
    display: flex;
    flex: 0 0 auto;
    flex-wrap: wrap;
    flex-direction: column;
    align-items: center;
    gap: 0px;
}

.expense-summary {
    display: flex;
    flex: 1 1 auto;
    flex-wrap: wrap;
    flex-direction: row;
    gap: 50px;
}


.expense-list {
    max-height: 250px;
    flex: 3 1 0;
    overflow-y: auto;
    background-color: transparent;
    margin-top: 1rem;
}

.expense-list table {
    width: 98%;
    color: white;
    border-collapse: collapse;
    table-layout: fixed;
}

.expense-list th:nth-child(1),
.expense-list td:nth-child(1) {
    width: 30%;
    /* Name */
}

.expense-list th:nth-child(2),
.expense-list td:nth-child(2) {
    width: 30%;
    /* Category */
}

.expense-list th:nth-child(3),
.expense-list td:nth-child(3) {
    width: 25%;
    /* Cost */
}

.expense-list th:nth-child(4),
.expense-list td:nth-child(4) {
    width: auto;
    /* Actions */
}

.expense-list thead th {
    position: sticky;
    top: 0;
    background: rgb(60, 130, 94);
    z-index: 10;
    border-bottom: 2px solid #ccc;
}

.expense-chart {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    justify-content: center;
    align-items: center;
    flex: 1 1 0;
}

.expense-list .action-col {
    display: table-cell;
    gap: 0.25rem;
    justify-content: center;
    align-items: center;
    white-space: nowrap;
    width: 100%
}

.expense-list .action-col button {
    flex: 1;
    padding: 0.5rem;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    color: white;
    transition: background-color 0.2s;
}

.action-btn {
    width: 50%;
}



.table-filter {
    width: 100%;
    box-sizing: border-box;
    margin-bottom: 0.25rem;
}

.table-filter--half {
    width: calc(50% - 4px);
    display: inline-block;
    margin-right: 8px;
}

.table-filter--half:last-child {
    margin-right: 0;
}

.cost-input {
    text-align: right;
    padding-right: 15px;
}

th.cost-col,
td.cost-col {
    text-align: right;
}

th,
td {
    border: 1px solid #ccc;
    flex-wrap: wrap;
}


input[type=number] {
    -moz-appearance: textfield;
}
</style>