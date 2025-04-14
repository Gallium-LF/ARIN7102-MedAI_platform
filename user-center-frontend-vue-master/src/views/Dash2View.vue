<template>
  <div style="background: #ececec; padding: 30px">
    <a-row :gutter="15" align="stretch">
      <a-col :span="24"><SalesSummaryCard /></a-col>
    </a-row>
    <a-row :gutter="15" style="margin-top: 32px">
      <a-col :span="10"> <PurchaseBehaviorChart /></a-col>
      <a-col :span="14"> <MonthlySalesLine /></a-col>
    </a-row>
  </div>
</template>

<script lang="ts" setup>
import SalesSummaryCard from "@/components/dashboard/SalesSummaryCard.vue";
import PurchaseBehaviorChart from "@/components/dashboard/PurchaseBehaviorChart.vue";
import MonthlySalesLine from "@/components/dashboard/MonthlySalesLine.vue";
</script>

<style scoped></style>
