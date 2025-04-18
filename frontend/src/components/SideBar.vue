<template>
  <div class="sidebar" :class="{ 'collapsed': isCollapsed }">
    <!-- 侧边栏头部：折叠按钮 & 新聊天按钮 -->
    <div class="sidebar-header">
      <el-tooltip content="关闭边栏" placement="bottom">
        <el-button type="text" class="collapse-btn" @click="toggleSidebar">
          <img src="../../public/sidebar.svg" alt="Sidebar" class="icon-img" />
        </el-button>
      </el-tooltip>
      <el-tooltip content="新聊天" placement="bottom">
        <el-button
          type="text"
          class="action-btn"
          @click="newChat"
          :disabled="!isLoggedIn"
        >
          <img src="../../public/newmessage.svg" alt="New Message" class="icon-img" />
        </el-button>
      </el-tooltip>
    </div>

    <!-- 登录后：展示历史会话 -->
    <div class="conversation-list" v-if="isLoggedIn">
      <div
        v-for="session in conversations"
        :key="session.id"
        class="conversation-item"
        :class="{ active: session.id === activeConversationId }"
        @click="selectConversation(session)"
      >
        <div class="conversation-main">
          <i class="el-icon-chat-line-round"></i>
          <span class="conversation-title">
            会话{{ session.id }}
          </span>
        </div>
        <el-button type="text" class="delete-btn" @click.stop="deleteConversation(session)">
          <el-icon><Delete /></el-icon>
        </el-button>
      </div>
    </div>

    <!-- 未登录提示 -->
    <div v-else class="no-history">
      <p>登录后可以保存历史对话和开启新聊天</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
import { Delete } from '@element-plus/icons-vue';

export default {
  name: 'SideBar',
  components: {
    Delete
  },
  props: {
    isCollapsed: {
      type: Boolean,
      default: false
    },
    isLoggedIn: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      conversations: [],         // 会话列表
      activeConversationId: null // 当前选中的会话 ID
    };
  },
  computed: {
    ...mapGetters({
      currentUser: 'stateUser'
    })
  },
  watch: {
    // 登录成功或退出时触发
    isLoggedIn: {
      immediate: true,
      handler(loggedIn) {
        if (loggedIn) {
          this.fetchConversations();
        } else {
          this.conversations = [];
          this.activeConversationId = null;
        }
      }
    }
  },
  created() {
    // 初始化时，如果路由中带有 id，设为激活
    const id = this.$route.query.id;
    if (id) {
      this.activeConversationId = Number(id);
    }
  },
  methods: {
    toggleSidebar() {
      this.$emit('sidebar-toggle');
    },
    // 拉取当前用户的会话列表
    async fetchConversations() {
      try {
        const userId = this.currentUser.id;
        const resp = await axios.get('/sessions', {
          params: { user_id: userId }
        });
        this.conversations = resp.data || [];
      } catch (err) {
        console.error('获取会话列表失败:', err);
        this.conversations = [];
      }
    },
    // 选中某个会话，通知 ChatView 加载它
    selectConversation(session) {
      this.activeConversationId = session.id;
      this.$router.push({ path: '/chat', query: { id: session.id } });
    },
    // 新建会话，插入列表并选中
    async newChat() {
      if (!this.isLoggedIn) return;
      try {
        const userId = this.currentUser.id;
        const resp = await axios.post('/sessions', {
          user_id: userId,
          title: '新对话'
        });

        const session = resp.data;
        // 插入到最前面
        this.conversations.unshift(session);
        // 选中并路由
        this.selectConversation(session);
        // 通知 ChatView 清空消息
        window.dispatchEvent(new CustomEvent('new-chat-created', { detail: session }));
      } catch (err) {
        console.error('创建新会话失败:', err);
      }
    },
    async deleteConversation(session) {
      try {
        await axios.delete(`/sessions/${session.id}`);
        // 从列表中移除
        this.conversations = this.conversations.filter(s => s.id !== session.id);
        // 如果删除的是当前激活的，则跳回空聊天
        if (this.activeConversationId === session.id) {
          this.activeConversationId = null;
          this.$router.push({ path: '/chat' });
          window.dispatchEvent(new CustomEvent('new-chat-created', { detail: null }));
        }
      } catch (err) {
        console.error('删除会话失败:', err);
      }
    }
  }
};
</script>

<style scoped>
/* ---------- 保持原有样式不变 ---------- */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 260px;
  background-color: #f5f5f5;
  display: flex;
  flex-direction: column;
  z-index: 101;
  transition: width 0.3s;
}
.sidebar.collapsed {
  width: 0;
  overflow: hidden;
}
.sidebar-header {
  height: 60px;
  padding: 0 15px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e0e0e0;
}
.header-actions {
  display: flex;
  gap: 10px;
}
.collapse-btn,
.action-btn {
  padding: 8px;
  color: #606266;
  transition: color 0.3s, background-color 0.3s;
}
.collapse-btn:hover,
.action-btn:hover {
  color: #000;
  background-color: #d3d3d3 !important;
  border-radius: 4px;
}
.icon-img {
  width: 24px;
  height: 24px;
}
.conversation-list {
  flex-grow: 1;
  overflow-y: auto;
  padding: 10px 0;
}
.conversation-item {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 10px;
  margin: 2px 8px;
  color: #333;
  transition: background-color 0.2s;
  justify-content: space-between; /* 分散会话内容和删除按钮 */
}
.conversation-main {
  display: flex;
  align-items: center;
  flex: 1; /* 占满剩余空间，保证点击区域 */
  overflow: hidden;
}

.delete-btn {
  color: #959393;
  opacity: 0; /* 初始不可见 */
  transition: opacity 0.2s;
  margin-left: 8px; /* 添加间距 */
}

.conversation-item:hover .delete-btn {
  opacity: 1;
}
.conversation-item:hover {
  background-color: #e9e9e9;
}
.conversation-item.active {
  background-color: #d9d9d9;
  font-weight: bold;
}
.conversation-item i {
  margin-right: 10px;
  font-size: 16px;
}
.conversation-title {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.no-history {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 16px;
  color: #606266;
}
</style>

