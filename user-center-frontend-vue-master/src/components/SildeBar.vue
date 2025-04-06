<template>
  <div id="sildeBar">
    <div class="title-bar">
      <img class="logo" src="../assets/logo.png" alt="logo" />
    </div>
    <a-menu
      id="dddddd"
      v-model:openKeys="openKeys"
      v-model:selectedKeys="selectedKeys"
      style="width: 190px"
      mode="inline"
      :items="items"
      @click="handleClick"
    ></a-menu>
  </div>
</template>

<script lang="ts" setup>
import { reactive, ref, watch, VueElement, h } from "vue";
import {
  MailOutlined,
  AppstoreOutlined,
  SettingOutlined,
  CommentOutlined,
  HomeOutlined,
} from "@ant-design/icons-vue";
import type { MenuProps, ItemType } from "ant-design-vue";
import { useRouter, useRoute } from "vue-router";

// ✅ 路由实例
const router = useRouter();
const route = useRoute();

// ✅ 选中和展开的 key
const selectedKeys = ref<string[]>(["sub2"]); // 初始默认选中 HomePage
const openKeys = ref<string[]>(["sub1"]);

// ✅ 创建 menu items
function getItem(
  label: VueElement | string,
  key: string,
  icon?: any,
  children?: ItemType[],
  type?: "group"
): ItemType {
  return {
    key,
    icon,
    children,
    label,
    type,
  } as ItemType;
}

// ✅ 侧栏菜单配置
const items: ItemType[] = reactive([
  getItem("HomePage", "sub2", () => h(HomeOutlined)),
  getItem("AI Agent", "sub1", () => h(CommentOutlined)),

  { type: "divider" },

  getItem("Navigation Three", "sub4", () => h(SettingOutlined), [
    getItem("Option 9", "9"),
    getItem("Option 10", "10"),
    getItem("Option 11", "11"),
    getItem("Option 12", "12"),
  ]),

  getItem(
    "Group",
    "grp",
    null,
    [getItem("Option 13", "13"), getItem("Option 14", "14")],
    "group"
  ),
]);

// ✅ 处理点击事件
const handleClick: MenuProps["onClick"] = (e) => {
  console.log("click", e);
  if (e.key === "sub1") {
    router.push({ name: "aiagent" });
  }
  if (e.key === "sub2") {
    router.push({ name: "about" });
  }
};

// ✅ 监听路由变化，自动更新 `selectedKeys`
watch(
  () => route.path,
  (newPath) => {
    console.log("route changed to:", newPath);
    if (newPath === "/aiagent") {
      selectedKeys.value = ["sub1"];
    } else if (newPath === "/") {
      selectedKeys.value = ["sub2"];
    }
  },
  { immediate: true } // 初始化时触发
);
</script>

<style scoped>
.title-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 78px;
  width: 128px;
  overflow: hidden;
}

.logo {
  height: 100%;
  width: 100%;
  object-fit: cover;
}

/* 高亮选中效果 */
.ant-menu-item-selected {
  background-color: #e6f7ff !important;
  color: #1890ff !important;
  font-weight: bold;
}
</style>
