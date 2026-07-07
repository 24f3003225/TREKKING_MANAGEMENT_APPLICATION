const { createApp } = Vue

createApp({

    data() {

        return {

            loading: false,

            taskId: "",

            report: null

        }

    },

    methods: {

        async generateReport() {

            this.loading = true

            this.report = null

            const token =
                localStorage.getItem(
                    "token"
                )

            const response =
                await fetch(
                    "/admin/monthly-report",
                    {

                        method: "POST",

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
                            `/admin/report-status/${this.taskId}`,
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

                        this.loading = false

                        this.report =
                            data.report

                        alert(
                            "Monthly Report Generated Successfully"
                        )

                    }

                }, 2000)

        }

    }

}).mount("#reportApp")