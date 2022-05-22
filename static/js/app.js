const app = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            isVisible: false,
            greeting: 'you clicked enter!',
            anyText: '',
            showSearch: false,
            showUpload: false,
            showNavbar: true,
            lastScrollPosition: 0
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
        onScroll () {
            const currentScrollPosition = window.pageYOffset || document.documentElement.scrollTop
            if (currentScrollPosition < 0) {
              return
            }
            // Stop executing this function if the difference between
            // current scroll position and last scroll position is less than some offset
            if (Math.abs(currentScrollPosition - this.lastScrollPosition) < 60) {
              return
            }
            this.showNavbar = currentScrollPosition < this.lastScrollPosition
            this.lastScrollPosition = currentScrollPosition
          }
    },
            mounted () {
            window.addEventListener('scroll', this.onScroll)
        },
        beforeDestroy () {
            window.removeEventListener('scroll', this.onScroll)
        },
})

app.mount('#app');