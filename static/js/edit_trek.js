const { createApp } = Vue

createApp({

    data() {
        return {

            trekId: null,

            name: "",
            location: "",
            difficulty: "",
            duration: "",
            available_slots: "",
            description: "",

            staff_id: "",
            staffs: []
        }
    },

    methods: {

        async loadTrek() {

            const token =
                localStorage.getItem("token")

            const response =
                await fetch(
                    `/admin/trek/${this.trekId}`,
                    {
                        headers: {
                            "Authorization":
                                `Bearer ${token}`
                        }
                    }
                )

            const trek =
                await response.json()

            this.name = trek.name
            this.location = trek.location
            this.difficulty = trek.difficulty
            this.duration = trek.duration
            this.available_slots =
                trek.available_slots
            this.description =
                trek.description
            this.staff_id =
                trek.staff_id
        },
        async loadStaffs() {

            const response =
                await fetch(
                    "/admin/staff-list"
                )

            this.staffs =
                await response.json()
        },

        async updateTrek() {

            const token =
                localStorage.getItem("token")

            const response =
                await fetch(
                    `/admin/update-trek/${this.trekId}`,
                    {
                        method: "PUT",

                        headers: {
                            "Content-Type":
                                "application/json",

                            "Authorization":
                                `Bearer ${token}`
                        },

                        body: JSON.stringify({

                            name: this.name,
                            location: this.location,
                            difficulty: this.difficulty,
                            duration: this.duration,
                            available_slots: this.available_slots,
                            description: this.description,

                            staff_id: this.staff_id
                        })
                    }
                )

            const data =
                await response.json()

            alert(data.message)

            window.location.href =
                "/admin/treks-page"
        }

    },

    mounted() {

        this.trekId =
            window.location.pathname
                .split("/")
                .pop()

        this.loadStaffs()

        this.loadTrek()
    }

}).mount("#editTrekApp")