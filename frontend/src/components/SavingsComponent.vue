<script setup>
import { onMounted, ref, computed } from 'vue'
const BASE = import.meta.env.VITE_API_BASE_URL

let id = 0
const timeUnits = ["Month", "Year"]
const rateTypes = ["Simple", "Compound"]
const savings = ref([])

const newName = ref('')
const newAmount = ref(0)
const newTimeSaved = ref(0)
const newTimeSavedUnit = ref('')
const newRate = ref(0)
const newRateTimeUnit = ref('')
const newRateType = ref('')

const finalAmount = computed(() => {
    const t = calculateFinalAmount(
        newAmount.value,
        newTimeSaved.value,
        newTimeSavedUnit.value,
        newRate.value,
        newRateTimeUnit.value,
        newRateType.value
    )
    return Number.isNaN(t) ? 0 : t
})

const gain = computed(() => {
    const t = finalAmount.value - newAmount.value
    return Number.isNaN(t) ? 0 : t
})

function getTimeSavedInMonths(timeSaved, timeSavedUnit) {
    if (timeSavedUnit === "Month") {
        return timeSaved
    } else if (timeSavedUnit === "Year") {
        return timeSaved * 12
    }
}

function getTimeSavedInYears(timeSaved, timeSavedUnit) {
    if (timeSavedUnit === "Month") {
        return timeSaved / 12
    } else if (timeSavedUnit === "Year") {
        return timeSaved
    }
}

function getCorrectTimeSaved(timeSaved, timeSavedUnit, rateTimeUnit) {
    let correctTimeSaved = 0
    if (rateTimeUnit === "Year") {
        correctTimeSaved = getTimeSavedInYears(timeSaved, timeSavedUnit)
    } else if (rateTimeUnit === "Month") {
        correctTimeSaved = getTimeSavedInMonths(timeSaved, timeSavedUnit)
    }
    if (correctTimeSaved < 1) {
        correctTimeSaved = 0
    }
    return correctTimeSaved
}

function calculateFinalAmount(principal, timeSaved, timeSavedUnit, percentRate, rateTimeUnit, rateType) {
    const correctTimeSaved = getCorrectTimeSaved(timeSaved, timeSavedUnit, rateTimeUnit)
    const rate = percentRate / 100
    let final = 0

    if (rateType === "Simple") {
        final = principal * (1 + rate * correctTimeSaved)
    } else if (rateType === "Compound") {
        final = principal * Math.pow((1 + rate), correctTimeSaved)
    }

    return final
}

// POST saving
async function createSaving(
    name,
    amount,
    time_saved,
    time_saved_unit,
    rate,
    rate_time_unit,
    rate_type,
    final,
    gain
) {
    const opts = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name,
            amount,
            time_saved,
            time_saved_unit,
            rate,
            rate_time_unit,
            rate_type,
            final,
            gain
        })
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
        newRateTimeUnit.value,
        newRateType.value,
        finalAmount.value,
        gain.value
    );
    savings.value.push(newSave)
    newName.value = ''
    newAmount.value = 0
    newTimeSaved.value = 0
    newTimeSavedUnit.value = ''
    newRate.value = 0
    newRateTimeUnit.value = ''
    newRateType.value = ''
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
            <div id="savings-data">
                <div id="savings-plan-name">
                    Savings Plan:
                    <input v-model="newName" placeholder="Enter label" required />
                </div>
                <div id="savings-amount">
                    Amount of saved money:
                    <input v-model.number="newAmount" type="number" placeholder="0.00" required />
                </div>
                <div id="time-saved">
                    Saving Duration:
                    <input v-model.number="newTimeSaved" type="number" placeholder="Time Saved" required />

                    <select v-model="newTimeSavedUnit" required>
                        <option disabled value=""> Time Unit</option>
                        <option v-for="u in timeUnits" :key="u" :value="u"> {{ u }}(s)</option>
                    </select>
                </div>
                <div id="savings-rate">
                    Rates of interest (%):
                    <input v-model.number="newRate" type="number" placeholder="Rate" required />

                    <select v-model="newRateTimeUnit" required>
                        <option disabled value=""> Time Unit</option>
                        <option v-for="u in timeUnits" :key="u" :value="u">per {{ u }}</option>
                    </select>

                    <select v-model="newRateType" required>
                        <option disabled value="">Rates Type</option>
                        <option v-for="t in rateTypes" :key="t" :value="t">{{ t }}</option>
                    </select>
                </div>
            </div>
            <div id="calculated-data">
                <div id="savings-calculated-amount">
                    Calculated Amount:
                    <input type="number" :value="finalAmount.toFixed(2)" disabled />
                </div>
                <div id="savings-gain">
                    Gain:
                    <input type="number" :value="gain.toFixed(2)" disabled />
                </div>
            </div>
            <button type="submit" id="add-saving-button">Add Plan</button>
        </form>

        <div class="saving-list">
            <table>
                <thead>
                    <tr>
                        <th>Plan</th>
                        <th>Saved</th>
                        <th>For</th>
                        <th>At</th>
                        <th>Final</th>
                        <th>Gain</th>
                        <th>Remove</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="s in savings" :key="s.id">
                        <td>{{ s.name }}</td>
                        <td>{{ s.amount.toFixed(2) }}</td>
                        <td>{{ s.time_saved }} {{ s.time_saved_unit }} (s)</td>
                        <td>{{ s.rate }}% per {{ s.rate_time_unit }} ({{ s.rate_type }})</td>
                        <td>{{ s.final.toFixed(2) }}</td>
                        <td>
                            <span :class="{ exceeded: s.gain < 0 }">
                                {{ s.gain.toFixed(2) }}
                            </span>
                        </td>
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

.exceeded { color: red; font-weight: bold; }
</style>