const { createApp } = Vue

createApp({

    data() {

        return {

            bookings: []
        }
    },

    methods: {

        async loadBookings() {

            const response =
                await fetch(
                    "/admin/bookings"
                )

            this.bookings =
                await response.json()
        }
    },

    mounted() {

        this.loadBookings()
    }

}).mount("#bookingApp")