<template>
  <a-card title="Age vs Purchase Tendency" :bordered="false">
    <div ref="lineChartRef" style="height: 348px" />
  </a-card>
</template>

<script lang="ts" setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { Line } from "@antv/g2plot";

const lineChartRef = ref<HTMLElement | null>(null);
let lineChart: Line | null = null;

// 示例数据（单位：年龄段 vs 购买倾向率）
const ageData = [
  { age: "10", tendency: 0.6364 },
  { age: "20", tendency: 0.6022 },
  { age: "30", tendency: 0.6113 },
  { age: "40", tendency: 0.3211 },
  { age: "50", tendency: 0.3167 },
  { age: "60", tendency: 0.3188 },
  { age: "70", tendency: 0.2333 },
];

onMounted(() => {
  if (lineChartRef.value) {
    lineChart = new Line(lineChartRef.value, {
      data: ageData,
      xField: "age",
      yField: "tendency",
      smooth: true,
      point: {
        size: 5,
        shape: "circle",
        style: {
          fill: "white",
          stroke: "#5B8FF9",
          lineWidth: 2,
        },
      },
      tooltip: {
        formatter: (datum) => ({
          name: "Purchase Tendency",
          value: `${(datum.tendency * 100).toFixed(1)}%`,
        }),
      },
      yAxis: {
        label: {
          formatter: (val) => `${(parseFloat(val) * 100).toFixed(0)}%`,
        },
        title: { text: "Purchase Tendency Rate" },
      },
      color: "#5B8FF9",
    });
    lineChart.render();
  }
});

onBeforeUnmount(() => {
  lineChart?.destroy();
});
</script>
