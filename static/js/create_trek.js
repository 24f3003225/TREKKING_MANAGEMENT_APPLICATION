Vue.createApp({

    data() {
        return {

            name: "",
            location: "",
            difficulty: "",
            duration: "",
            available_slots: "",
            description: "",
            start_date: "",
            end_date: "",

            staff_id: "",
            staffs: []
        }
    },

    methods: {

        async createTrek() {

            const token = localStorage.getItem("token")

            const response = await fetch(
                "/admin/create-trek",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${localStorage.getItem("token")}`
                    },
                    body: JSON.stringify({

                        name: this.name,
                        location: this.location,
                        difficulty: this.difficulty,
                        duration: this.duration,
                        available_slots: this.available_slots,
                        description: this.description,
                        start_date: this.start_date,
                        end_date: this.end_date,

                        staff_id: this.staff_id
                    })
                }
            )

            const data = await response.json()

            alert(data.message)
        },
        async loadStaffs() {

            const response =
                await fetch(
                    "/admin/staff-list"
                )

            this.staffs =
                await response.json()
        }
    },
    mounted() {
        this.loadStaffs()
    }


}).mount("#createTrekApp")