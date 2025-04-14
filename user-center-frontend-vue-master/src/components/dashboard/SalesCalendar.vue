<template>
  <a-card title="Daily Sales Heatmap (2015 Jan - Jul)" :bordered="false">
    <div ref="chartRef" style="height: 360px" />
  </a-card>
</template>

<script lang="ts" setup>
import { onMounted, onBeforeUnmount, ref } from "vue";
import { Heatmap } from "@antv/g2plot";
import { heatmapCalendarData } from "@/data/heatmapCalendarData";

const chartRef = ref<HTMLElement | null>(null);
let chart: Heatmap | null = null;

onMounted(() => {
  if (chartRef.value) {
    chart = new Heatmap(chartRef.value, {
      data: heatmapCalendarData,
      xField: "week", // 横轴：第几周
      yField: "day", // 纵轴：星期几
      colorField: "sales", // 色值字段：销售额
      sizeRatio: 1,
      shape: "square",
      color: ["#BAE7FF", "#1890FF", "#0050B3"], // 颜色渐变
      tooltip: {
        formatter: (datum) => ({
          name: datum.date,
          value: `€${datum.sales.toLocaleString()}`,
        }),
      },
      xAxis: {
        title: { text: "Week" },
        label: { autoHide: true, autoRotate: false },
        grid: { visible: false },
      },
      yAxis: {
        title: { text: "Day of Week" },
        label: {
          formatter: (val) => val.slice(0, 3), // 显示 Mon, Tue, ...
        },
        grid: { visible: false },
      },
    });
    chart.render();
  }
});

onBeforeUnmount(() => {
  chart?.destroy();
});
</script>
