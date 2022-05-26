const app = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            isVisible: false,
            greeting: 'you clicked enter!',
            anyText: '',
            showSearch: false,
            showUpload: false,
            showSuggested: false,
        };
    },
    methods: {
        toggleSettings() {
            this.isVisible = !this.isVisible
        },
        directRegister() { 
            router.push({ path: '/register'})
        },
        toggleSearch() {
            this.showSearch = !this.showSearch
        },
        toggleUpload() {
            this.showUpload = !this.showUpload
        },
        toggleSuggested() {
            this.showSuggested = !this.showSuggested
        },
    },
})

app.mount('#app');