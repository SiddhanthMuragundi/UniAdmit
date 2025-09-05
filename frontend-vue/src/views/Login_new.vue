<template>
  <div class="login-page d-flex align-items-center justify-content-center py-5">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-4">
          <div class="card shadow-lg">
            <div class="card-header text-center py-4">
              <h3 class="mb-1 text-white">Welcome to UniAdmit</h3>
              <p class="mb-0 text-white-50">Sign in to your account</p>
            </div>
            <div class="card-body p-4">
              <!-- Alert for errors -->
              <div v-if="error" class="alert alert-danger" role="alert">
                {{ error }}
              </div>
              
              <!-- Alert for success messages -->
              <div v-if="successMessage" class="alert alert-success" role="alert">
                {{ successMessage }}
              </div>

              <form @submit.prevent="handleLogin">
                <div class="mb-3">
                  <label for="email" class="form-label">Email Address</label>
                  <input
                    type="email"
                    class="form-control"
                    id="email"
                    v-model="formData.email"
                    required
                    :disabled="loading"
                    placeholder="Enter your email"
                  >
                </div>

                <div class="mb-4">
                  <label for="password" class="form-label">Password</label>
                  <div class="input-group">
                    <input
                      :type="showPassword ? 'text' : 'password'"
                      class="form-control"
                      id="password"
                      v-model="formData.password"
                      required
                      :disabled="loading"
                      placeholder="Enter your password"
                    >
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      @click="showPassword = !showPassword"
                      :disabled="loading"
                    >
                      {{ showPassword ? '🙈' : '👁️' }}
                    </button>
                  </div>
                </div>

                <div class="d-grid">
                  <button
                    type="submit"
                    class="btn btn-primary btn-lg py-3"
                    :disabled="loading"
                  >
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                    {{ loading ? 'Signing in...' : 'Sign In' }}
                  </button>
                </div>
              </form>

              <hr class="my-4">

              <div class="text-center">
                <p class="mb-0">
                  Don't have an account?
                  <router-link to="/register" class="text-decoration-none fw-semibold">
                    Register here
                  </router-link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRoute } from 'vue-router'

export default {
  name: 'Login',
  setup() {
    const authStore = useAuthStore()
    const route = useRoute()
    
    const formData = ref({
      email: '',
      password: ''
    })
    
    const showPassword = ref(false)
    const loading = ref(false)
    const error = ref('')
    const successMessage = ref('')
    
    // Check for success message from registration
    if (route.query.message) {
      successMessage.value = route.query.message
    }
    
    const handleLogin = async () => {
      error.value = ''
      loading.value = true
      
      const result = await authStore.login(formData.value)
      
      if (!result.success) {
        error.value = result.error
      }
      
      loading.value = false
    }
    
    return {
      formData,
      showPassword,
      loading,
      error,
      successMessage,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}
</style>
