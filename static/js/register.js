const { createApp } = Vue

createApp({

    data() {
        return {
            name: "",
            email: "",
            phone: "",
            password: ""
        }
    },

    methods: {

        async registerUser() {

            const response = await fetch(
                "/auth/register",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        name: this.name,
                        email: this.email,
                        phone: this.phone,
                        password: this.password
                    })
                }
            )

            const data = await response.json()

            alert(data.message)

            if (data.success) {
                window.location.href = "/login"
            }
        }
    }

}).mount("#registerApp")