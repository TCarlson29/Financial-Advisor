<script setup>
import { onMounted, ref, computed, reactive, watch } from 'vue'
import { debounce } from 'lodash-es';
import Decimal from 'decimal.js'
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

const isEditing = ref(false)
const editSavingsId = ref(null)

const finalD = computed(() => {
    return calculateFinalAmount(
        newAmount.value,
        newTimeSaved.value,
        newTimeSavedUnit.value,
        newRate.value,
        newRateTimeUnit.value,
        newRateType.value
    )
})

const gainD = computed(() =>
    finalD.value.minus(newAmount.value)
)

function getTimeSavedInMonths(timeSaved, timeSavedUnit) {
    const t = new Decimal(timeSaved)
    return timeSavedUnit === 'Year'
        ? t.times(12)
        : t
}

function getTimeSavedInYears(timeSaved, timeSavedUnit) {
    const t = new Decimal(timeSaved)
    return timeSavedUnit === 'Month'
        ? t.dividedBy(12)
        : t
}

function getCorrectTimeSaved(timeSaved, timeSavedUnit, rateTimeUnit) {
    let n = rateTimeUnit === 'Year'
        ? getTimeSavedInYears(timeSaved, timeSavedUnit)
        : getTimeSavedInMonths(timeSaved, timeSavedUnit)

    n = n.floor()

    return n
}

function calculateFinalAmount(
    principal,
    timeSaved,
    timeSavedUnit,
    percentRate,
    rateTimeUnit,
    rateType
) {
    const P = new Decimal(principal)
    const r = new Decimal(percentRate).dividedBy(100)
    const n = getCorrectTimeSaved(timeSaved, timeSavedUnit, rateTimeUnit)

    let finalD
    if (rateType === 'Simple') {
        // A = P × (1 + r × n)
        finalD = P.times(Decimal(1).plus(r.times(n)))
    } else {
        // A = P × (1 + r)^n
        finalD = P.times(Decimal(1).plus(r).pow(n))
    }

    return finalD
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
    finalD,
    gainD
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
            final: finalD.value.toString(),
            gain: gainD.value.toString()
        })
    }
    return fetch(`${BASE}/api/savings`, opts).then(r => r.json())
}

// PUT savings
async function updateSavings(
    id,
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
    const ops = {
        method: 'PUT',
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
    const response = await fetch(`${BASE}/api/savings/${id}`, ops)
    return await response.json()
}

// DELETE saving
async function deleteSaving(id) {
    await fetch(`${BASE}/api/savings/${id}`, { method: 'DELETE' })
    savings.value = savings.value.filter(a => a.id !== id)
}


async function addSaving() {
    if (isEditing.value) {
        await updateSavings(
            editSavingsId.value,
            newName.value,
            newAmount.value,
            newTimeSaved.value,
            newTimeSavedUnit.value,
            newRate.value,
            newRateTimeUnit.value,
            newRateType.value,
            finalAmount.value,
            gain.value
        )

        const index = savings.value.findIndex(s => s.id === editSavingsId.value)
        if (index !== -1) {
            savings.value[index] = {
                id: editSavingsId.value,
                name: newName.value,
                amount: newAmount.value,
                time_saved: newTimeSaved.value,
                time_saved_unit: newTimeSavedUnit.value,
                rate: newRate.value,
                rate_time_unit: newRateTimeUnit.value,
                rate_type: newRateType.value,
                final: finalAmount.value,
                gain: gain.value
            }
        }

        isEditing.value = false
        editSavingsId.value = null
    } else {
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
        )
        savings.value.push(newSave)
    }

    clearForm()
}


async function removeSaving(id) {
    await deleteSaving(id)
}


const filters = reactive({
    name: '',
    time_saved_unit: '',
    rate_time_unit: '',
    rate_type: '',

    amount_min: '',
    amount_max: '',
    time_saved_min: '',
    time_saved_max: '',
    rate_min: '',
    rate_max: '',
    final_min: '',
    final_max: '',
    gain_min: '',
    gain_max: ''
})


// GET savings
async function fetchSavings() {
    const url = new URL(`${BASE}/api/savings`);

    // string filters
    if (filters.name) url.searchParams.set("name", filters.name);
    if (filters.time_saved_unit) url.searchParams.set("time_saved_unit", filters.time_saved_unit);
    if (filters.rate_time_unit) url.searchParams.set("rate_time_unit", filters.rate_time_unit);
    if (filters.rate_type) url.searchParams.set("rate_type", filters.rate_type);

    // numeric range filters: only set if not empty
    if (filters.amount_min !== "") url.searchParams.set("amount_min", filters.amount_min);
    if (filters.amount_max !== "") url.searchParams.set("amount_max", filters.amount_max);
    if (filters.time_saved_min !== "") url.searchParams.set("time_saved_min", filters.time_saved_min);
    if (filters.time_saved_max !== "") url.searchParams.set("time_saved_max", filters.time_saved_max);
    if (filters.rate_min !== "") url.searchParams.set("rate_min", filters.rate_min);
    if (filters.rate_max !== "") url.searchParams.set("rate_max", filters.rate_max);
    if (filters.final_min !== "") url.searchParams.set("final_min", filters.final_min);
    if (filters.final_max !== "") url.searchParams.set("final_max", filters.final_max);
    if (filters.gain_min !== "") url.searchParams.set("gain_min", filters.gain_min);
    if (filters.gain_max !== "") url.searchParams.set("gain_max", filters.gain_max);

    const res = await fetch(url.toString());
    savings.value = await res.json();
}

