<template>
  <a-card
    :bordered="false"
    style="
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    "
  >
    <div>
      <div style="font-size: 16px; font-weight: 600; margin-bottom: 8px">
        Overall Rating
      </div>

      <div
        style="
          display: flex;
          align-items: center;
          font-size: 32px;
          font-weight: bold;
        "
      >
        <span style="min-width: 40px; text-align: right">
          {{ selectedDrug.rating.toFixed(1) }}
        </span>
        <a-rate
          allow-half
          :value="selectedDrug.rating"
          disabled
          style="margin-left: 10px; font-size: 20px"
        />
      </div>

      <div style="color: #52c41a; margin-bottom: 16px">
        {{ selectedDrug.change }} points from last month
      </div>

      <a-divider style="margin: 12px 0" />

      <div>
        <div style="color: rgba(0, 0, 0, 0.45); font-size: 14px">Drug Name</div>
        <a-select
          v-model:value="selectedDrugName"
          style="width: 100%; margin-bottom: 12px"
        >
          <a-select-option
            v-for="(drug, name) in drugs"
            :key="name"
            :value="name"
          >
            {{ name }}
          </a-select-option>
        </a-select>

        <div style="color: rgba(0, 0, 0, 0.45); font-size: 14px">Treats</div>
        <a-tooltip :title="selectedDrug.disease">
          <div
            style="
              font-size: 16px;
              overflow: hidden;
              text-overflow: ellipsis;
              white-space: nowrap;
            "
          >
            {{ selectedDrug.disease }}
          </div>
        </a-tooltip>
      </div>
    </div>
  </a-card>
</template>

<script lang="ts" setup>
import { ref, computed } from "vue";
import { drugData } from "@/data/drugData"; // 引入你生成的静态数据

const drugs = drugData;
const selectedDrugName = ref(Object.keys(drugs)[0]); // 默认选择第一个药品
const selectedDrug = computed(() => drugs[selectedDrugName.value]);
</script>

<style scoped>
/* 可以根据需要加入响应式调整或卡片阴影等增强视觉效果 */
</style>
