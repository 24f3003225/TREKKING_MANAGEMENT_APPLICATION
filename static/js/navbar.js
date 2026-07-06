Vue.createApp({

    data() {

        return {
            user: null
        }
    },

    mounted() {

        const storedUser =
            localStorage.getItem("user")

        if (storedUser) {

            this.user =
                JSON.parse(storedUser)
        }

        console.log(this.user)
    },

    methods: {

        logout() {

            localStorage.removeItem("token")
            localStorage.removeItem("user")

            window.location.href = "/login"
        }
    }

}).mount("#navbarApp")