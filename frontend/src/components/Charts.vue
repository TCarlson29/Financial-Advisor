<template>
  <div class="charts">
    <button class="toggle-button" @click="toggleChart">
      Show {{ currentChart === 'bar' ? 'Pie' : 'Bar' }} Chart
    </button>

    <Bar
      v-if="currentChart === 'bar'"
      :data="chartData"
      :options="barChartOptions('Bar Chart of Categories')"
    />
    <Pie
      v-else
      :data="chartData"
      :options="pieChartOptions('Pie Chart of Categories')"
    />
  </div>
</template>

<script>
import { computed, ref } from 'vue'
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

    // Generate distinct colors for each input
    function generateColors(count) {
      const colors = []
      for (let i = 0; i < count; i++) {
        const hue = Math.round((360 * i) / count)
        colors.push(`hsl(${hue}, 70%, 60%)`)
      }
      return colors
    }

    const currentChart = ref('bar')
    const toggleChart = () => {
      currentChart.value = currentChart.value == 'bar' ? 'pie' : 'bar'
    }

    const chartData = computed(() => {
      const labels = props.chartInput.map(item => item.label)
      const data = props.chartInput.map(item => item.value)
      const backgroundColor = generateColors(data.length)

      return {
        labels,
        datasets: [
          {
            label: 'Total Cost per Category',
            data,
            backgroundColor,
            borderColor: 'white',
            borderWidth: 2
          }
        ]
      }
    })

    const barChartOptions = (title) => ({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { 
          position: 'top',
          labels: {
            color: 'white'
          }
        },
        title: { 
          display: true, 
          text: title, 
          color: 'white' 
        }
      },
      scales: {
        x: {
          ticks: {
            color: 'white' 
          },
          grid: {
            color: 'rgb(255, 255, 255, 0.3)'
          }
        },
        y: {
          ticks: {
            color: 'white'
          },
          grid: {
            color: 'rgb(255, 255, 255, 0.3)'
          }
        }
      }
    })

    const pieChartOptions = (title) => ({
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            color: 'white'
          }
        },
        title: {
          display: true,
          text: title,
          color: 'white'
        },
        tooltip: {
          titleColor: 'white',
          bodyColor: 'white',
          backgroundColor: '#333'
        }
      }
    })


    return { 
        chartData, 
        pieChartOptions,
        barChartOptions,
        currentChart,
        toggleChart 
    }
  }
}
</script>

<style scoped>
.charts {
  width: 400px;
  height: 300px;
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  gap: 30px;
  align-self: center;
  justify-content: center;
  margin-top: 2rem;
  color: white;
}

.toggle-button {
  width: 195px;
  height: 50px;
  padding: 0.5rem 1rem;
  background-color: rgb(60, 130, 94);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

</style>
