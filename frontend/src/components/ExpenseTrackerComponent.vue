<script setup>
import { onMounted, ref } from 'vue'

let id = 0
const newName = ref('')
const newCategory = ref('')
const newCost = ref(0)
const expenses = ref([])

// POST expense
async function createExpense(name, category, cost) {
    const opts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, category, cost })
    }
    return fetch('http://localhost:8000/api/expenses', opts).then(r => r.json())
}

// DELETE expense
async function deleteExpense(id) {
    await fetch(`http://localhost:8000/api/expenses/${id}`, { method: 'DELETE' })
    expenses.value = expenses.value.filter(a => a.id !== id)
}

async function addExpense() {
    const newAct = await createExpense(
        newName.value,
        newCategory.value,
        newCost.value
    );
    expenses.value.push(newAct)
    newName.value = ''
    newCategory.value = ''
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
    const res = await fetch('http://localhost:8000/api/expenses')
    expenses.value = await res.json()
}
</script>

<template>
    <div id="finance-tracker">
        <form @submit.prevent="addExpense">
            <input v-model="newName" placeholder="Expense name" required />
            <CategorySelect v-model="newCategory" />
            <input v-model.number="newCost" type="number" placeholder="Cost" required />
            <button type="submit">Add</button>
        </form>

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
                <tr v-for="act in expenses" :key="act.id">
                    <td>{{ act.name }}</td>
                    <td>{{ act.category }}</td>
                    <td>{{ act.cost.toFixed(2) }}</td>
                    <td>
                        <button @click="removeExpense(act.id)">❌</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>


<style scoped>
/* Sayfayı ortala */
body {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
}

/* Formu ortala ve oval çerçeve ekle */
form {
    display: flex;
    padding-left: 12px;
    padding-right: 12px;
    margin-bottom: 23px;
    flex-direction: column;
    align-items: center;
    border: 2px solid #ccc;
    border-radius: 34px;
    padding-top: 34px;
    padding-bottom: 34px;
    background-color: transparent;
}

input {
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 5px;
    color: black;
    /* Metin rengini siyah olarak ayarla */
}




#inptBtn {
    border-radius: 23px;
    height: 59px;
    margin-bottom: 5%;
    width: 89%;
    background: transparent;
    color: white;
}


#addBtn {
    width: 50%;
    border: 1px solid white !important;
}


button {
    padding: 10px;
    background-color: transparent;
    color: white;
    border: none;
    padding: 12px;
    border-radius: 12px;
    cursor: pointer;
}

button:hover {
    background-color: #aaaaaa23;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    padding: 10px;
    border: 1px solid #ffffff4a;
    border-radius: 23px;
    background-color: #fff;
    color: rgb(255, 255, 255);
    /* Metin rengini siyah olarak ayarla */
    background-color: transparent;
}
</style>