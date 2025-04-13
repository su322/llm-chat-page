<template>
  <div class="chat-container" :class="{ 'new-conversation': messages.length === 0, 'started-conversation': messages.length > 0 }">
    <div class="chat-messages" ref="messagesContainer" v-show="messages.length > 0">
      <div v-for="(message, index) in messages" :key="index"
           :class="['message', message.role === 'user' ? 'user-message' : 'assistant-message']">
        <div class="avatar">
          <el-avatar :icon="message.role === 'user' ? 'el-icon-user' : 'el-icon-s-custom'"></el-avatar>
        </div>
        <div class="message-content">
          <div class="role-name">{{ message.role === 'user' ? '你' : 'AI助手' }}</div>
          <div class="message-text">{{ message.content }}</div>
        </div>
      </div>

      <div v-if="isLoading" class="message assistant-message">
        <div class="avatar">
          <el-avatar icon="el-icon-s-custom"></el-avatar>
        </div>
        <div class="message-content">
          <div class="role-name">AI助手</div>
          <div class="message-text">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="empty-state" v-if="messages.length === 0">
      <h1 class="empty-state-heading">有什么可以帮忙的？</h1>
    </div>

    <div class="chat-input-container" :class="{ 'centered-input': messages.length === 0 }">
      <el-input
        v-model="userInput"
        type="textarea"
        :rows="1"
        placeholder="询问任何问题"
        @keyup.enter="sendMessage"
        class="chat-input"
        :autosize="{ minRows: 1, maxRows: 7 }"
      ></el-input>
      <el-button type="primary" @click="sendMessage" :loading="isLoading" class="send-button">
        发送
      </el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ChatView',
  data() {
    return {
      messages: [], // Initialize messages as an empty array
      userInput: '',
      isLoading: false
    };
  },
  methods: {
    sendMessage() {
      if (!this.userInput.trim() || this.isLoading) return;

      // Add user message to chat
      this.messages.push({
        role: 'user',
        content: this.userInput
      });

      // Clear input
      const userMessage = this.userInput;
      this.userInput = '';

      // Set loading state
      this.isLoading = true;

      // Call API to get response
      this.$store.dispatch('sendMessage', userMessage)
        .then(response => {
          // Add AI response to chat
          this.messages.push({
            role: 'assistant',
            content: response
          });
          this.isLoading = false;
          this.scrollToBottom();
        })
        .catch(error => {
          console.error('Error sending message:', error);
          this.isLoading = false;
        });
    },
    scrollToBottom() {
      this.$nextTick(() => {
        if (this.$refs.messagesContainer) {
          this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
        }
      });
    }
  },
  mounted() {
    // Load messages if needed
    // this.messages = this.$store.getters.getMessages || [];
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 70px);
  max-width: 900px;
  margin: 0 auto;
  padding: 120px 80px; /* Reduced top padding from 80px to 60px */
}

.chat-container.started-conversation {
}

.new-conversation {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.chat-messages {
  flex-grow: 1;
  overflow-y: auto;
  margin-bottom: 20px;
  padding-bottom: 20px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  margin-bottom: 10px;
  margin-top: 8vh; /* Reduced from 10vh to 5vh to move up */
}

.empty-state-heading {
  font-size: 28px;
  font-weight: 700;
  color: #000000;
}

.message {
  display: flex;
  padding: 20px 10px;
  margin-bottom: 5px;
}

.user-message {
  background-color: #ffffff;
}

.assistant-message {
  background-color: #ffffff;
}

.avatar {
  margin-right: 15px;
  align-self: flex-start;
}

.message-text {
  line-height: 1.6;
  word-break: break-word;
  white-space: pre-wrap;
  overflow-wrap: break-word;
  max-width: 100%;
}

.role-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.message-text {
  line-height: 1.6;
}

.chat-input-container {
  display: flex;
  flex-direction: column;
  padding: 15px;
  background-color: #ffffff;
  border: 1px solid #eaeaea;
  border-radius: 20px; /* Increased from 12px to 20px for larger radius */
  position: relative;
  min-height: 100px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.chat-input :deep(.el-textarea__inner) {
  border: none !important;
  box-shadow: none !important;
  padding: 5px 15px; /* Increased left padding from 0 to 15px */
  resize: none;
  background-color: transparent;
  max-height: 200px;         /* ✅ 设置最大高度 */
  overflow-y: auto !important; /* ✅ 启用垂直滚动条 */
}

.chat-input :deep(.el-textarea__inner)::placeholder {
  font-size: 15px;
  color: #959393; /* Lighter gray color for placeholder */
}

/* Make sure focus state doesn't add borders or outlines */
.chat-input :deep(.el-textarea__inner):focus {
  outline: none !important;
  box-shadow: none !important;
  border-color: transparent !important;

}

/* Target the textarea wrapper if needed */
.chat-input :deep(.el-textarea) {
  border: none;
}

.centered-input {
  max-width: 750px;
  width: 100%;
  margin: 10px auto;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.18); /* Increased shadow for centered input */
}

.chat-input {
  flex-grow: 1;
  margin-right: 10px;
  min-height: 70px; /* Make input area taller */
}

.send-button {
  position: absolute;
  left: 665px;
  right: 11px;
  bottom: 10px;
  border-radius: 20px; /* Match the auth-btn style */
  padding: 10px 21px; /* Match the auth-btn padding */
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #000000;
  border-color: #000000;
  color: #fff;
  font-size: 13px;
  font-weight: 550;
  transition: all 0.3s ease;
  height: 35px; /* Override fixed height */
  width: 60px; /* Override fixed width */
}

.send-button:hover {
  background-color: #333333;
  border-color: #333333;
  cursor: pointer;
}

.send-button i {
  margin: 0; /* Center the icon */
  font-size: 16px; /* Adjust icon size */
}

.typing-indicator {
  display: flex;
  align-items: center;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  margin: 0 1px;
  background-color: #666;
  border-radius: 50%;
  display: inline-block;
  animation: bounce 1.5s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) {
  animation-delay: -0.4s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: -0.2s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}
</style>