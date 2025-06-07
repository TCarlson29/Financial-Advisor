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
    background-color: var(--site-bg-color);
    padding: 0; 
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    z-index: 1000;
}

ul {
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    width: 100%;
}

li {
    flex: 1;
}

a {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 50px;
    color: inherit;
    text-decoration: none;
    transition: background-color 0.3s ease;
    width: 100%;
}

a:hover {
    background-color: rgba(60, 130, 94, 0.4);
}

a.router-link-active {
    background-color: rgba(60, 130, 94, 0.7);
    font-weight: bold;
    color: white;
}
</style>