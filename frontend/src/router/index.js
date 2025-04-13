import { createRouter, createWebHistory } from 'vue-router'
import RegisterView from '@/views/RegisterView.vue';
import LoginView from '@/views/LoginView.vue';
import ChatView from '@/views/ChatView.vue';
// import store from '@/store';


const routes = [
    {
    path: '/',
    redirect: '/chat'  // 重定向根路径到聊天页面
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/chat',
    name: 'Chat',
    component: ChatView,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// // 在路由跳转前执行的钩子函数
// router.beforeEach((to, _, next) => {
//   // 检查即将进入的路由是否需要认证
//   if (to.matched.some(record => record.meta.requiresAuth)) {
//     // 如果用户已经登录
//     if (store.getters.isAuthenticated) {
//       // 允许导航
//       next();
//       return;
//     }
//     // 如果用户未登录，重定向到登录页面
//     next('/login');
//   } else {
//     // 如果不需要认证，允许导航
//     next();
//   }
// });

export default router