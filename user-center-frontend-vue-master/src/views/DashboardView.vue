<template>
  <div style="background: #ececec; padding: 30px">
    <a-row :gutter="[15, 48]" align="stretch">
      <a-col :span="7">
        <Ratingcard />
      </a-col>
      <a-col :span="10">
        <CardBarChart />
      </a-col>
      <a-col :span="7">
        <SentimentPie />
      </a-col>
    </a-row>
    <a-row :gutter="[15, 48]" style="margin-top: 32px">
      <a-col :span="24">
        <LatestReviews />
      </a-col>
    </a-row>
  </div>
</template>

<script lang="ts" setup>
import Ratingcard from "@/components/dashboard/RatingCard.vue";
import CardBarChart from "@/components/dashboard/CardBarChart.vue";
import SentimentPie from "@/components/dashboard/SentimentPie.vue";
import LatestReviews from "@/components/dashboard/LatestReviews.vue";
</script>

<style scoped></style>
