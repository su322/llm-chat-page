<template>
  <div class="sidebar" :class="{ 'collapsed': isCollapsed }">
    <div class="sidebar-header">
      <el-tooltip content="关闭边栏" placement="bottom">
        <el-button type="text" class="collapse-btn" @click="toggleSidebar">
          <img src="../../public/sidebar.svg" alt="Sidebar" class="icon-img" />
        </el-button>
      </el-tooltip>
      <div class="header-actions">
        <el-tooltip content="新聊天" placement="bottom">
          <el-button type="text" class="action-btn" @click="newChat" :disabled="!isLoggedIn">
            <img src="../../public/newmessage.svg" alt="New Message" class="icon-img" />
          </el-button>
        </el-tooltip>
      </div>
    </div>

    <div class="conversation-list" v-if="isLoggedIn">
      <div
        v-for="(conversation, index) in conversations"
        :key="index"
        class="conversation-item"
        :class="{ 'active': activeConversationId === conversation.id }"
        @click="selectConversation(conversation)">
        <i class="el-icon-chat-line-round"></i>
        <span class="conversation-title">{{ conversation.title || '新对话' }}</span>
      </div>
    </div>

    <div v-else class="no-history">
      <p>登录后可以保存历史对话</p>
    </div>

    <div class="sidebar-footer">
      <el-menu class="sidebar-menu" :collapse="isCollapsed" router>
        <el-menu-item index="/settings">
          <i class="el-icon-setting"></i>
          <template #title>设置</template>
        </el-menu-item>
      </el-menu>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SideBar',
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
      activeConversationId: null,
      conversations: [
        { id: 1, title: '聊天历史 1' },
        { id: 2, title: '聊天历史 2' },
        { id: 3, title: '聊天历史 3' }
      ]
    };
  },
  methods: {
    toggleSidebar() {
      this.$emit('sidebar-toggle');
    },
    selectConversation(conversation) {
      this.activeConversationId = conversation.id;
      this.$router.push('/chat?id=' + conversation.id);
    },
    newChat() {
      if (!this.isLoggedIn) return;
      const newId = this.conversations.length + 1;
      const newConversation = { id: newId, title: '新对话' };
      this.conversations.unshift(newConversation);
      this.selectConversation(newConversation);
    }
  }
};
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 0; /* Changed: Start from top of page instead of below navbar */
  left: 0;
  height: 100vh; /* Changed: Take full viewport height */
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
  height: 60px; /* Match navbar height */
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
  display: block;
  border: none;
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
}

.conversation-item:hover {
  background-color: #e9e9e9; /* 悬浮时的浅灰色 */
}

.conversation-item.active {
  background-color: #d9d9d9; /* 选中时的灰色 */
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

.sidebar-footer {
  border-top: 1px solid #e0e0e0;
}

.sidebar-menu {
  border-right: none;
  background-color: transparent;
}

.sidebar-menu :deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
  border-left: none !important;
}

/* 清除Element UI的默认样式 */
.sidebar-menu.el-menu {
  border-right: none;
  background-color: transparent;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background-color: transparent;
  color: #000;
}

.sidebar-menu :deep(.el-menu-item):hover {
  background-color: #e9e9e9;
}

.no-history {
  flex-grow: 1; /* Allow the message to take up available space */
  display: flex;
  align-items: center; /* Center vertically */
  justify-content: center; /* Center horizontally */
  text-align: center; /* Align text in the center */
  font-size: 16px; /* Adjust font size if needed */
  color: #606266; /* Optional: Adjust text color */
}
</style>