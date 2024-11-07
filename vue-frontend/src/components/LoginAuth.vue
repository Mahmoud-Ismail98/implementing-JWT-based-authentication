<template>
    <div style="display: flex;flex-direction: column;align-items: center;">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <input v-model="username" placeholder="Username" />
        <input v-model="password" type="password" placeholder="Password" />
        <button type="submit">Login</button>
        <button @click="getProtectedContent">Access Protected Content</button>
        <p>{{ message }}</p>
      </form>
      <h2>Register</h2>
        <form @submit.prevent="register">
           <input v-model="registerUsername" placeholder="Username" />
           <input v-model="registerPassword" type="password" placeholder="Password" />
           <button type="submit">Register</button>
           <p>{{ registerMessage }}</p>
        </form>       
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        username: '',
        password: '',
        token: null,
        message: ''
      };
    },
    methods: {
        async register() {
            try {
                await axios.post('http://127.0.0.1:5000/register', {
                username: this.registerUsername,
                password: this.registerPassword
                });
                this.registerMessage = "Registration successful!";
            } catch (error) {
                this.registerMessage = error.response && error.response.data ? error.response.data.msg : "Registration failed!";
            }
      },
      async login() {
        try {
          const response = await axios.post('http://127.0.0.1:5000/login', {
            username: this.username,
            password: this.password
          });
          this.token = response.data.access_token;
          localStorage.setItem('token', this.token);
          this.message = "Logged in successfully!";
        } catch (error) {
          this.message = "Login failed!";
        }
      },
      async getProtectedContent() {
        try {
          const response = await axios.get('http://127.0.0.1:5000/protected', {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
          this.message = `Protected content: ${response.data.logged_in_as.username}`;
        } catch (error) {
          this.message = "Access denied!";
        }
      }
    }
  };
  </script>
  