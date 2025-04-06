<template>
  <div class="chat-container">
    <!-- 左侧历史记录 -->
    <div class="chat-history">
      <div class="chat-title">History</div>
      <a-list :data-source="chatList" bordered class="history-list">
        <template #renderItem="{ item }">
          <a-list-item class="history-item" @click="continueChat(item)">
            <div class="ellipsis">{{ item.title }}</div>
            <a-button
              type="link"
              danger
              @click.stop="deleteChat(item.conversationId)"
            >
              Delete
            </a-button>
          </a-list-item>
        </template>
      </a-list>
      <a-button
        type="primary"
        block
        class="new-chat-button"
        @click="createNewChat"
      >
        Create New Chat
      </a-button>
    </div>

    <!-- 右侧聊天区域 -->
    <div class="chat-main">
      <div class="chat-content" ref="chatContent">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          class="chat-bubble-container"
          :class="msg.role === 'user' ? 'user-container' : 'ai-container'"
        >
          <template v-if="msg.role === 'ai'">
            <RedditOutlined class="chat-avatar" />
            <div class="chat-bubble ai-bubble">{{ msg.text }}</div>
          </template>
          <template v-else>
            <div class="chat-bubble user-bubble">{{ msg.text }}</div>
            <UserOutlined class="chat-avatar" />
          </template>
        </div>
        <div v-if="loading" class="loading-bubble">
          <LoadingOutlined /> AI is thinking...
        </div>
      </div>

      <!-- 输入框 -->
      <div class="chat-input">
        <a-input
          ref="inputRef"
          :value="inputMessage"
          :disabled="loading"
          placeholder="Please enter your message..."
          @input="inputMessage = $event.target.value"
          @pressEnter.prevent="sendMessageRaw"
        />
        <a-button
          type="primary"
          :disabled="loading"
          style="margin-left: 8px"
          @click="sendMessageRaw"
        >
          Send
        </a-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";
import {
  UserOutlined,
  RedditOutlined,
  LoadingOutlined,
} from "@ant-design/icons-vue";
import axios from "axios";

const chatList = ref<
  { title: string; conversationId: number; messages: any[] }[]
>([]);
const messages = ref<{ role: "user" | "ai"; text: string }[]>([
  {
    role: "ai",
    text: "Hello, I'm your pharma sales assistant. How can I help you?",
  },
]);
const inputMessage = ref("");
const loading = ref(false);
const conversationId = ref<number | null>(null);

// ✅ DOM 引用
const chatContent = ref<HTMLElement | null>(null);
const inputRef = ref();

// ✅ 聚焦输入框
const focusInput = () => {
  nextTick(() => {
    inputRef.value?.focus?.();
  });
};

// ✅ 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (chatContent.value) {
      chatContent.value.scrollTo({
        top: chatContent.value.scrollHeight,
        behavior: "smooth",
      });
    }
  });
};

// ✅ 加载聊天历史
const loadChatHistory = async () => {
  try {
    const res = await axios.get("http://127.0.0.1:5000/chat/history");
    chatList.value = res.data.map((item: any) => {
      const lastMessageIndex = item.messages.length - 1;
      const lastMessage =
        lastMessageIndex >= 0 ? item.messages[lastMessageIndex].question : null;
      const title = lastMessage ? lastMessage : `Chat ${item.conversation_id}`;
      return {
        title,
        conversationId: item.conversation_id,
        messages: item.messages,
      };
    });
  } catch (error) {
    console.error("Failed to load chat history:", error);
  }
};

// ✅ 创建新对话
const createNewChat = async () => {
  conversationId.value = null;
  messages.value = [
    { role: "ai", text: "New chat created. How can I assist you?" },
  ];
  await loadChatHistory();
  scrollToBottom();
  focusInput();
};

// ✅ 恢复对话
const continueChat = (item: any) => {
  conversationId.value = item.conversationId;
  messages.value = item.messages
    .map((msg: any) => [
      { role: "user", text: msg.question },
      { role: "ai", text: msg.answer },
    ])
    .flat();
  scrollToBottom();
  focusInput();
};

// ✅ 删除对话并判断是否为当前活跃会话
const deleteChat = async (id: number) => {
  try {
    await axios.delete(`http://127.0.0.1:5000/chat/delete/${id}`);
    chatList.value = chatList.value.filter(
      (chat) => chat.conversationId !== id
    );

    if (conversationId.value === id) {
      conversationId.value = null;
      messages.value = [
        {
          role: "ai",
          text: "This chat has been deleted. You can start a new one.",
        },
      ];
    }
  } catch (error) {
    console.error("Failed to delete chat:", error);
  }
};

// ✅ 主发送函数
const sendMessageRaw = async () => {
  if (loading.value) return;

  const msg = inputMessage.value.trim();
  if (!msg) return;

  messages.value.push({ role: "user", text: msg });
  inputMessage.value = "";
  loading.value = true;

  try {
    const payload: any = { message: msg };
    if (conversationId.value !== null) {
      payload.conversation_id = conversationId.value;
    }

    const res = await axios.post("http://127.0.0.1:5000/chat", payload);
    if (res.data.conversation_id) {
      conversationId.value = res.data.conversation_id;
    }

    messages.value.push({ role: "ai", text: res.data.reply });
    await loadChatHistory();
  } catch (error) {
    messages.value.push({
      role: "ai",
      text: "An error occurred, please try again later.",
    });
    console.error("Error while sending message:", error);
  } finally {
    loading.value = false;
    scrollToBottom();
    focusInput();
  }
};

onMounted(() => {
  loadChatHistory();
  focusInput();
});
</script>

<style scoped>
.chat-container {
  display: flex;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  height: 100vh;
  overflow: hidden;
}

.chat-history {
  width: 280px;
  background-color: #fafafa;
  border-right: 1px solid #f0f0f0;
  display: flex;
  flex-direction: column;
  padding: 16px;
  box-sizing: border-box;
}

.chat-title {
  font-weight: bold;
  margin-bottom: 16px;
  font-size: 16px;
}

.history-list {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 16px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 44px;
  padding: 12px 8px;
  box-sizing: border-box;
}

.ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 180px;
  flex: 1;
  margin-right: 8px;
}

.new-chat-button {
  width: 100%;
  margin-top: auto;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  overflow: hidden;
}

.chat-content {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  scroll-behavior: smooth;
}

.chat-bubble-container {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.chat-bubble-container.ai-container {
  justify-content: flex-start;
}

.chat-bubble-container.user-container {
  justify-content: flex-end;
}

.chat-bubble {
  display: inline-block;
  padding: 10px 14px;
  border-radius: 8px;
  max-width: 70%;
  word-break: break-word;
  white-space: pre-wrap;
  line-height: 1.5;
}

.ai-bubble {
  align-self: flex-start;
  background-color: #e6f7ff;
}

.user-bubble {
  align-self: flex-end;
  background-color: #f0f0f0;
}

.chat-avatar {
  font-size: 18px;
  margin: 0 8px;
}

.loading-bubble {
  align-self: center;
  color: #999;
  margin-top: 8px;
}

.chat-input {
  display: flex;
  padding: 12px 16px;
  border-top: 1px solid #f0f0f0;
  background-color: #fff;
}
</style>
