Vue.createApp({

    data() {

        return {

            available_slots: 0
        }
    },

    methods: {

        async loadTrek() {

            const token =
                localStorage.getItem(
                    "token"
                )

            const trekId =
                new URLSearchParams(
                    window.location.search
                ).get(
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

            const data =
                await response.json()

            this.available_slots =
                data.available_slots
        },

        async updateSlots() {

            const token =
                localStorage.getItem(
                    "token"
                )

            const trekId =
                new URLSearchParams(
                    window.location.search
                ).get(
                    "trek_id"
                )

            const response =
                await fetch(
                    `/staff/update-slots/${trekId}`,
                    {
                        method: "PUT",

                        headers: {

                            "Content-Type":
                                "application/json",

                            Authorization:
                                `Bearer ${token}`
                        },

                        body: JSON.stringify({

                            available_slots:
                                this.available_slots
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
    "#slotsApp"
)