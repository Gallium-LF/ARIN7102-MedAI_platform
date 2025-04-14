<template>
  <a-card title="Purchase Behavior Chart" :bordered="false">
    <!-- 下拉选择框 -->
    <a-select
      v-model:value="selectedChart"
      style="width: 240px; margin-bottom: 16px"
    >
      <a-select-option value="gender"
        >Gender-based Purchase Rate</a-select-option
      >
      <a-select-option value="category"
        >Product Category Success Rate</a-select-option
      >
    </a-select>

    <!-- 图表容器 -->
    <div ref="chartRef" style="height: 300px" />
  </a-card>
</template>

<script lang="ts" setup>
import { ref, watch, onMounted, onBeforeUnmount } from "vue";
import { Column } from "@antv/g2plot";

const chartRef = ref<HTMLElement | null>(null);
let chart: Column | null = null;

// 选中项
const selectedChart = ref<"gender" | "category">("gender");

// 图表数据
const genderData = [
  { gender: "Male", rate: 0.4307 },
  { gender: "Female", rate: 0.4333 },
];

const categoryData = [
  { category: "Antibiotics", rate: 0.4048 },
  { category: "Analgesics", rate: 0.4502 },
  { category: "Antidepressants", rate: 0.4249 },
  { category: "Antihistamines", rate: 0.465 },
  { category: "Gastrointestinal", rate: 0.4143 },
];

// 渲染图表函数
function renderChart(type: "gender" | "category") {
  if (!chartRef.value) return;

  const isGender = type === "gender";
  const data = isGender ? genderData : categoryData;

  chart?.destroy(); // 销毁旧图
  chart = new Column(chartRef.value, {
    data,
    xField: isGender ? "gender" : "category",
    yField: "rate",
    xAxis: {
      title: {
        text: isGender ? "Gender" : "Product Category",
      },
    },
    yAxis: {
      label: {
        formatter: (v) => `${(parseFloat(v) * 100).toFixed(0)}%`,
      },
    },
    label: {
      position: "middle",
      content: (d) => `${(d.rate * 100).toFixed(1)}%`,
      style: { fill: "#fff" },
    },
    columnStyle: { radius: [4, 4, 0, 0] },
    color: isGender ? "#1677ff" : "#13c2c2",
  });
  chart.render();
}

onMounted(() => {
  renderChart(selectedChart.value);
});

watch(selectedChart, (newVal) => {
  renderChart(newVal);
});

onBeforeUnmount(() => {
  chart?.destroy();
});
</script>
