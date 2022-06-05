
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
            showPanel: false,
            previewImage: null,
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
        togglePanel() {
            this.showPanel = !this.showPanel
        },
        selectImage() {
            this.$refs.fileInput.click()
        },
        pickFile () {
            let input = this.$refs.fileInput
            let file = input.files
            if (file && file[0]) {
              let reader = new FileReader
              reader.onload = e => {
                this.previewImage = e.target.result
              }
              reader.readAsDataURL(file[0])
              this.$emit('input', file[0])
            }
        },
    },
})

app.mount('#app');