const debouncedFetch = debounce(fetchSavings, 300);
watch(filters, debouncedFetch);

onMounted(async () => {
    await fetchSavings();
})

// Populate form while editing
function editSaving(saving) {
    newName.value = saving.name
    newAmount.value = saving.amount
    newTimeSaved.value = saving.time_saved
    newTimeSavedUnit.value = saving.time_saved_unit
    newRate.value = saving.rate
    newRateTimeUnit.value = saving.rate_time_unit
    newRateType.value = saving.rate_type
    isEditing.value = true
    editSavingsId.value = saving.id
}

// Clear form after editing
function clearForm() {
    newName.value = '';
    newAmount.value = 0;
    newTimeSaved.value = 0;
    newTimeSavedUnit.value = '';
    newRate.value = 0;
    newRateTimeUnit.value = '';
    newRateType.value = '';
    isEditing.value = false;
    editSavingsId.value = null;
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
                        <input v-model.number="newTimeSaved" type="number" step="any" min="0" max="150" placeholder="0"
                            required />

                        <select v-model="newTimeSavedUnit" required>
                            <option disabled value=""> Time Unit</option>
                            <option v-for="u in timeUnits" :key="u" :value="u"> {{ u }}(s)</option>
                        </select>
                    </div>
                    <div id="savings-rate">
                        Rates of interest (%):
                        <input v-model.number="newRate" type="number" step="any" min="0" max="30" placeholder="0.00"
                            required />

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
                        <input type="text" :value="finalD.toFixed(2)" disabled />
                    </div>
                    <div id="savings-gain">
                        Gain:
                        <input type="text" :value="gainD.toFixed(2)" disabled />
                    </div>
                </div>
            </div>

            <button type="submit" id="add-saving-button">{{ isEditing ? 'Update Plan' : 'Add Plan' }}</button>
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
                        <th class="act-col">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <!-- Plan name filter -->
                        <td>
                            <input class="table-filter" v-model="filters.name" placeholder="Search Plan" />
                        </td>

                        <!-- Saved amount min/max -->
                        <td>
                            <input class="table-filter table-filter--half" v-model.number="filters.amount_min"
                                type="number" step="any" placeholder="Min Saved" />
                            <input class="table-filter table-filter--half" v-model.number="filters.amount_max"
                                type="number" step="any" placeholder="Max Saved" />
                        </td>

                        <!-- Time saved min/max -->
                        <td>
                            <input class="table-filter table-filter--half" v-model.number="filters.time_saved_min"
                                type="number" step="any" placeholder="Min Duration" />
                            <input class="table-filter table-filter--half" v-model.number="filters.time_saved_max"
                                type="number" step="any" placeholder="Max Duration" />
                        </td>

                        <!-- Rate min/max -->
                        <td>
                            <input class="table-filter table-filter--half" v-model.number="filters.rate_min"
                                type="number" step="any" placeholder="Min Rate" />
                            <input class="table-filter table-filter--half" v-model.number="filters.rate_max"
                                type="number" step="any" placeholder="Max Rate" />
                        </td>

                        <!-- Final amount min/max -->
                        <td>
                            <input class="table-filter table-filter--half" v-model.number="filters.final_min"
                                type="number" step="any" placeholder="Min Final" />
                            <input class="table-filter table-filter--half" v-model.number="filters.final_max"
                                type="number" step="any" placeholder="Max Final" />
                        </td>

                        <!-- Gain min/max -->
                        <td>
                            <input class="table-filter table-filter--half" v-model.number="filters.gain_min"
                                type="number" step="any" placeholder="Min Gain" />
                            <input class="table-filter table-filter--half" v-model.number="filters.gain_max"
                                type="number" step="any" placeholder="Max Gain" />
                        </td>

                        <!-- Remove column has no filter -->
                        <td></td>
                    </tr>
                    <tr v-for="s in savings" :key="s.id">
                        <td>{{ s.name }}</td>
                        <td class="money-col">{{ s.amount.toFixed(2) }}</td>
                        <td>{{ s.time_saved }} {{ s.time_saved_unit }} (s)</td>
                        <td>{{ s.rate }}% per {{ s.rate_time_unit }} ({{ s.rate_type }})</td>
                        <td class="money-col">{{ s.final }}</td>
                        <td class="money-col">
                            <span :class="{ exceeded: s.gain < 0 }">
                                {{ s.gain }}
                            </span>
                        </td>
                        <td class="act-col">
                            <button @click="editSaving(s)">Edit</button>
                            <button @click="removeSaving(s.id)">Remove</button>
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

.saving-list .act-col {
    display: flex;
    gap: 0.5rem;
    justify-content: center;
    align-items: center;
}

.saving-list .act-col button {
    min-width: 35px;
    padding: 0.5rem;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    color: white;
    transition: background-color 0.2s;
}

.action-btn {
    width: 25%;
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