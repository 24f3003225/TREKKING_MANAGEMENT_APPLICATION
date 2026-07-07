Vue.createApp({

    data() {

        return {

            participants: []
        }
    },

    methods: {

        async loadParticipants() {

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
                    `/staff/participants/${trekId}`,
                    {
                        headers: {
                            Authorization:
                                `Bearer ${token}`
                        }
                    }
                )

            this.participants =
                await response.json()
        }

    },

    mounted() {

        this.loadParticipants()
    }

}).mount(
    "#participantsApp"
)