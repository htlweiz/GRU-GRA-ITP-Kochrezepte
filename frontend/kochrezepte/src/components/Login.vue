<template>
    <h1 class="login-title">Login</h1>
    <div class="login-container">
    <div class="button-container">
      <button 
        class="btn btn-login" 
        v-if="!loggedIn"
        @click="login"
      >
        Log in mit Microsoft
      </button>
    </div>
  </div>
</template>

<script>
import * as msal from '@azure/msal-browser';
import axios from 'axios';
import { useToast } from 'vue-toast-notification';

const $toast = useToast();


const APIURL = `https://172.31.179.240:8002/users/`;

export default {
  data() {
    return {
      msalConfig: {
        auth: {
          clientId: import.meta.env.VITE_AZURE_CLIENT_ID,
          authority: import.meta.env.VITE_AZURE_AUTHORITY,
          redirectUri: import.meta.env.VITE_AZURE_REDIRECT_URI,
        },
      },
      msalInstance: null,
      loggedIn: false,
      username: '',
    };
  },
  methods: {
    async logout() {
      this.loggedIn = false;
      this.username = '';
      localStorage.removeItem('token');
      localStorage.removeItem('userId');
      localStorage.removeItem('username');
      localStorage.removeItem('email');
      localStorage.removeItem('role');
    },

    async login() {
        const loginRequest = {
            scopes: ['openid profile User.Read email'],
        };
        const response = await this.msalInstance.loginPopup(loginRequest);

        const token = response.accessToken;
        const userId = response.account.localAccountId;
        const name = response.account.name;
        const email = response.account.username;

        localStorage.setItem('token', token);
        localStorage.setItem('userId', userId);
        localStorage.setItem('username', name);
        localStorage.setItem('email', email);

        this.UserExists = false;
        
        await this.createUser(userId, name, email, token);

        
    },
    async createUser(id, name, email, token)
    {
      try
      {
        let res = await axios.post(
            APIURL,
            {
                userId: id,
                firstName: name.split(' ')[1] || '',
                lastName: name.split(' ')[0],
                email: email,
            },
            {
                headers: {
                Authorization: `Bearer ${token}`,
                },
            });

            if (res.status === 201)
            {
                this.loggedIn = true;
                $toast.success('Login erfolgreich', { duration: 5000 });
                this.$router.push('/home'); 
                return true;
            }

          }
          catch (error)
          {
            if (error.response.status === 409)
            {
                this.UserExists = true;
                this.loggedIn = true;
                $toast.success('Login erfolgreich', { duration: 5000 });
                this.$router.push('/home'); 
                return true;
            }

            $toast.error('Login fehlgeschlagen', { duration: 5000 });
          }

          
    },

    checkLoginStatus() {
      const token = localStorage.getItem('token');
      const username = localStorage.getItem('username');

      if (token && username) {
        this.loggedIn = true;
        this.username = username;
      }
    },
  },
  created() {
    this.msalInstance = new msal.PublicClientApplication(this.msalConfig);
    this.msalInstance.initialize();

    this.checkLoginStatus();
  },
};
</script>

<style scoped>
/* Container for the login form */
.login-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

/* Title */
.login-title {
  font-size: 36px;
  font-weight: 600;
  color: #2e3a59;
  margin-bottom: 20px;
  justify-self: center;
}


/* Button container */
.button-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  justify-self: center;
}

/* Common styles for buttons */
.btn {
  padding: 12px 20px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 250px;
}

/* Login button style */
.btn-login {
  background-color: #0078d4;
  color: white;
  border: none;
}

.btn-login:hover {
  background-color: #005fa3;
}

/* Responsive design */
@media (max-width: 768px) {
  .login-title {
    font-size: 28px;
  }

  .btn {
    width: 200px;
  }
}
</style>
