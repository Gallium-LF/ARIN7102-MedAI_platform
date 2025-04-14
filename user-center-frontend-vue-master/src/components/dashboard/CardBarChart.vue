<template>
  <a-card
    :bordered="false"
    style="width: 100%; border-radius: 8px; height: 100%"
  >
    <!-- 顶部标题和统计 -->
    <div
      style="display: flex; justify-content: space-between; align-items: center"
    >
      <div>
        <div style="font-weight: 600; font-size: 16px">Public Reviews</div>
        <div
          style="
            display: flex;
            align-items: baseline;
            gap: 40px;
            margin-top: 8px;
          "
        >
          <a-statistic
            title="Total Reviews"
            :value="totalReviews"
            :value-style="{ fontSize: '24px' }"
          />
          <a-statistic
            title="Since PatientPop"
            :value="activeReviews"
            :value-style="{ color: '#3f8600', fontSize: '24px' }"
            prefix="+"
          />
        </div>
      </div>
      <div style="font-size: 14px; color: #999">1 year</div>
    </div>

    <!-- 图表区 -->
    <div class="chart-container">
      <!-- Y轴刻度 + 灰线 -->
      <div class="y-axis">
        <div
          v-for="tick in yAxisTicks"
          :key="tick"
          class="y-tick-line"
          :style="{ bottom: (tick / maxValue) * 100 + '%' }"
        >
          <span class="y-label">{{ tick }}</span>
          <div class="y-line"></div>
        </div>
      </div>

      <!-- 柱状图区域 -->
      <div class="bar-chart">
        <a-tooltip
          v-for="(item, index) in normalizedChartData"
          :key="index"
          :title="`${item.height} reviews`"
        >
          <div
            class="bar-item"
            :style="{
              height: item.normalizedHeight + 'px',
              backgroundColor: item.active ? '#00c896' : '#d9d9d9',
            }"
          >
            <div class="bar-label">{{ item.month }}</div>
          </div>
        </a-tooltip>
      </div>
    </div>
  </a-card>
</template>

<script lang="ts" setup>
import { chartData } from "@/data/chartData";

// 配置：最大柱高像素
const MAX_BAR_HEIGHT = 120;

// 找最大值用于归一化比例
const maxValue = Math.max(...chartData.map((d) => d.height));

// Y轴刻度（可按需改为更多分段）
const yAxisTicks = [0, Math.round(maxValue / 2), maxValue];

// 把高度归一化为 0~MAX_BAR_HEIGHT
const normalizedChartData = chartData.map((d) => ({
  ...d,
  normalizedHeight: Math.round((d.height / maxValue) * MAX_BAR_HEIGHT),
}));

const totalReviews = chartData.reduce((sum, d) => sum + d.height, 0);
const activeReviews = chartData
  .filter((d) => d.active)
  .reduce((sum, d) => sum + d.height, 0);
</script>

<style scoped>
.chart-container {
  display: flex;
  margin-top: 24px;
  height: 160px;
  position: relative;
}

/* === Y轴刻度 + 灰线 === */
.y-axis {
  width: 40px;
  position: relative;
  margin-right: 12px;
}
.y-tick-line {
  position: absolute;
  left: 0;
  width: 100%;
  display: flex;
  align-items: center;
  transform: translateY(50%);
}
.y-label {
  font-size: 12px;
  color: #999;
  width: 30px;
  text-align: right;
  margin-right: 6px;
}
.y-line {
  height: 1px;
  background-color: #999;
  flex: 1;
}

/* === 柱状图区域 === */
.bar-chart {
  display: flex;
  align-items: end;
  gap: 8px;
  flex: 1;
  position: relative;
}
.bar-item {
  width: 20px;
  border-radius: 4px 4px 0 0;
  position: relative;
  display: flex;
  align-items: end;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}
.bar-item:hover {
  opacity: 0.8;
  transform: scaleY(1.05);
}
.bar-label {
  position: absolute;
  bottom: -20px;
  font-size: 12px;
  color: #999;
  text-align: center;
}
</style>
