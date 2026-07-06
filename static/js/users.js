const { createApp } = Vue

createApp({

    data() {

        return {

            users: [],
            search: ""
        }
    },

    methods: {

        async loadUsers() {

            const response =
                await fetch(
                    `/admin/users?search=${this.search}`
                )

            this.users =
                await response.json()
        },

        async deactivateUser(id) {

            const response =
                await fetch(
                    `/admin/deactivate-user/${id}`,
                    {
                        method: "PUT"
                    }
                )

            const data =
                await response.json()

            alert(data.message)

            this.loadUsers()
        },

        async activateUser(id) {

            const response =
                await fetch(
                    `/admin/activate-user/${id}`,
                    {
                        method: "PUT"
                    }
                )

            const data =
                await response.json()

            alert(data.message)

            this.loadUsers()
        }
    },

    mounted() {

        this.loadUsers()
    }

}).mount("#usersApp")