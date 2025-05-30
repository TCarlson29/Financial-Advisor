<template>
  <div class="charts">
    <Bar :data="chartData" :options="chartOptions('Bar Chart of Categories')" />
    <Pie :data="chartData" :options="chartOptions('Pie Chart of Categories')" />
  </div>
</template>

<script>
import { computed } from 'vue'
import { Bar, Pie } from 'vue-chartjs'
import ChartJS from 'chart.js/auto'

// ChartJS.register(Title, Tooltip, Legend, ArcElement, BarElement, CategoryScale, LinearScale)

export default {
  components: { Bar, Pie },
  name: 'Charts',
  props: {
    chartInput: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    const chartData = computed(() => ({
      labels: props.chartInput.map(item => item.label),
      datasets: [
        {
          label: 'Total Cost per Category',
          data: props.chartInput.map(item => item.value),
          backgroundColor: [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
          ]
        }
      ]
    }))

    const chartOptions = (title) => ({
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: { display: true, text: title }
      }
    })

    return { 
        chartData, 
        chartOptions 
    }
  }
}
</script>

<style scoped>
.charts {
  max-width: 400px;
  max-height: 300px;
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  gap: 30px;
  align-self: center;
  justify-content: center;
  margin-top: 2rem;
  color: white;
}
</style>
