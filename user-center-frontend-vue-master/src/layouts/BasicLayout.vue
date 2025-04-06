<template>
  <div id="basicLayout">
    <a-layout style="height: 100vh">
      <!-- 左侧菜单栏 -->
      <a-layout-sider class="sider" width="200">
        <SildeBar />
      </a-layout-sider>

      <!-- 右侧主区域 -->
      <a-layout style="display: flex; flex-direction: column">
        <!-- 顶部导航栏 -->
        <a-layout-header class="header">
          <GlobalHeader />
        </a-layout-header>

        <!-- 主内容区域 -->
        <a-layout-content class="content">
          <router-view />
        </a-layout-content>
      </a-layout>
    </a-layout>
  </div>
</template>

<script setup lang="ts">
import GlobalHeader from "@/components/GlobalHeader.vue";
import SildeBar from "@/components/SildeBar.vue";
</script>

<style scoped>
#basicLayout {
  height: 100vh;
}

/* 左侧导航栏 */
.sider {
  background: white;
  padding: 10px;
}

/* 顶部区域 */
.header {
  background: rgb(242, 242, 242);
  color: unset;
  padding-top: 20px;
}

/* 主内容区域 */
.content {
  flex: 1;
  overflow: hidden; /* ❌ 不允许多余滚动条 */
  padding: 0; /* ✅ 移除 padding，交由子组件决定 */
  display: flex; /* ✅ 让子元素可以使用 flex 填充 */
  flex-direction: column;
}
</style>
