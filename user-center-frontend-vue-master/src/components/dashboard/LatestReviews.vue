<template>
  <div class="review-list">
    <div v-for="review in reviews" :key="review.uniqueID" class="review-card">
      <!-- 用户头像 + 名称 + 日期 -->
      <div class="header">
        <a-avatar :style="{ backgroundColor: avatarColor(review.uniqueID) }">
          {{ review.uniqueID.toString().slice(0, 2) }}
        </a-avatar>
        <div class="info">
          <div class="top-row">
            <span class="drug-name">{{ review.drugName }}</span>
            <a-rate :value="review.rating" allow-half disabled />
          </div>
          <div class="date">{{ review.date }}</div>
        </div>
      </div>

      <!-- 使用条件 -->
      <div class="condition">{{ review.condition }}</div>

      <!-- 评论内容 -->
      <div class="review-text">
        {{ review.review }}
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reviewList } from "@/data/reviewData"; // ← 路径按你实际目录修改
import { Avatar as AAvatar, Rate as ARate } from "ant-design-vue";

const reviews = reviewList;

function avatarColor(id: number): string {
  const colors = ["#f56a00", "#7265e6", "#ffbf00", "#00a2ae", "#13c2c2"];
  return colors[id % colors.length];
}
</script>

<style scoped>
.review-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 450px; /* 可自定义高度 */
  overflow-y: auto;
  padding-right: 8px; /* 给滚动条让空间 */
}

/* 美化滚动条 - 可选 */
.review-list::-webkit-scrollbar {
  width: 6px;
}
.review-list::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.review-card {
  background: white;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #f0f0f0;
}

.header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.top-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 15px;
}

.date {
  color: #888;
  font-size: 13px;
}

.condition {
  color: #1677ff;
  font-weight: 500;
  font-size: 14px;
  margin-bottom: 6px;
}

.review-text {
  font-size: 15px;
  color: #333;
  line-height: 1.6;
}
</style>
