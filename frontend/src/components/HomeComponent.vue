<template>
    <div id='theContainer'>
      <h1> Welcome</h1>
      <h2>  Financial Advisor  </h2>
      <router-link to="/expense-tracker">
        <button style="margin: 23px; width: 24%;">Open</button>
      </router-link>
    </div>
  </template>
  
  <style>
  body {
    background: linear-gradient(135deg, #0e4a18, #1577296b);
  }
  #theContainer {
    text-align: center;
    margin: 23px;
    padding: 23px;
  }
  h1 {
      text-align: center;
      margin-top: 45px;
      margin-bottom: 45px;
      color: white;
      width: 100%;
  }
  h2 {
    text-align: center;
    margin-bottom: 24px;
    font-weight: lighter;
    font-family: system-ui;
    color: white;
  }
  button {
      width: 50%;
      border: 1px solid white !important;
      padding: 10px;
      background-color: transparent;
      color: white;
      border: none;
      padding: 12px;
      border-radius: 12px;
      cursor: pointer;
    }
  </style>