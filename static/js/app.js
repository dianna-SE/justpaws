const app = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            isVisible: false,
            greeting: 'you clicked enter!'
        };
    },
    methods: {
        togglePanel() {
            this.isVisible = !this.isVisible
        },
    },
})

app.mount('#app');