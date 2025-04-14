<template>
  <div style="background: #ececec; padding: 30px">
    <a-row :gutter="15" align="stretch">
      <a-col :span="24"><SalesKpiSummary /></a-col>
    </a-row>
    <a-row :gutter="15" style="margin-top: 32px">
      <a-col :span="10"><DailySalesTrend /></a-col>
      <a-col :span="14"><SalesCalendar /></a-col>
    </a-row>
  </div>
</template>

<script lang="ts" setup>
import DailySalesTrend from "@/components/dashboard/DailySalesTrend.vue";
import SalesCalendar from "@/components/dashboard/SalesCalendar.vue";
import SalesKpiSummary from "@/components/dashboard/SalesKpiSummary.vue";
</script>

<style scoped></style>
