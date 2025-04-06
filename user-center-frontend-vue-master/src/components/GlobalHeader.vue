<template>
  <div class="GlobalHeader">
    <a-row warp="false">
      <a-col :span="24" :offset="22">
        <div class="user-login-status">
          <a-dropdown-button>
            Login
            <template #overlay>
              <a-menu @click="handleMenuClick">
                <a-menu-item key="1">
                  <UserOutlined />
                  User center
                </a-menu-item>
                <a-menu-item key="2">
                  <UserOutlined />
                  Change password
                </a-menu-item>
              </a-menu>
            </template>
            <template #icon><UserOutlined /></template>
          </a-dropdown-button></div
      ></a-col>
    </a-row>
  </div>
</template>
<script lang="ts" setup>
import { h, ref } from "vue";
import {
  MailOutlined,
  AppstoreOutlined,
  SettingOutlined,
  UserOutlined,
  CommentOutlined,
} from "@ant-design/icons-vue";
import { MenuProps } from "ant-design-vue";
</script>

<style scoped>
.user-login-status {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
