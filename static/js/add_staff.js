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

        async addStaff() {

            const response =
                await fetch(
                    "/admin/add-staff",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            name: this.name,
                            email: this.email,
                            phone: this.phone,
                            password: this.password
                        })
                    }
                )

            const data =
                await response.json()

            alert(data.message)

            if (response.ok) {

                window.location.href =
                    "/admin/staff"
            }
        }
    }

}).mount("#staffApp")