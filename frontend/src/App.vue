<!-- src/App.vue -->
<script setup>
import HeaderComponent from './components/HeaderComponent.vue'
import { useRoute } from 'vue-router'
import NavBar from './components/NavBar.vue'

const route = useRoute()
</script>

<template>
  <div id="app">
    <NavBar v-if="route.path !== '/'" />
    <router-view/>
  </div>
</template>



<style>
#app {
  display: block;
  width: 100%;
  margin: 0 auto;
  margin-bottom: 23px;
  padding: 0rem;
  padding-top: 60px;
  font-weight: normal;
  text-align: center;
}

header {
  text-align: center;
  color: white;
}

body {
  background: linear-gradient(135deg, var(--colorPrimary), #4e085f);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  margin: 0;
}
</style>
