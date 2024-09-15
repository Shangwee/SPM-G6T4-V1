<template>
    <NavBar></NavBar>
    <div class="app-container border border-dark bg-white bg-opacity-75">
        <div class="sidebar">
            <div class="search-box">
                <input type="text" placeholder="Search" />
            </div>

            <!-- Selected contact -->
            <div class="contact" v-for="contact in contacts" :key="contact.id" @click="selectContact(contact.id)">
                <div class="avatar">{{ contact.initials }}</div>
                <div class="name">{{ contact.name }}</div>
            </div>
        </div>
        <div class="chat-container">
            <div class="messages">
                <!-- Display messages -->
                <div v-for="message in MessageFilter" :key="message.id" class="message"
                    :class="{ 'mine': message.isMine }">
                    <div class="sender-name">{{ message.senderName }}</div>
                    <div class="content">{{ message.content }}</div>
                </div>
            </div>
            <div class="input-box">
                <!-- Send messages -->
                <input v-model="newMessage" type="text" placeholder="Write a message..." @keyup.enter="sendMessage" />
                <button @click="sendMessage">Send</button>
            </div>
        </div>
    </div>
</template>

<script setup>
    import NavBar from './NavBar.vue';
</script>

<script>
export default {
    name: 'LiveChat',
    data() {
        return {
            newMessage: '',
            currentContactId: null,

            // Messages 
            messages: [
                { id: 1, senderName: 'John Lim', content: 'Hi, my name is John Lim and my flight was affected. Here are my rescheduling details: 1. Full Name: John Lim 2. Affected Flight Number: 1111 3. Choice of Destination: San Juan 4. Departure Date & Time: 5 April 2024, 2 pm (U.S. Timing) 5. Number of Pax: 3', contactId: 1, isMine: false },
                { id: 2, senderName: 'Jane Tan', content: 'Hi, my name is Jane Tan and my flight was affected. Here are my rescheduling details: 1. Full Name: Jane Tan 2. Affected Flight Number: 1111 3. Choice of Destination: San Juan 4. Departure Date & Time: 5 April 2024, 2 pm (U.S. Timing) 5. Number of Pax: 3', contactId: 2, isMine: false },
            ],

            // Contacts Listed
            contacts: [
                { id: 1, name: 'John Lim', initials: 'JL' },
                { id: 2, name: 'Jane Tan', initials: 'JT' },
            ],
        };
    },
    methods: {
        selectContact(contactId) {
            this.currentContactId = contactId;
        },
        sendMessage() {
            if (this.newMessage.trim() && this.currentContactId) {
                const newMessage = {
                    id: this.messages.length + 1,
                    senderName: 'Southwest Airlines Operations Crew',
                    content: this.newMessage,
                    contactId: this.currentContactId,
                    isMine: true,
                };
                this.messages.push(newMessage);
                this.newMessage = '';
            }
        },
    },
    computed: {

        // Filter messages by the different users
        MessageFilter() {
            if (!this.currentContactId) return [];
            return this.messages.filter(message => message.contactId === this.currentContactId);
        },
    },
};
</script>

<!-- Styling of the LiveChat User Interface -->
<style>
.app-container {
    display: flex;
    height: 60vh;
    width: 60vw;
}

.bg-gray {
    background-color: #f0f0f0; /* Change to your desired grey color */
}

.sidebar {
    background-color: #02025f;
    color: white;
    padding: 0px;
}

.search-box {
    margin: 10px;
}

.contact {
    display: flex;
    align-items: center;
    margin: 10px;
}

.avatar {
    background-color: #6c757d;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 10px;
}

.name {
    font-size: 1rem;
}

.chat-container {
    width: 75%;
    display: flex;
    flex-direction: column;
    padding: 10px;
}

.messages {
    flex-grow: 1;
    overflow-y: auto;
}

.message {
    margin: 5px 0;
    padding: 10px;
    background-color: #e1ffc7;
    border-radius: 10px;
    width: fit-content;
    max-width: 50%;
    align-self: flex-start;
}

.message.mine {
    background-color: #dcf8c6;
    align-self: flex-end;
}

.sender-name {
    font-size: 0.75rem;
    color: #333;
    margin-bottom: 4px;
}

.input-box {
    display: flex;
    padding: 10px 0;
}

.input-box input {
    flex-grow: 1;
    /* margin-right: 10px; */
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 10px;
}

.input-box button {
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
}

.input-box button:hover {
    background-color: #0056b3;
}
</style>
