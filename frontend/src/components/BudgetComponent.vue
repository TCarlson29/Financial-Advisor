<script setup>
import { onMounted, ref, reactive, computed } from 'vue'

const BASE = "http://localhost:8000"
const expenses = ref([])
const budgets = reactive({})
const categories = ref([])

// load all expenses on mount
onMounted(async () => {
    const [expRes, budRes, catRes] = await Promise.all([
        fetch(`${BASE}/api/expenses`),
        fetch(`${BASE}/api/budgets`),
        fetch(`${BASE}/api/categories`)
    ])
    expenses.value = await expRes.json()
    const budget_cat_limit = await budRes.json()
    budget_cat_limit.forEach(b => { budgets[b.category] = b.limit })
    categories.value = await catRes.json()
    categories.value = categories.value.map(c => c.name)
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
    const res = await fetch(`${BASE}/api/budgets`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    if (!res.ok) {
        console.error('Budget save failed:', await res.text())
    } else {
        const saved = await res.json()
        budgets[saved.category] = saved.limit
    }
}


</script>

<template>
    <div id="budget-component">
        <h2>Budget Planning by Category</h2>
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
                <tr v-for="cat in categories" :key="cat">
                    <td>{{ cat }}</td>
                    <!-- use 0 if there’s no entry yet -->
                    <td>{{ (totalsByCategory[cat] || 0).toFixed(2) }}</td>
                    <td>
                        <input type="number" min="0" v-model.number="budgets[cat]" @change="saveBudget(cat)"
                            placeholder="0.00" />
                    </td>
                    <td :class="{
                        'exceeded': (totalsByCategory[cat] || 0) > (budgets[cat] || 0)
                    }">
                        <!-- within or exceeded -->
                        <template v-if="(totalsByCategory[cat] || 0) <= (budgets[cat] || 0)">
                            Within
                        </template>
                        <template v-else>
                            Exceeded By {{ ((totalsByCategory[cat] || 0) - (budgets[cat] || 0)).toFixed(2) }}
                        </template>
                    </td>
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
    color: white;
    background-color: #507f57;
    border-collapse: collapse;
}

th,
td {
    padding: 0.5rem;
    border: 1px solid #ccc;
}

th {
    background: rgb(60, 130, 94);
}

.exceeded {
  color: red;
  font-weight: bold;
}

input[type=number] {
  -moz-appearance: textfield;
  text-align: right;
  padding-right: 15px;
}
</style>