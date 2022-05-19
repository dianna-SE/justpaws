const app = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            firstName: 'why is this not working',
            email: 'page@gmail.com',
        };
    },
    methods: {
        getUser() {
            console.log(this.firstName)
        },
    },
})

app.mount('#app');