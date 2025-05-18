<script setup>
import { onMounted, ref, computed } from 'vue'
import CategorySelect from './CategorySelect.vue'
import { useRoute } from 'vue-router'

const expenses = ref([])

// load all expenses on mount
onMounted(async () => {
    const res = await fetch('http://localhost:8000/api/expenses')
    expenses.value = await res.json()
})

// compute a map of { category → totalCost }
const totalsByCategory = computed(() => {
    return expenses.value.reduce((acc, { category, cost }) => {
        acc[category] = (acc[category] || 0) + cost
        return acc
    }, /** start with an empty object **/ {})
})
</script>

<template>
    <div id="budget-component">
        <h2>Budget Totals by Category</h2>
        <table>
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Total Spent</th>
                </tr>
            </thead>
            <tbody>
                <!-- 3) loop over your computed totals -->
                <tr v-for="(total, category) in totalsByCategory" :key="category">
                    <td>{{ category }}</td>
                    <td>{{ total.toFixed(2) }}</td>
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