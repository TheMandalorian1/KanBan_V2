const editcard = {
    template: `
    <div class="top">
    <div class="upbox card" style="height: 650px; width: 450px; background-color:#80ced6; ">
        <h1 class="head">Edit Task</h1>

        <form @submit.prevent="editCard" >

        <div class="info" >
        <label for="name"><p class="formp" id="in">Select List: </p></label>

        <select name="list" v-model="list" id="typeNameX-2" 
        class="form-control form-control" id="in" style=" width: 250px">                 
            <option :value="lId">{{ lister[lId][1] }}</option>                                      
            <option :value="l[0]" v-for="l in lister" v-if="l[0] != lId">{{l[1]}}</option>
        </select>
        </div>

        <div class="info" >
        <label for="desc"><p class="formp" id="in">Title: </p></label>
        <input type="text" name="name" placeholder="Title" maxlength="20" required v-model="name" 
        id="typeNameX-2" class="form-control form-control" id="in" style=" width: 300px">
    </div>

    <div class="info">
        <label for="desc"><p class="formp" id="in">Content: </p></label>
        <textarea name="desc" cols="22" rows="2" placeholder="Content" maxlength="100" required 
        id="typeNameX-2" class="form-control form-control" id="in" v-model="desc"></textarea>
    </div>

            <div class="info" >
                <label for="deadline"><p class="formp" id="in">Deadline: </p></label>
                <input type="datetime-local" name="deadline" required v-model="deadline" :min="td"
                id="typeNameX-2" class="form-control form-control" id="in" style="height: 40px; width: 250px">
            </div>

            <div class="info">
            <label for="status"><p class="formp" id="in">Completed: </p></label>
                <!--<input type="checkbox" name="status" class="check" v-model="status" disabled checked>-->

                <input type="checkbox" v-if="status == 'Completed'" name="status" class="check" v-model="status" disabled checked>
                <input type="checkbox" v-else-if="status == 'Failed to complete'" name="" class="check" disabled>
                <input type="checkbox" v-else name="status" value="" class="check" v-model="status">
            </div>

            <div class="sub">
                <button type="submit" class="newb" id="btn">Save</button>
            </div>
        </form>

        <div class="sub">
            <button onclick="history.back()" class="newb" id="btnc">Cancel</button>
        </div>
    </div>
</div>`,

    data() {
        return {
            list: this.$route.params.listId,
            lister: "",
            name: "",
            desc: "",
            deadline: "",
            status: "",
            lId: this.$route.params.listId,
            td:""
        }
    },

    async mounted() {
        console.log(this.status)
        const res = await fetch('/api/dashboard', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + localStorage.getItem('accessToken')
            }
          })
        const req = await fetch(`/api/card/${this.$route.params.cardId}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + localStorage.getItem('accessToken')
            }
          })

        const d = await res.json()
        const c = await req.json()

        if (res.ok) {
            this.lister = d.lister;
        } else (
            confirm(res.message)
        )
        if (req.ok) {
            this.lId = c.Listc_id
            this.list = c.Listc_id
            this.name = c.Card_title
            this.desc = c.Card_content
            this.deadline = c.Card_dline
            this.status = c.Card_status
            this.td = c.td
        } else (
            this.$router.push({ path: '/dashboard' }),
            alert(res.message)
        )
    },

    methods: {
        editCard: async function () {
            const req = await fetch(`/api/ecard/${this.$route.params.cardId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('accessToken')
                },
                body: JSON.stringify({
                    list: this.list,
                    title: this.name,
                    content: this.desc,
                    deadline: this.deadline,
                    status: this.status
                })
            })

            if (req.ok) {
                this.$router.push({ path: '/dashboard' })
            } else {
                const d = await req.json()
                this.$router.push({ path: '/dashboard' })
                alert(d.message)
            }
        },

    }
}

export default editcard