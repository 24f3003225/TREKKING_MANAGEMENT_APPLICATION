const { createApp } = Vue

createApp({

    data() {
        return {
            email: "",
            password: ""
        }
    },

    methods: {

        async loginUser() {

            const response = await fetch(
                "/auth/login",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        email: this.email,
                        password: this.password
                    })
                }
            )

            const data = await response.json()

            if (data.success) {

                localStorage.setItem(
                    "token",
                    data.token
                )

                localStorage.setItem(
                    "user",
                    JSON.stringify(data.user)
                )

                if (data.user.role === "admin") {
                    window.location.href = "/admin/dashboard"
                }
                else if (data.user.role === "staff") {
                    window.location.href = "/staff/dashboard"
                }
                else {
                    window.location.href = "/user/dashboard"
                }
            }
        }
    }


}).mount("#loginApp")
