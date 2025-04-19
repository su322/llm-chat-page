<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="login-title">创建账户</h1>

      <form @submit.prevent="submit" class="login-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            type="text"
            id="username"
            v-model="form.username"
            placeholder="创建用户名"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input
            type="password"
            id="password"
            v-model="form.password"
            placeholder="创建密码"
            required
          />
        </div>

        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input
            type="password"
            id="confirmPassword"
            v-model="form.confirmPassword"
            placeholder="再次输入密码"
            required
          />
        </div>

        <div class="terms-agreement">
          <input type="checkbox" id="terms" v-model="form.agreeTerms" required>
          <label for="terms">我同意<a href="/terms" target="_blank">服务条款</a>和<a href="/privacy" target="_blank">隐私政策</a></label>
        </div>

        <button type="submit" class="login-button" :disabled="isLoading || !form.agreeTerms">
          {{ isLoading ? '注册中...' : '创建账户' }}
        </button>
      </form>

      <div class="signup-prompt">
        已有账户? <router-link to="/login">登录</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { mapActions } from 'vuex';

export default defineComponent({
  name: 'RegisterView',
  data() {
    return {
      form: {
        username: '',
        password: '',
        confirmPassword: '',
        agreeTerms: false
      },
      isLoading: false
    };
  },
  methods: {
    ...mapActions(['register']),
    async submit() {
      if (this.form.password !== this.form.confirmPassword) {
        alert('两次密码输入不一致');
        return;
      }

      try {
        this.isLoading = true;
        const userData = new FormData();
        userData.append('username', this.form.username);
        userData.append('password', this.form.password);
        await this.register(userData);
        this.$router.push('/chat');
      } catch (error) {
        console.error('Registration failed:', error);
        alert('注册失败');
      } finally {
        this.isLoading = false;
      }
    }
  }
});
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  background-color: #f7f7f8;
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.login-title {
  margin: 0 0 10px;
  font-size: 28px;
  font-weight: 600;
  text-align: center;
}

.login-subtitle {
  margin-bottom: 30px;
  color: #666;
  text-align: center;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.form-group input {
  height: 44px;
  padding: 0 14px;
  font-size: 16px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  background-color: #fff;
  transition: border-color 0.2s;
}

.form-group input:focus {
  border-color: #000000;
  outline: none;
}

.terms-agreement {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
}

.terms-agreement a {
  color: #000000;
  text-decoration: none;
}

.terms-agreement a:hover {
  text-decoration: underline;
}

.login-button {
  height: 44px;
  margin-top: 10px;
  border: none;
  border-radius: 8px;
  background-color: #000000;
  color: white;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: #333333;
}

.login-button:disabled {
  background-color: #666;
  cursor: not-allowed;
}

.signup-prompt {
  margin-top: 30px;
  text-align: center;
  font-size: 14px;
  color: #666;
}

.signup-prompt a {
  color: #000000;
  font-weight: 500;
  text-decoration: none;
}

.signup-prompt a:hover {
  text-decoration: underline;
}
</style>