Vue.createApp({

    data() {

        return {

            treks: []
        }
    },

    methods: {

        async loadTreks() {

            const token =
                localStorage.getItem(
                    "token"
                )

            const response =
                await fetch(
                    "/staff/my-treks",
                    {
                        headers: {
                            Authorization:
                                `Bearer ${token}`
                        }
                    }
                )

            this.treks =
                await response.json()
        },

        viewParticipants(id) {

            window.location.href =
                `/staff/participants-page?trek_id=${id}`
        },

        updateStatus(id) {

            window.location.href =
                `/staff/update-status-page?trek_id=${id}`
        },
        updateSlots(id) {

            window.location.href =
                `/staff/update-slots-page?trek_id=${id}`
        }

    },

    mounted() {

        this.loadTreks()
    }

}).mount(
    "#staffTreksApp"
)