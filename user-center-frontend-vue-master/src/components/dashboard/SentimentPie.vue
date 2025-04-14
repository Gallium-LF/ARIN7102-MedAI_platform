<template>
  <a-card
    :bordered="false"
    style="width: 100%; border-radius: 8px; height: 100%"
  >
    <!-- 左上角标题 + 月份选择 -->
    <div
      style="
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
      "
    >
      <div style="font-weight: 600; font-size: 16px">Patient Sentiment</div>
      <a-select v-model:value="selectedMonth" style="width: 120px">
        <a-select-option
          v-for="(v, month) in monthPercentMap"
          :key="month"
          :value="month"
        >
          {{ month }}
        </a-select-option>
      </a-select>
    </div>

    <!-- 仪表盘 + 表情 -->
    <div class="gauge-container">
      <a-progress
        type="dashboard"
        :percent="percent"
        :show-info="false"
        stroke-color="#1677ff"
        :width="160"
      />
      <component :is="faceIcon" class="gauge-icon" />
    </div>

    <!-- 状态文字 -->
    <div class="status-text">{{ statusText }}</div>

    <!-- 百分比说明 -->
    <div class="satisfaction-text">
      <span class="satisfaction-bold">{{ percent }}%</span>
      <span class="satisfaction-subtext">
        of patients satisfied<br />
        with their visit.
      </span>
    </div>
  </a-card>
</template>

<script lang="ts" setup>
import {
  SmileOutlined,
  MehOutlined,
  FrownOutlined,
} from "@ant-design/icons-vue";
import { computed, ref } from "vue";

// 月份 -> 满意度百分比 映射
const monthPercentMap = {
  January: 85,
  February: 72,
  March: 60,
  April: 90,
  May: 65,
  June: 78,
  July: 55,
  August: 82,
  September: 74,
  October: 68,
  November: 80,
  December: 88,
};

// 当前选中的月份
const selectedMonth = ref("January");

// 根据选中月份计算百分比
const percent = computed(() => monthPercentMap[selectedMonth.value]);

const faceIcon = computed(() => {
  if (percent.value >= 80) return SmileOutlined;
  if (percent.value >= 60) return MehOutlined;
  return FrownOutlined;
});

const statusText = computed(() => {
  if (percent.value >= 80) return "Superb!";
  if (percent.value >= 60) return "Okay";
  return "Poor";
});
</script>

<style scoped>
.gauge-container {
  position: relative;
  width: fit-content;
  margin: 0 auto 12px;
}
.gauge-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 48px;
  color: #1677ff;
  pointer-events: none;
}
.status-text {
  color: #1677ff;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 8px;
}
.satisfaction-text {
  font-size: 16px;
  text-align: center;
}
.satisfaction-bold {
  font-weight: bold;
  font-size: 24px;
}
.satisfaction-subtext {
  color: #888;
  font-size: 14px;
  display: block;
  margin-top: 4px;
}
</style>
