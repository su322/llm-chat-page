// 导入 axios 库，用于发送 HTTP 请求
import axios from 'axios';

// 定义状态
const state = {
  // 存储当前用户的对象
  user: null,
};

// 定义获取器
const getters = {
  // 判断用户是否已登录
  isAuthenticated: state =>!!state.user,
  // 获取当前用户
  stateUser: state => state.user,
};

// 定义动作
const actions = {
  // 注册新用户
  async register({ dispatch }, userData) {
    try {
      await axios.post('user/logout');
      await axios.post('register', userData);
      await dispatch('logIn', userData);
    } catch (e) {
      console.error('注册失败', e);
      throw e;
    }
  },
  // 用户登录
  async logIn({ dispatch }, userData) {
    await axios.post('login', userData);
    await dispatch('viewMe');
  },
  // 获取当前用户信息
  async viewMe({commit}) {
    // 发送 GET 请求到 users/whoami 接口
    let {data} = await axios.get('users/whoami');
    // 将获取到的用户数据提交到 mutations 中更新状态
    await commit('setUser', data);
  },
  // 用户登出
  async logOut({ commit }) {
    try {
      await axios.post('user/logout'); // 调用 logout 接口清除 Cookie
    } catch (e) {
      console.warn('后端登出失败（可能已经登出）', e);
    }

    commit('logout');
    window.location.reload(); // 刷新页面，清理前端状态
  }
};

// 定义突变
const mutations = {
  // 设置当前用户
  setUser(state, username) {
    state.user = username;
  },
  // 用户登出时调用，将用户设置为 null
  logout(state, user){
    state.user = user;
  },
};

// 导出 Vuex 模块
export default {
  state,
  getters,
  actions,
  mutations
};