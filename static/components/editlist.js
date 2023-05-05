const editlist = {
    template: `
    <div class="top">
        <div class="upbox card" style="height: 500px; width: 400px; background-color:#80ced6;">    
            <h1 class="head">Edit List</h1>
            
            <form @submit.prevent="editList" >
                <div class="info">
                    <label for="name"><p>Name: </p></label>
                    <input type="text" name="name" placeholder="Name" maxlength="20" required v-model="name" 
                    id="typeNameX-2" class="form-control form-control-lg">
                </div>
                <div class="info">
                    <label for="desc"><p>Description: </p></label>
                    <p><textarea name="desc" cols="22" rows="2" placeholder="Description...." required maxlength="100" 
                    v-model="desc" id="typeNameX-2" class="form-control form-control-lg"></textarea></p>
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
            name: "",
            desc: "",
        }
    },
    async beforeMount() {
        const req = await fetch(`/api/list/${this.$route.params.listId}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': 'Bearer ' + localStorage.getItem('accessToken')
            }
          })
        const info = await req.json()
        if (req.ok) {
            this.name = info.List_name
            this.desc = info.List_desc

        } else {
            this.$router.push({ path: '/login' })
            alert(info.message)
        }
    },

    methods: {
       editList: async function () {
            const req = await fetch(`/api/elist/${this.$route.params.listId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('accessToken')
                },
                body: JSON.stringify({
                    name: this.name,
                    description: this.desc
                })
            })

            if (req.ok) {
                alert("List has been edited!")
                this.$router.push({ path: '/dashboard' })
            } else {
                this.$router.push({ path: '/login' })
                alert(req.message)
            }
        },
    }
}

export default editlist