import { createStore } from "vuex";

import users from './modules/users';
// import chat from './modules/chat';

export default createStore({
  modules: {
    users,
    // chat
  }
});