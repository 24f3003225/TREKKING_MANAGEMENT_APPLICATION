const { createApp } = Vue

createApp({

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

            let url =
                "/user/treks?"

            if (this.difficulty) {

                url +=
                    `difficulty=${this.difficulty}&`
            }

            if (this.location) {

                url +=
                    `location=${this.location}&`
            }

            if (this.duration) {

                url +=
                    `duration=${this.duration}&`
            }

            const response =
                await fetch(
                    url,
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

        async bookTrek(trekId) {

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
                    `/user/book-trek/${trekId}`,
                    {
                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json",

                            Authorization:
                                `Bearer ${token}`
                        },

                        body: JSON.stringify({

                            user_id: user.id
                        })
                    }
                )

            const data =
                await response.json()

            alert(data.message)

            this.loadTreks()
        }

    },

    mounted() {

        this.loadTreks()
    }

}).mount("#treksApp")