Vue.createApp({

    data() {

        return {

            name: "",

            email: "",

            phone: ""
        }
    },

    methods: {

        async loadProfile() {

            const token =
                localStorage.getItem(
                    "token"
                )

            const response =
                await fetch(
                    "/user/profile",
                    {
                        headers: {
                            Authorization:
                                `Bearer ${token}`
                        }
                    }
                )

            const data =
                await response.json()

            this.name =
                data.name

            this.email =
                data.email

            this.phone =
                data.phone
        },

        async updateProfile() {

            const token =
                localStorage.getItem(
                    "token"
                )

            const response =
                await fetch(
                    "/user/profile",
                    {
                        method: "PUT",

                        headers: {

                            "Content-Type":
                                "application/json",

                            Authorization:
                                `Bearer ${token}`
                        },

                        body: JSON.stringify({

                            name:
                                this.name,

                            phone:
                                this.phone
                        })
                    }
                )

            const data =
                await response.json()

            alert(
                data.message
            )
        }

    },

    mounted() {

        this.loadProfile()
    }

}).mount(
    "#profileApp"
)