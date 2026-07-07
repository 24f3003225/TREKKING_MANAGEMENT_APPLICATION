const { createApp } = Vue

createApp({

    data() {

        return {

            bookings: [],

            taskId: "",

            downloadFile: ""

        }
    },
    methods: {

        async loadBookings() {

            const user =
                JSON.parse(
                    localStorage.getItem(
                        "user"
                    )
                )

            const token =
                localStorage.getItem(
                    "token"
                )

            const response =
                await fetch(
                    `/user/my-bookings/${user.id}`,
                    {
                        headers: {

                            Authorization:
                                `Bearer ${token}`
                        }
                    }
                )

            this.bookings =
                await response.json()
        },
        async exportHistory() {
            console.log("Export button clicked");
            const token =
                localStorage.getItem(
                    "token"
                )

            const response =
                await fetch(
                    "/user/export-history",
                    {

                        headers: {

                            Authorization:
                                `Bearer ${token}`

                        }

                    }
                )

            const data =
                await response.json()

            this.taskId =
                data.task_id

            alert(
                "Export Started..."
            )

            this.checkStatus()

        },
        async checkStatus() {

            const token =
                localStorage.getItem(
                    "token"
                )

            const interval =
                setInterval(async () => {

                    const response =
                        await fetch(
                            `/user/export-status/${this.taskId}`,
                            {

                                headers: {

                                    Authorization:
                                        `Bearer ${token}`

                                }

                            }
                        )

                    const data =
                        await response.json()

                    if (
                        data.status ==
                        "Completed"
                    ) {

                        clearInterval(
                            interval
                        )

                        this.downloadFile =
                            data.file

                        alert(
                            "CSV Export Completed"
                        )

                    }

                }, 3000)

        },

        async cancelBooking(id) {

            const token =
                localStorage.getItem(
                    "token"
                )

            const response =
                await fetch(
                    `/user/cancel-booking/${id}`,
                    {
                        method: "PUT",

                        headers: {

                            Authorization:
                                `Bearer ${token}`
                        }
                    }
                )

            const data =
                await response.json()

            alert(data.message)

            this.loadBookings()
        }
    },

    mounted() {

        this.loadBookings()
    }

}).mount("#bookingApp")