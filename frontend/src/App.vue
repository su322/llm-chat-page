<template>
  <div id="app">
    <NavBar
      v-if="showNavBar"
      :isSidebarCollapsed="sidebarCollapsed"
      @toggle-sidebar="toggleSidebar"
      @new-chat="createNewChat"
    />
    <div class="content-container" :class="{ 'with-sidebar': !sidebarCollapsed && showNavBar, 'no-navbar': !showNavBar }">
      <SideBar
        v-if="showNavBar"
        :isCollapsed="sidebarCollapsed"
        :isLoggedIn="isLoggedIn"
        @sidebar-toggle="toggleSidebar"
        ref="sidebar"
      />
      <main class="main-content" :class="{ 'no-navbar': !showNavBar, 'sidebar-collapsed': sidebarCollapsed }">
        <router-view/>
      </main>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import SideBar from '@/components/SideBar.vue';
import { mapGetters } from 'vuex';

export default {
  components: {
    NavBar,
    SideBar
  },
  data() {
    return {
      sidebarCollapsed: false
    };
  },
  computed: {
    ...mapGetters(['isAuthenticated']),
    isLoggedIn() {
      return this.isAuthenticated;
    },
    showNavBar() {
      const hiddenRoutes = ['/login', '/register'];
      return !hiddenRoutes.includes(this.$route.path);
    }
  },
  methods: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed;
    },
    createNewChat() {
      if (this.$refs.sidebar) {
        this.$refs.sidebar.newChat();
      }
    }
  }
};
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content-container {
  display: flex;
  flex: 1;
  margin-top: 60px; /* 导航栏高度 */
}

.content-container:not(.with-sidebar) {
  margin-top: 0;
}

.content-container.with-sidebar .main-content {
  margin-left: 260px; /* 侧边栏宽度 */
}

.main-content {
  flex: 1;
  transition: margin-left 0.3s;
  padding: 20px;
}

.main-content.sidebar-collapsed {
  margin-left: 0;
}

.main-content.no-navbar {
  margin-top: 0;
  width: 100%;
}

.content-container.no-navbar {
  margin-top: 0;
}

.main-content.no-navbar {
  margin-top: 0;
  width: 100%;
  padding: 0;
}

@media (max-width: 768px) {
  .content-container.with-sidebar .main-content {
    margin-left: 0;
  }
}
</style>