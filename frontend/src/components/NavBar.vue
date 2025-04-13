<template>
  <header class="navbar" :class="{ 'navbar-with-border': showBorder && !isSidebarCollapsed}">
    <div class="left-controls">
      <!-- Buttons to open sidebar and start a new chat when sidebar is collapsed -->
      <template v-if="isSidebarCollapsed">
        <el-tooltip content="打开边栏" placement="bottom">
          <el-button type="text" class="sidebar-btn" @click="toggleSidebar">
            <img src="../../public/sidebar.svg" alt="Open Sidebar" class="icon-img" />
          </el-button>
        </el-tooltip>
        <el-tooltip content="新聊天" placement="bottom">
          <el-button type="text" class="new-chat-btn" @click="startNewChat" :disabled="!isLoggedIn">
            <img src="../../public/newmessage.svg" alt="New Chat" class="icon-img" />
          </el-button>
        </el-tooltip>
      </template>
    </div>

    <!-- 用户区域 -->
    <div class="user-section">
      <template v-if="isLoggedIn">
        <el-dropdown trigger="click">
          <el-avatar :size="32" :icon="'el-icon-user'"></el-avatar>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="logout">
                <div class="dropdown-item-content">
                  <img src="../../public/logout.svg" alt="Logout Icon" class="icon-img2" />
                  <span>注销</span>
                </div>
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </template>
      <template v-else>
        <router-link to="/login" class="auth-btn login-btn">登录</router-link>
        <router-link to="/register" class="auth-btn signup-btn">注册</router-link>
      </template>
    </div>
  </header>
</template>

<script>
export default {
  name: 'NavBar',
  props: {
    isSidebarCollapsed: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      welcomeModalVisible: false
    };
  },
  computed: {
    isLoggedIn() {
      return this.$store.getters.isAuthenticated;
    },
    username() {
      return this.$store.getters.getUsername || '用户';
    },
    showBorder() {
      return this.isLoggedIn && this.$route.path === '/chat';
    }
  },
  methods: {
    toggleSidebar() {
      this.$emit('toggle-sidebar');
    },
    async logout() {
      await this.$store.dispatch('logOut');
      this.$router.push('/chat');
    },
    startNewChat() {
      this.$emit('new-chat');
    }
  }
};
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  padding: 0 15px;
  background-color: #ffffff;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  transition: padding-left 0.3s ease;
}

.navbar.with-sidebar {
  padding-left: 260px; /* 侧边栏宽度 */
}

html, body {
  height: 100%;
  overflow: hidden; /* 禁止页面滚动条出现 */
}

#app {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.content-container {
  display: flex;
  flex: 1;
  margin-top: 60px; /* Navbar height */
  height: calc(100vh - 60px); /* Full height minus navbar */
  overflow: hidden; /* Prevent overflow */
}

.main-content {
  flex: 1;
  overflow-y: auto; /* Enable scrolling only in the main content */
  transition: margin-left 0.3s ease; /* Smooth transition for sidebar toggle */
  height: 100%; /* Ensure consistent height */
}

.content-container.with-sidebar .main-content {
  margin-left: 260px; /* 侧边栏宽度 */
}

.dropdown-item-content {
  display: flex;
  align-items: center;

}

.icon-img2 {
  width: 18px; /* Adjust the size of the icon */
  height: 18px;
  margin-right: 8px; /* Space between the icon and text */
}

/* When sidebar is visible, modify navbar to make space for it */
.navbar.with-sidebar {
  padding-left: 275px; /* 260px sidebar width + 15px padding */
  transition: padding-left 0.3s;
}

.navbar-with-border {
  border-bottom: 1px solid #e0e0e0; /* 淡灰色的底部边框 */
}

.left-controls {
  display: flex;
  align-items: center;
}

.sidebar-btn,
.new-chat-btn {
  padding: 8px;
  margin-right: 8px;
  color: #606266;
  transition: color 0.3s, background-color 0.3s;
}

.sidebar-btn:hover,
.new-chat-btn:hover {
  color: #000;
  background-color: #f0f0f0;
}

.icon-img {
  width: 24px;
  height: 24px;
  display: block;
  border: none;
}

.user-section {
  display: flex;
  align-items: center;
}

.auth-btn {
  padding: 8px 14px;
  margin-left: 12px;
  border-radius: 20px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
}

.login-btn {
  color: #fff;
  background-color: #000000;
  border: 1px solid #000000;
}

.login-btn:hover {
  background-color: #333333;
}

.signup-btn {
  color: #000000;
  background-color: #ffffff;
  border: 1px solid #dcdfe6;
}

.signup-btn:hover {
  background-color: #f5f7fa;
}

.sidebar-btn:hover,
.new-chat-btn:hover {
  color: #000;
  background-color: #d3d3d3 !important; /* Match the sidebar hover background */
  border-radius: 4px; /* Match the sidebar button border radius */
}
</style>