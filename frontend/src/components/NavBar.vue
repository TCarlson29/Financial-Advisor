<template>
    <nav v-if="$route.path !== '/'">
    <ul>
      <template v-for="(groupItems, group) in groupedMenus">
        <!-- <li v-if="group" class="group-header">{{ group }}</li> -->
        <li v-for="item in groupItems" :key="item.path">
          <router-link :to="item.path">
            <i :class="`icon-${item.icon}`" /> 
            {{ item.label }}
          </router-link>
        </li>
      </template>
    </ul>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { menuConfig } from '@/router/menuConfig.js'

// sort by order, then group by the `group` key
const sorted = computed(() =>
    [...menuConfig].sort((a, b) => a.order - b.order)
)

// produce an object like { null: [...], Tracker: [...], Reports: [...] }
const groupedMenus = computed(() =>
    sorted.value.reduce((acc, item) => {
        (acc[item.group] ||= []).push(item)
        return acc
    }, {})
)

const route = useRoute()
</script>

<style scoped>
nav {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background: #f0f0f0;
    padding: 10px 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    z-index: 1000;
}

ul {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-wrap: wrap;
}

.group-header {
    width: 100%;
    font-weight: bold;
    margin: 8px 0 4px;
}

li {
    margin-right: 20px;
}

a.router-link-active {
    font-weight: bold;
}
</style>