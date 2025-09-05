<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
    <div class="container">
      <router-link class="navbar-brand fw-bold fs-3" to="/">
        <span class="text-primary">Uni</span>Admit
      </router-link>
      
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <!-- Guest menu -->
          <template v-if="!authStore.isAuthenticated">
            <li class="nav-item">
              <router-link class="nav-link" to="/">🏠 Home</router-link>
            </li>
          </template>
          
          <!-- Authenticated user menu -->
          <template v-if="authStore.isAuthenticated">
            <li class="nav-item">
              <router-link class="nav-link" to="/dashboard">📊 Dashboard</router-link>
            </li>
            <li class="nav-item" v-if="authStore.user?.roles?.includes('student')">
              <router-link class="nav-link" to="/my-applications">📋 Applications</router-link>
            </li>
            <li class="nav-item" v-if="authStore.user?.roles?.includes('student')">
              <router-link class="nav-link" to="/application">➕ New Application</router-link>
            </li>
            <li class="nav-item" v-if="authStore.user?.roles?.includes('admin')">
              <router-link class="nav-link" to="/admin">⚙️ Admin Panel</router-link>
            </li>
          </template>
        </ul>
        
        <!-- Right side menu -->
        <ul class="navbar-nav">
          <template v-if="!authStore.isAuthenticated">
            <li class="nav-item">
              <router-link class="nav-link" to="/login">
                <i class="fas fa-sign-in-alt me-1"></i>Login
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/register">
                <i class="fas fa-user-plus me-1"></i>Register
              </router-link>
            </li>
          </template>
          
          <template v-if="authStore.isAuthenticated">
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle d-flex align-items-center" href="#" id="userDropdown" 
                 role="button" @click="toggleDropdown" aria-expanded="false"
                 :class="{ show: dropdownOpen }">
                <div class="user-avatar me-2">
                  <i class="fas fa-user-circle fs-5"></i>
                </div>
                <span class="d-none d-lg-inline">{{ authStore.user?.name }}</span>
              </a>
              <ul class="dropdown-menu dropdown-menu-end shadow-lg border-0" 
                  :class="{ show: dropdownOpen }" aria-labelledby="userDropdown">
                <li>
                  <h6 class="dropdown-header">
                    <i class="fas fa-user me-1"></i>{{ authStore.user?.name }}
                  </h6>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <router-link class="dropdown-item" to="/profile" @click="closeDropdown">
                    <i class="fas fa-user-edit me-2"></i>Profile
                  </router-link>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item text-danger" href="#" @click.prevent="handleLogout">
                    <i class="fas fa-sign-out-alt me-2"></i>Logout
                  </a>
                </li>
              </ul>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'NavBar',
  setup() {
    const authStore = useAuthStore()
    const dropdownOpen = ref(false)
    
    const toggleDropdown = () => {
      dropdownOpen.value = !dropdownOpen.value
    }
    
    const closeDropdown = () => {
      dropdownOpen.value = false
    }
    
    const handleLogout = async () => {
      try {
        closeDropdown()
        await authStore.logout()
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
    
    // Close dropdown when clicking outside
    const handleClickOutside = (event) => {
      const dropdown = document.querySelector('.dropdown')
      if (dropdown && !dropdown.contains(event.target)) {
        closeDropdown()
      }
    }
    
    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
    })
    
    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside)
    })
    
    return {
      authStore,
      dropdownOpen,
      toggleDropdown,
      closeDropdown,
      handleLogout
    }
  }
}
</script>

<style scoped>
.navbar-brand {
  font-size: 1.8rem;
  letter-spacing: -1px;
}

.nav-link {
  font-weight: 500;
  transition: all 0.3s ease;
  border-radius: 0.375rem;
  margin: 0 0.25rem;
  padding: 0.5rem 0.75rem !important;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

.nav-link.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
  font-weight: 600;
}

.dropdown-menu {
  border-radius: 0.75rem;
  padding: 0.5rem 0;
  min-width: 200px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  display: block !important;
}

.dropdown-menu.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-toggle.show::after {
  transform: rotate(180deg);
}

.dropdown-toggle::after {
  transition: transform 0.3s ease;
}

.dropdown-item {
  padding: 0.5rem 1rem;
  transition: all 0.2s ease;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
  transform: translateX(5px);
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
}

.navbar-toggler {
  border: none;
  padding: 0.25rem 0.5rem;
}

.navbar-toggler:focus {
  box-shadow: none;
}

@media (max-width: 991.98px) {
  .navbar-nav {
    text-align: center;
    padding: 1rem 0;
  }
  
  .nav-link {
    margin: 0.25rem 0;
  }
  
  .dropdown-menu {
    position: static !important;
    transform: none !important;
    border: none;
    box-shadow: none;
    background: transparent;
    opacity: 1 !important;
    visibility: visible !important;
  }
  
  .dropdown-menu.show {
    display: block !important;
  }
  
  .dropdown-item {
    color: rgba(255, 255, 255, 0.8) !important;
    padding: 0.5rem 1rem;
  }
  
  .dropdown-item:hover {
    background-color: rgba(255, 255, 255, 0.1) !important;
    color: white !important;
  }
}

/* Custom hover effects */
.navbar-brand:hover {
  transform: scale(1.05);
  transition: transform 0.2s ease;
}

.dropdown-toggle::after {
  margin-left: 0.5rem;
}
</style>
