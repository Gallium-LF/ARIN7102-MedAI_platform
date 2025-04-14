<template>
  <a-row :gutter="[16, 16]">
    <a-col :span="6" v-for="kpi in kpis" :key="kpi.title">
      <a-card :bordered="false">
        <div class="kpi-title">{{ kpi.title }}</div>
        <div class="kpi-value">{{ kpi.value }}</div>
        <div class="kpi-sub" v-if="kpi.subtitle">{{ kpi.subtitle }}</div>
      </a-card>
    </a-col>
  </a-row>
</template>

<script lang="ts" setup>
const kpis = [
  {
    title: "Total Users",
    value: 1549,
    subtitle: "Rows in dataset",
  },
  {
    title: "Purchase Rate",
    value: "43.2%",
    subtitle: "Users who purchased",
  },
  {
    title: "Avg Time on Website",
    value: "30.47 min",
    subtitle: "Time spent browsing",
  },
  {
    title: "Loyalty Members",
    value: "32.6%",
    subtitle: "Enrolled in loyalty program",
  },
];
</script>

<style scoped>
.kpi-title {
  font-size: 14px;
  font-weight: 500;
  color: #888;
}
.kpi-value {
  font-size: 26px;
  font-weight: bold;
  margin: 8px 0;
}
.kpi-sub {
  font-size: 13px;
  color: #aaa;
}
</style>
