<template>
  <div class="chat-container">
    <div class="chat-messages" ref="messagesContainer">
      <div v-if="messages.length === 0" class="empty-state">
        <h3>开始一个新的对话</h3>
        <p>发送一条消息开始聊天</p>
      </div>
      <div v-for="(msg, index) in messages" :key="index" class="message-item" :class="msg.role">
        <div class="message-avatar">
          <div v-if="msg.role === 'user'" class="avatar user-avatar">U</div>
          <div v-else class="avatar ai-avatar">AI</div>
        </div>
        <div class="message-content">
          <!-- 如果 AI 消息未完成加载，显示加载动画，否则格式化展示 -->
          <p v-if="msg.role === 'assistant' && msg.content === '' && isLoading" class="loading-animation">
            思考中<span>.</span><span>.</span><span>.</span>
          </p>
          <p v-else v-html="formatMessage(msg.content)"></p>
        </div>
      </div>
    </div>

    <div class="chat-input">
      <textarea
        v-model="message"
        placeholder="输入消息..."
        class="input-box"
        @keydown.enter.exact.prevent="sendMessage"
        :disabled="isLoading"
      ></textarea>
      <button @click="sendMessage" class="send-button" :disabled="isLoading || !message.trim()">
        <span v-if="!isLoading">发送</span>
        <span v-else>发送中...</span>
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  name: 'ChatView',
  data() {
    return {
      message: '',
      messages: [],
      isLoading: false,
      currentSessionId: null,
    };
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'stateUser']),
    modelName() {
      return 'deepseek-r1:latest'; // 默认模型名称
    }
  },
  async mounted() {
    // 如果URL有会话ID参数，加载该会话的消息
    const sessionId = this.$route.query.id;
    if (sessionId && this.isAuthenticated) {
      this.currentSessionId = sessionId;
      await this.loadSessionMessages(sessionId);
    }

    // 使用Vue 3兼容的事件监听方式
    window.addEventListener('new-chat-created', this.handleNewChatEvent);
  },
  beforeUnmount() {
    window.removeEventListener('new-chat-created', this.handleNewChatEvent);
  },
   watch: {
     // 监听 URL 中的 ?id=xxx
     '$route.query.id': {
       immediate: true,
       handler(newId) {
         if (newId && this.isAuthenticated) {
           this.currentSessionId = Number(newId);
           this.loadSessionMessages(this.currentSessionId);
         }
       }
     }
   },
  methods: {
    handleNewChatEvent(event) {
      this.handleNewChat(event.detail);
    },

    async sendMessage() {
      if (!this.message.trim() || this.isLoading) return;

      const userMessage = this.message.trim();
      this.messages.push({ role: 'user', content: userMessage });
      this.message = '';
      this.isLoading = true;

      // 滚动到底部
      this.$nextTick(() => this.scrollToBottom());

      try {
        if (this.isAuthenticated) {
          // 如果已登录但没有当前会话ID，创建新会话
          if (!this.currentSessionId) {
            await this.createNewSession();
          }
          await this.sendAuthenticatedMessage(userMessage);
        } else {
          await this.sendUnauthenticatedMessage(userMessage);
        }
      } catch (error) {
        console.error('发送消息错误:', error);
        this.messages.push({ role: 'assistant', content: '发送消息时出错，请稍后再试。' });
      } finally {
        this.isLoading = false;
        this.$nextTick(() => this.scrollToBottom());
      }
    },

    async createNewSession() {
      try {
        const response = await axios.post('/sessions', {
          user_id: this.stateUser.id,
          title: '新对话'
        });
        this.currentSessionId = response.data.id;
        // 通知其他组件已创建新会话
        this.$root.$emit('session-created', response.data);
        return response.data;
      } catch (error) {
        console.error('创建会话错误:', error);
        throw error;
      }
    },

    async sendAuthenticatedMessage(userMessage) {
      try {
        // 先添加AI消息容器
        this.messages.push({ role: 'assistant', content: '' });

        let aiResponse = '';

        // 使用axios处理流式响应
        await axios({
          method: 'post',
          url: `/sessions/${this.currentSessionId}/messages/stream`,
          data: {
            message: userMessage,
            model: this.modelName
          },
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/plain'
          },
          responseType: 'stream',
          onDownloadProgress: (progressEvent) => {
            // 检查是否有新数据
            if (progressEvent.event && progressEvent.event.target) {
              const responseText = progressEvent.event.target.responseText;
              if (responseText && responseText.length > aiResponse.length) {
                // 直接更新累积的响应
                aiResponse = responseText;

                // 更新最后一条AI消息
                this.messages[this.messages.length - 1].content = aiResponse;
                this.$nextTick(() => this.scrollToBottom());
              }
            }
          }
        });
      } catch (error) {
        console.error('流式消息错误:', error);
        // 如果请求失败，添加错误信息
        if (this.messages[this.messages.length - 1].role === 'assistant') {
          this.messages[this.messages.length - 1].content = `发送消息时出错: ${error.message || '请稍后再试'}`;
        }
      }
    },

    async sendUnauthenticatedMessage(userMessage) {
      try {
        // 先添加AI消息容器
        this.messages.push({ role: 'assistant', content: '' });

        let aiResponse = '';

        // 使用axios处理流式响应，不需要存储返回值
        await axios({
          method: 'post',
          url: '/chat/stream',
          data: {
            message: userMessage,
            model: this.modelName
          },
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'text/plain'
          },
          responseType: 'stream',
          onDownloadProgress: (progressEvent) => {
            // 检查是否有新数据
            if (progressEvent.event && progressEvent.event.target) {
              const responseText = progressEvent.event.target.responseText;
              if (responseText && responseText.length > aiResponse.length) {
                // 直接更新累积的响应，不需要单独保存chunk
                aiResponse = responseText;

                // 更新最后一条AI消息
                this.messages[this.messages.length - 1].content = aiResponse;
                this.$nextTick(() => this.scrollToBottom());
              }
            }
          }
        });
      } catch (error) {
        console.error('流式消息错误:', error);
        // 如果请求失败，添加错误信息
        if (this.messages[this.messages.length - 1].role === 'assistant') {
          this.messages[this.messages.length - 1].content = `发送消息时出错: ${error.message || '请稍后再试'}`;
        }
      }
    },

    async loadSessionMessages(sessionId) {
      try {
        const { data } = await axios.get(`/sessions/${sessionId}/messages`);
        this.messages = data.map(msg => ({
          role: 'user',
          content: msg.user_message
        })).flatMap((userMsg, i) => {
          const aiMsg = data[i] ? {
            role: 'assistant',
            content: data[i].ai_message
          } : null;
          return aiMsg ? [userMsg, aiMsg] : [userMsg];
        });
      } catch (error) {
        console.error('加载会话消息错误:', error);
      }
    },

    handleNewChat(session) {
      // 清空当前消息
      this.messages = [];
      this.currentSessionId = session ? session.id : null;
    },

    formatMessage(text) {
      return text.replace(/<think>[\s\S]*?<\/think>/g, '').trim();
    },

    scrollToBottom() {
      const container = this.$refs.messagesContainer;
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    }
  }
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
  padding: 20px;
  background-color: #fff;
}

.empty-state {
  text-align: center;
  margin-top: 100px;
  color: #888;
}

.message-item {
  display: flex;
  margin-bottom: 20px;
}

.message-avatar {
  margin-right: 15px;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.user-avatar {
  background-color: #007bff;
  color: white;
}

.ai-avatar {
  background-color: #28a745;
  color: white;
}

.message-content {
  flex: 1;
  padding: 10px 15px;
  border-radius: 10px;
  max-width: calc(100% - 60px);
}

.user .message-content {
  background-color: #f0f2f5;
}

.assistant .message-content {
  background-color: #f8f9fa;
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
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  resize: none;
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

.send-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.loading-animation span {
  animation: dots 1.5s infinite;
  animation-fill-mode: both;
}

.loading-animation span:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-animation span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes dots {
  0% { opacity: 0; }
  20% { opacity: 1; }
  100% { opacity: 0; }
}
</style>