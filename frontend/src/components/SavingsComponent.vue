<script setup>
import { onMounted, ref, computed } from 'vue'
const BASE = "http://localhost:8000"

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
    final = Math.floor(final)

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
            <div id="savings-numbers">
                <div id="savings-data">
                    <div id="savings-plan-name">
                        Savings Plan:
                        <input v-model="newName" placeholder="Enter label" required />
                    </div>
                    <div id="savings-amount">
                        Amount of saved money:
                        <input v-model.number="newAmount" type="number" step="any" min="0" max="1000000000"
                            placeholder="0.00" required />
                    </div>
                    <div id="time-saved">
                        Saving Duration:
                        <input v-model.number="newTimeSaved" type="number" step="any" min="0" max="150" placeholder="0" required />

                        <select v-model="newTimeSavedUnit" required>
                            <option disabled value=""> Time Unit</option>
                            <option v-for="u in timeUnits" :key="u" :value="u"> {{ u }}(s)</option>
                        </select>
                    </div>
                    <div id="savings-rate">
                        Rates of interest (%):
                        <input v-model.number="newRate" type="number" step="any" min="0" max="30" placeholder="0.00" required />

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
            </div>

            <button type="submit" id="add-saving-button">Add Plan</button>
        </form>

        <div class="saving-list">
            <table>
                <thead>
                    <tr>
                        <th>Plan</th>
                        <th class="money-col">Saved</th>
                        <th>For</th>
                        <th>At</th>
                        <th class="money-col">Final</th>
                        <th class="money-col">Gain</th>
                        <th class="del-col">Remove</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="s in savings" :key="s.id">
                        <td>{{ s.name }}</td>
                        <td class="money-col">{{ s.amount.toFixed(2) }}</td>
                        <td>{{ s.time_saved }} {{ s.time_saved_unit }} (s)</td>
                        <td>{{ s.rate }}% per {{ s.rate_time_unit }} ({{ s.rate_type }})</td>
                        <td class="money-col">{{ s.final.toFixed(2) }}</td>
                        <td class="money-col">
                            <span :class="{ exceeded: s.gain < 0 }">
                                {{ s.gain.toFixed(2) }}
                            </span>
                        </td>
                        <td class="del-col">
                            <button class="action-btn" @click="removeSaving(s.id)">X</button>
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
    width: 100%;
    max-width: 1000px;
    margin: 0 auto 1rem;
    align-self: center;
    flex-direction: column;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    border: 2px solid #ccc;
    border-radius: 34px;
    color: white;
    padding: 2rem 1rem;
    background: rgba(255, 255, 255, 0.1);
}

#savings-numbers {
    display: flex;
    justify-content: space-between;
    width: 100%;
}

#savings-data,
#calculated-data {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    width: 100%;
    gap: 1rem;
}

#savings-data {
    flex: 2;
    margin-right: 1rem;
    align-items: flex-start;
}

#calculated-data {
    flex: 1;
    align-items: flex-end;
}

input,
select,
button {
    min-width: 30px;
    padding: 0.5rem;
    /* text-align: center; */
    /* center the placeholder / typed text */
    border-radius: 5px;
    border: 1px solid #999;
}


#add-saving-button {
    max-width: 80px;
    align-self: center;
}

/* this is your scrollable container */
.saving-list {
    width: 100%;
    margin: 0 auto;
    max-height: 350px;
    max-width: 80%;
    align-self: center;
    /* take up all remaining space */
    overflow-y: auto;
    /* scroll only when needed */
    /* optional visual styling */
    background-color: #507f57;
    color: white;
    border-top: 1px solid #ddd;
    margin-top: 1rem;
}

/* make the table fill its wrapper */
.saving-list table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
}

.saving-list thead th {
    position: sticky;
    top: 0;
    background: rgb(60, 130, 94);
    z-index: 10;
    border-bottom: 2px solid #ccc;
}

.saving-list .money-col {
    text-align: right;
}

.saving-list .del-col {
    max-width: 500px;
}

.action-btn{
    width:25%;
}

th,
td {
    border: 1px solid #ccc;
    padding: 0.5rem;
}

.exceeded {
    color: red;
    font-weight: bold;
}

input[type=number] {
    -moz-appearance: textfield;
}
</style>