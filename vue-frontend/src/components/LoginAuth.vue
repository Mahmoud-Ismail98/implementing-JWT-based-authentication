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

      <!-- Conditional content based on role -->
      <div v-if="isAdmin">
        <h3>Admin Content</h3>
        <p>Welcome, Admin! Here is the content specifically for administrators.</p>
      </div>
      <div v-else-if="isUser">
        <h3>User Content</h3>
        <p>Welcome, User! Here is the content specifically for standard users.</p>
      </div>

      <!-- Conditional content based on department -->
      <div v-if="isRAndD">
        <h3>R&D Department</h3>
        <p>Welcome to the R&D department. This content is specific to you.</p>
      </div>
      <div v-else>
        <h3>General Content</h3>
        <p>Welcome to the general section. This content is for all departments.</p>
      </div>      
    </div>
  </template>
  <script>
  import axios from 'axios';
  import {   jwtDecode } from 'jwt-decode';
  
  export default {
    data() {
      return {
        username: '',
        password: '',
        registerUsername: '',
        registerPassword: '',
        token: null,
        message: '',
        userRoles: [],
        userAttributes: {},
        registerMessage: ''
      };
    },
    computed: {
      isAdmin() {
        return this.userRoles.includes('admin');
      },
      isUser() {
      return this.userRoles.includes('user');
    },
      isRAndD() {
        return this.userAttributes.department === 'R&D';
      }
    },
    methods: {
      adminAction() {
        console.log('Admin action triggered');
      },
      rdContent() {
        console.log('R&D content triggered');
      },
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
          console.log({ username: this.username, password: this.password });
          const response = await axios.post('http://127.0.0.1:5000/login', {
            username: this.username,
            password: this.password
          });

          this.token = response.data.access_token;
          console.log('Token received:', this.token);

          // Decode the token after assigning it to `this.token`
          const decodedToken = jwtDecode(this.token); // Declare and use `decodedToken` here
          console.log('Decoded Token:', decodedToken); // Log to verify the structure

          // Store the token in local storage
          localStorage.setItem('token', this.token);

          // Set user roles and attributes based on the decoded token
          this.userRoles = decodedToken.sub.role ? [decodedToken.sub.role] : [];
          this.userAttributes = { department: decodedToken.sub.department || '' };
          console.log('User roles:', this.userRoles);
          console.log('User attributes:', this.userAttributes);

          this.message = "Logged in successfully!";
        } catch (error) {
          console.error('Login error:', error.response ? error.response.data : error);
          this.message = error.response && error.response.data ? error.response.data.msg : "Login failed!";
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
  