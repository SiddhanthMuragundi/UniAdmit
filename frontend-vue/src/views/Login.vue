<template>
  <div class="login-page">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">
        <div class="col-md-6 col-lg-5 col-xl-4">
          <div class="card border-0 shadow">
            <div class="card-header text-center border-0 bg-white py-4">
              <h1 class="h4 fw-bold text-primary mb-2">UniAdmit</h1>
              <h2 class="h5 fw-semibold text-dark mb-1">Welcome Back</h2>
              <p class="text-muted small mb-0">Sign in to your account</p>
            </div>
            <div class="card-body p-4">
              <!-- Form Instructions -->
              <div class="form-instructions mb-3">
                <p class="text-muted small text-center">
                  Fields marked with <span class="text-danger">*</span> are required
                </p>
              </div>

              <!-- Alert for errors -->
              <div v-if="error" class="alert alert-danger border-0" role="alert">
                {{ error }}
              </div>
              
              <!-- Alert for success messages -->
              <div v-if="successMessage" class="alert alert-success border-0" role="alert">
                {{ successMessage }}
              </div>

              <form @submit.prevent="handleLogin">
                <div class="form-group mb-3">
                  <label for="email" class="form-label fw-semibold">
                    Email Address <span class="text-danger">*</span>
                  </label>
                  <input
                    type="email"
                    class="form-control form-control-lg"
                    id="email"
                    v-model="formData.email"
                    required
                    :disabled="loading"
                    placeholder="Enter your email address"
                    aria-describedby="emailHelp"
                  >
                  <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
                </div>

                <div class="form-group mb-4">
                  <label for="password" class="form-label fw-semibold">
                    Password <span class="text-danger">*</span>
                  </label>
                  <div class="input-group">
                    <input
                      :type="showPassword ? 'text' : 'password'"
                      class="form-control form-control-lg"
                      id="password"
                      v-model="formData.password"
                      required
                      :disabled="loading"
                      placeholder="Enter your password"
                      aria-describedby="passwordHelp"
                    >
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      @click="showPassword = !showPassword"
                      :disabled="loading"
                      aria-label="Toggle password visibility"
                    >
                      {{ showPassword ? 'Hide' : 'Show' }}
                    </button>
                  </div>
                  <div id="passwordHelp" class="form-text">Password must be at least 6 characters long.</div>
                </div>

                <div class="d-grid mb-4">
                  <button
                    type="submit"
                    class="btn btn-primary btn-lg"
                    :disabled="loading"
                  >
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    {{ loading ? 'Signing in...' : 'Sign In' }}
                  </button>
                </div>
              </form>

              <div class="text-center">
                <p class="mb-0 text-muted">
                  Don't have an account? 
                  <router-link to="/register" class="text-primary text-decoration-none">
                    Create one here
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
  background: #f8f9fa;
  min-height: 100vh;
}

.min-vh-100 {
  min-height: 100vh;
}

.card {
  border-radius: 0.5rem;
}

.card-header {
  border-radius: 0.5rem 0.5rem 0 0;
  background: #ffffff;
}

.form-control {
  border: 1px solid #e9ecef;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.btn:focus {
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.alert {
  border-radius: 0.375rem;
  border: none;
}

.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
}

.alert-success {
  background-color: #d1e7dd;
  color: #0f5132;
}

@media (max-width: 576px) {
  .card-body {
    padding: 1.5rem !important;
  }
  
  .container {
    padding: 1rem;
  }
}
</style>
