Vue.createApp({

    data() {
        return {
            treks: []
        }
    },

    methods: {

        async loadTreks() {

            const token = localStorage.getItem("token")

            const response = await fetch(
                "/admin/treks",
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            )

            const data = await response.json()

            this.treks = data
        },

        async deleteTrek(id) {

            const token = localStorage.getItem("token")

            await fetch(
                `/admin/delete-trek/${id}`,
                {
                    method: "DELETE",
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            )

            this.loadTreks()
        },

        editTrek(id) {

            window.location.href =
                `/admin/edit-trek/${id}`
        }

    },

    mounted() {
        this.loadTreks()
    }

}).mount("#treksApp")