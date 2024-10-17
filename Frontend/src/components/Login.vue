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

                    <!-- Error popup -->
                    <div v-if="errorMessage" class="error-popup">
                        {{ errorMessage }}
                    </div>
                </form>
            </div>
            <div class="text-section">
                <div class="welcome-text">
                    <h2>Welcome to Work-From-Home Management System</h2>
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
            },
            errorMessage: '' // Initialize as empty
        };
    },
    methods: {
        async login() {
            try {
                // Reset the error message before trying login
                this.errorMessage = '';

                const response = await fetch('http://localhost:5001/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.credentials),
                });

                const data = await response.json();

                if (response.ok) {
                    // Successful login
                    sessionStorage.setItem('staffID', data.Staff_ID);
                    sessionStorage.setItem('role', data.Role);

                    // Redirect user to the homepage or dashboard
                    this.$router.push('/');
                } else {
                    // Display error message from response
                    this.errorMessage = data.message || 'Incorrect login details, please try again.';
                }
            } catch (error) {
                // Catch any network or server errors
                this.errorMessage = 'Login failed, please try again later.';
            }
        },
    },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

.full-screen-container {
    display: flex;
    justify-content: center;
    margin-top: 150px;
    font-family: 'Poppins', sans-serif;
}

.card-container {
    display: flex;
    width: 900px;
    height: 450px;
    box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.1);
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
    background-image: url('../assets/94999.png');
    background-size: cover;
    display: flex;
    align-items: center;
    justify-content: center;
}

.welcome-text {
    background: rgba(255, 255, 255, 0.85);
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    color: #333;
}

h2 {
    font-weight: 600;
    font-size: 24px;
    color: #333;
    margin-bottom: 20px;
}

p {
    font-weight: 400;
    color: #555;
}

.input-group label {
    font-weight: 500;
    font-size: 14px;
    color: #666;
    margin-bottom: 5px;
}

.input-group input {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 14px;
    color: #333;
    transition: border 0.2s ease;
}

.input-group input:focus {
    border-color: #5c6bc0;
    outline: none;
}

button {
    padding: 12px;
    width: 100%;
    border: none;
    border-radius: 5px;
    background-color: #5c6bc0;
    color: white;
    font-weight: 600;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #3f51b5;
}

/* Error popup styles */
.error-popup {
    margin-top: 10px;
    padding: 10px;
    color: #fff;
    background-color: #f44336;
    border-radius: 5px;
    text-align: center;
    font-weight: 500;
    animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
</style>
