<template>
  <a-card title="Yearly Sales Trend" :bordered="false">
    <div ref="chartRef" style="height: 360px" />
  </a-card>
</template>

<script lang="ts" setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { Line } from "@antv/g2plot";
import { salesData } from "@/data/salesData"; // ✅ 引入 Python 导出的 ts 数据

const chartRef = ref<HTMLElement | null>(null);
let chart: Line | null = null;

onMounted(() => {
  if (chartRef.value) {
    chart = new Line(chartRef.value, {
      data: salesData,
      xField: "year",
      yField: "sales",
      smooth: true,
      xAxis: {
        type: "category",
        title: { text: "Year" },
        label: {
          rotate: Math.PI / 8,
          autoRotate: true,
        },
      },
      yAxis: {
        title: { text: "Total Sales (€)" },
        label: {
          formatter: (v) => `€${(+v).toLocaleString()}`,
        },
      },
      tooltip: {
        formatter: (datum) => ({
          name: `Year ${datum.year}`,
          value: `€${datum.sales.toLocaleString()}`,
        }),
      },
      color: "#1677ff",
      point: {
        size: 4,
        style: {
          fill: "#fff",
          stroke: "#1677ff",
          lineWidth: 2,
        },
      },
    });
    chart.render();
  }
});

onBeforeUnmount(() => {
  chart?.destroy();
});
</script>
