Vue.createApp({

    data() {

        return {

            totalTreks: 0,
            totalBookings: 0
        }
    },

    methods: {

        async loadDashboard() {

            const token =
                localStorage.getItem(
                    "token"
                )

            const response =
                await fetch(
                    "/staff/dashboard-data",
                    {
                        headers: {
                            Authorization:
                                `Bearer ${token}`
                        }
                    }
                )

            const data =
                await response.json()

            this.totalTreks =
                data.total_treks

            this.totalBookings =
                data.total_bookings
        }

    },

    mounted() {

        this.loadDashboard()
    }

}).mount(
    "#staffDashboardApp"
)