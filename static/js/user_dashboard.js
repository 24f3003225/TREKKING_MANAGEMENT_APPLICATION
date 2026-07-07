const { createApp } = Vue

createApp({

    data() {

        return {

            totalTreks: 0,
            totalBookings: 0,
            activeTreks: 0

        }
    },

    methods: {

        async loadDashboard() {

            const token =
                localStorage.getItem("token")

            const response =
                await fetch(
                    "/user/dashboard-data",
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

            this.activeTreks =
                data.active_treks
        }
    },

    mounted() {

        this.loadDashboard()
    }

}).mount("#userDashboardApp")