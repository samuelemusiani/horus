<template>
    <div class="w-[35vw] h-[60vh] rounded-lg bg-gray-100 border-2 border-gray-400 shadow-lg overflow-hidden">
        <div class="w-full text-center py-2 bg-blue-500 text-white font-semibold shadow-md">
            <h1>{{ title }}</h1>
            <button class="absolute left-2 top-2"><v-icon name="io-close-circle" scale="1.2"
                    @click="closeChat" /></button>
        </div>
        <div class="overflow-y-auto h-4/5" ref="chatContainer">
            <div class="flex flex-col p-3 gap-4">
                <div v-for="msg in messages"
                    :class="{ 'justify-start': msg[0] === 'assistant', 'justify-end text-right': msg[0] !== 'assistant' }"
                    class="w-full flex">
                    <div
                        :class="['w-4/5 p-3 rounded-lg text-md text-gray-700 shadow-md flex flex-col', { 'bg-white': msg[0] === 'assistant', 'bg-blue-200': msg[0] !== 'assistant' }]">
                        <span v-if="msg[1].length === 0" class="loader"></span>
                        <span v-else v-html="renderMarkdown(msg[1])"></span>
                    </div>
                </div>
            </div>
        </div>
        <div class=" flex absolute shadow-lg bottom-1 left-1 right-1 rounded-lg border-2 overflow-hidden">
            <input v-model="message" @keyup.enter="sendMessage" type="text" class="flex-grow p-2 border rounded-l-lg"
                placeholder="Type your question here...">
            <button @click="sendMessage" class="p-2 bg-blue-500 text-white rounded-r-lg">Send</button>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { marked } from 'marked'

export default {
    name: 'ChatComponent',
    emits: ['close'],
    props: {
        title: {
            type: String,
            default: 'Vulnerability Assistant'
        },
        initialMessage: {
            type: Array,
            default: () => ['assistant', 'Hello, World!']
        }
    },
    data() {
        return {
            message: '',
            messages: []
        };
    },
    methods: {
        async sendMessage() {
            if (this.message === '') return;
            this.messages.push(['human', this.message]);
            this.message = '';
            await this.sendMsgsAndDisplay();
        },
        closeChat() {
            this.$emit('close');
        },
        async sendMsgsAndDisplay() {
            const msgs = [...this.messages];
            this.messages.push(['assistant', '']);
            this.scrollToBottom();
            const response = await axios.post("http://localhost:8000/chat", msgs);
            this.messages[this.messages.length - 1][1] = response.data;
            this.scrollToBottom();
        },
        scrollToBottom() {
            this.$nextTick(() => {
                const chatContainer = this.$refs.chatContainer;
                chatContainer.scrollTop = chatContainer.scrollHeight;
            });
        },
        renderMarkdown(content) {
            return marked(content);
        }
    },
    async mounted() {
        console.log(this.initialMessage);
        this.messages.push(this.initialMessage);
        await this.sendMsgsAndDisplay();
    }
};
</script>

<style scoped>
.chat-component {
    border: 1px solid #ccc;
}

.loader {
    animation: rotate 1s infinite;
    height: 30px;
    width: 30px;
}

.loader:before,
.loader:after {
    border-radius: 50%;
    content: "";
    display: block;
    height: 15px;
    width: 15px;
}

.loader:before {
    animation: ball1 1s infinite;
    background-color: rgb(59 130 246);
    box-shadow: 30px 0 0 gray;
    margin-bottom: 10px;
}

.loader:after {
    animation: ball2 1s infinite;
    background-color: rgb(59 130 246);
    box-shadow: 30px 0 0 gray;
}

@keyframes rotate {
    0% {
        transform: rotate(0deg) scale(0.8)
    }

    50% {
        transform: rotate(360deg) scale(1.2)
    }

    100% {
        transform: rotate(720deg) scale(0.8)
    }
}

@keyframes ball1 {
    0% {
        box-shadow: 30px 0 0 rgb(59 130 246);
    }

    50% {
        box-shadow: 0 0 0 rgb(59 130 246);
        margin-bottom: 0;
        transform: translate(15px, 15px);
    }

    100% {
        box-shadow: 30px 0 0 rgb(59 130 246);
        margin-bottom: 10px;
    }
}

@keyframes ball2 {
    0% {
        box-shadow: 30px 0 0 gray;
    }

    50% {
        box-shadow: 0 0 0 gray;
        margin-top: -20px;
        transform: translate(15px, 15px);
    }

    100% {
        box-shadow: 30px 0 0 gray;
        margin-top: 0;
    }
}

input:focus {
    outline: none;
    box-shadow: none;
}
</style>