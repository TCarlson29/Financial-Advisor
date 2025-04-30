<script setup>
import { onMounted, ref } from 'vue'

let id = 0
const newName = ref('')
const newAmount = ref(0)
const activities = ref([])

// POST activity
async function createActivity(name, amount) {
    const opts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, amount })
    }
    return fetch('http://localhost:8000/api/activities', opts).then(r => r.json())
}

// DELETE activity
async function deleteActivity(id) {
    await fetch(`http://localhost:8000/api/activities/${id}`, { method: 'DELETE' })
    activities.value = activities.value.filter(a => a.id !== id)
}

async function addActivity() {
  const newAct = await createActivity(newName.value, newAmount.value)
  activities.value.push(newAct)
  newName.value = ''
  newAmount.value = 0
}

async function removeActivity(id) {
  await deleteActivity(id)
}

onMounted(async () => {
    await fetchActivities();
})

// GET activities
async function fetchActivities() {
    const res = await fetch('http://localhost:8000/api/activities')
    activities.value = await res.json()
}
</script>

<template>
    <div id="finance-tracker">
        <form @submit.prevent="addActivity">
            <input v-model="newName" placeholder="Activity name" required />
            <input v-model.number="newAmount" type="number" placeholder="Amount" required />
            <button type="submit">Add</button>
        </form>

        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Amount</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="act in activities" :key="act.id">
                    <td>{{ act.name }}</td>
                    <td>{{ act.amount.toFixed(2) }}</td>
                    <td>
                        <button @click="removeActivity(act.id)">❌</button>
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