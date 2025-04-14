<template>
  <a-row :gutter="[16, 16]">
    <a-col :span="6">
      <a-card>
        <div class="kpi-title">Total Sales</div>
        <div class="kpi-value">€ {{ totalSales.toLocaleString() }}</div>
        <div class="kpi-sub">All sales across stores</div>
      </a-card>
    </a-col>
    <a-col :span="6">
      <a-card>
        <div class="kpi-title">Total Customers</div>
        <div class="kpi-value">{{ totalCustomers.toLocaleString() }}</div>
        <div class="kpi-sub">Customers served</div>
      </a-card>
    </a-col>
    <a-col :span="6">
      <a-card>
        <div class="kpi-title">Avg Sales per Store</div>
        <div class="kpi-value">€ {{ avgSalesPerStore.toFixed(2) }}</div>
        <div class="kpi-sub">Sales divided by unique stores</div>
      </a-card>
    </a-col>
    <a-col :span="6">
      <a-card>
        <div class="kpi-title">Promo Day Avg Sales</div>
        <div class="kpi-value">€ {{ promoAvgSales.toFixed(2) }}</div>
        <div class="kpi-sub">When promo = 1</div>
      </a-card>
    </a-col>
  </a-row>
</template>

<script lang="ts" setup>
// 这些数据可从父组件或 API 中获取
const totalSales = 5873180623;
const totalCustomers = 644041755;
const avgSalesPerStore = 5267426.57; // 假设有 1115 家门店
const promoAvgSales = 8228.28;
</script>

<style scoped>
.kpi-title {
  font-weight: 500;
  color: #888;
  margin-bottom: 6px;
}
.kpi-value {
  font-size: 26px;
  font-weight: bold;
  color: #222;
}
.kpi-sub {
  font-size: 13px;
  color: #999;
  margin-top: 6px;
}
</style>
