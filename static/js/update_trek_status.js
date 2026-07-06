Vue.createApp({

    data() {

        return {

            trek: {},

            newStatus: ""
        }
    },

    methods: {

        async loadTrek() {

            const token =
                localStorage.getItem(
                    "token"
                )

            const params =
                new URLSearchParams(
                    window.location.search
                )

            const trekId =
                params.get(
                    "trek_id"
                )

            const response =
                await fetch(
                    `/staff/trek/${trekId}`,
                    {
                        headers: {
                            Authorization:
                                `Bearer ${token}`
                        }
                    }
                )

            this.trek =
                await response.json()

            this.newStatus =
                this.trek.status
        },

        async updateStatus() {

            const token =
                localStorage.getItem(
                    "token"
                )

            const params =
                new URLSearchParams(
                    window.location.search
                )

            const trekId =
                params.get(
                    "trek_id"
                )

            const response =
                await fetch(
                    `/staff/update-status/${trekId}`,
                    {
                        method: "PUT",

                        headers: {

                            "Content-Type":
                                "application/json",

                            Authorization:
                                `Bearer ${token}`
                        },

                        body: JSON.stringify({

                            status:
                                this.newStatus
                        })
                    }
                )

            const data =
                await response.json()

            alert(
                data.message
            )

            window.location.href =
                "/staff/treks-page"
        }

    },

    mounted() {

        this.loadTrek()
    }

}).mount(
    "#statusApp"
)