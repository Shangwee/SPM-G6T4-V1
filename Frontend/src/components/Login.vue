<template>
    <div class="full-screen-container">
        <div class="card-container">
            <div class="login-section">
                <form @submit.prevent="login">
                    <h2>Login</h2>
                    <div class="input-group">
                        <label for="staffID">Staff ID</label>
                        <input type="text" id="staffID" v-model="credentials.staffID" required>
                    </div>
                    <div class="input-group">
                        <label for="password">Password</label>
                        <input type="password" id="password" v-model="credentials.password" required>
                    </div>
                    <button type="submit">Login</button>
                </form>
            </div>
            <div class="text-section">
                <div class="border rounded-3 border-2 border-light p-2 bg-opacity-75 bg-white">
                    <h2>Welcome to Southwest Airlines Operations Crew Scheduling System</h2>
                    <p>Enter your login details to start accessing.</p>
                </div>
                
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            credentials: {
                staffID: '',
                password: ''
            }
        };
    },
    methods: {
    //     login() {
    //         // default username and password for login
    //         if (this.credentials.username === '123' && this.credentials.password === '123') {
    //             console.log('Login successful');
    //             this.$router.push({ name: 'Home' });
    //         } else {
    //             alert('Incorrect username or password!');
    //         }
    //     }
    // }
    async login() {
      try {
        const response = await fetch('http://localhost:3000/api/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            staffID: this.staffID,
            password: this.password,
          }),
        });
        const data = await response.json();

        if (response.ok) {
          // On success, redirect or store token
          console.log('Login successful:', data);
          // Redirect user to dashboard or homepage
          this.$router.push('/home');
        } else {
          this.errorMessage = data.message;
        }
      } catch (error) {
        this.errorMessage = 'Login failed, please try again.';
      }
    },
  },
};
</script>

<style scoped>
.full-screen-container {
    display: flex;
    justify-content: center;
    margin-top: 200px;

  
}

.card-container {
    display: flex;
    width: 900px;
    /* Or desired width */
    height: 500px;
    /* Or desired height */
    box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.2);
    border-radius: 20px;
    overflow: hidden;
}

.login-section,
.text-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 40px;
}

.login-section {
    background-color: #fff;
}

.text-section {
    /* background-color: #3f51b5;
    color: white; */
    background-image: url('../assets/94999.png');
    overflow: hidden;
    width: 50%;
    height: 100%;
    background-size: contain;
}

.input-group input {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

button {
    padding: 10px;
    border: none;
    border-radius: 4px;
    background-color: #5c6bc0;
    color: white;
    cursor: pointer;
}

button:hover {
    background-color: #3f51b5;
}
.img {
  width: 50%;
  height: 100%;
  overflow: hidden;
}
</style>