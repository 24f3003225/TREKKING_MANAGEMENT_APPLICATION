const { createApp } = Vue

createApp({

    mounted() {

        const token =
            localStorage.getItem(
                "token"
            )

        const user =
            JSON.parse(
                localStorage.getItem(
                    "user"
                )
            )

        if (!token) {

            alert("Please Login")

            window.location.href =
                "/login"

            return
        }

        if (!user ||
            user.role !== "admin") {

            alert("Access Denied")

            window.location.href =
                "/login"

            return
        }

    }

}).mount("#adminApp")