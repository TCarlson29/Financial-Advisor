<script setup>
import { onMounted, ref, reactive, computed } from 'vue'

const expenses = ref([])
const budgets = reactive({})

// load all expenses on mount
onMounted(async () => {
    const BASE = import.meta.env.VITE_API_BASE_URL
    const [expRes, budRes] = await Promise.all([
        fetch(`${BASE}/api/expenses`),
        fetch(`${BASE}/api/budgets`),
    ])
    expenses.value = await expRes.json()
    const budget_cat_limit = await budRes.json()
    budget_cat_limit.forEach(b => { budgets[b.category] = b.limit })
})

// compute total spent per category
const totalsByCategory = computed(() => {
    return expenses.value.reduce((acc, { category, cost }) => {
        acc[category] = (acc[category] || 0) + cost
        return acc
    }, /** start with an empty object **/ {})
})

// save whenever a budget input changes
async function saveBudget(cat) {
    const payload = { category: cat, limit: budgets[cat] }
    await fetch('/api/budgets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    })
}

</script>

<template>
    <div id="budget-component">
        <h2>Budget Totals by Category</h2>
        <table>
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Total Spent</th>
                    <th>Planned Budget</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <!-- loop over computed totals -->
                <tr v-for="(total, category) in totalsByCategory" :key="category">
                    <td>{{ category }}</td>
                    <td>{{ total.toFixed(2) }}</td>
                    <td>
                        <input type="number" min="0" v-model.number="budgets[category]" @change="saveBudget(category)"
                            placeholder="0.00" />
                    </td>
                    <td>{{ total <= (budgets[category] || 0) ? 'Within' : 'Exceeded' }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<style scoped>
#budget-component {
    max-width: 600px;
    margin: auto;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th,
td {
    padding: 0.5rem;
    border: 1px solid #ccc;
}
</style>