const { createApp } = Vue

createApp({

    data() {

        return {

            staffs: [],
            search: ""
        }
    },

    methods: {

        async loadStaffs() {

            const response =
                await fetch(
                    `/admin/staff?search=${this.search}`
                )

            this.staffs =
                await response.json()
        },

        async deactivateStaff(id) {

            const response =
                await fetch(
                    `/admin/deactivate-staff/${id}`,
                    {
                        method: "PUT"
                    }
                )

            const data =
                await response.json()

            alert(data.message)

            this.loadStaffs()
        },

        async activateStaff(id) {

            const response =
                await fetch(
                    `/admin/activate-staff/${id}`,
                    {
                        method: "PUT"
                    }
                )

            const data =
                await response.json()

            alert(data.message)

            this.loadStaffs()
        }
    },

    mounted() {

        this.loadStaffs()
    }

}).mount("#staffApp")