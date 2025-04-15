<template>
  <div class="chat-container">
    <div class="chat-messages">
      <!-- 聊天消息显示区域 -->
    </div>
    <div class="chat-input">
      <input
        type="text"
        v-model="message"
        placeholder="输入消息..."
        class="input-box"
      />
      <button @click="sendMessage" class="send-button">发送</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: '',
    };
  },
  methods: {
    sendMessage() {
      if (this.message.trim()) {
        // 发送消息逻辑
        console.log('发送消息:', this.message);
        this.message = '';
      }
    },
  },
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  margin: 0 auto;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background-color: #fff;
}

.chat-input {
  display: flex;
  padding: 10px;
  background-color: #fff;
  border-top: 1px solid #ddd;
}

.input-box {
  flex: 1;
  height: 40px;
  padding: 0 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
}

.send-button {
  margin-left: 10px;
  padding: 0 20px;
  height: 40px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}

.send-button:hover {
  background-color: #333;
}
</style>