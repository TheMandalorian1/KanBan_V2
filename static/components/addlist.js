const addlist = {
    template: `
    <div class="top">
        <div class="upbox card" style="height: 500px; width: 400px; background-color:#80ced6;">    
            <h1 class="head">Add List</h1>
            
            <form @submit.prevent="addList" >
                <div class="info">
                    <label for="name"><p>Name:</p></label>
                    <input type="text" name="name" placeholder="Name" maxlength="20" required v-model="name" 
                    id="typeNameX-2" class="form-control form-control-lg">
                </div>
                <div class="info">
                    <label for="desc"><p>Description:</p></label>
                    <textarea name="desc" cols="22" rows="2" placeholder="Description...." required maxlength="100" 
                    v-model="desc" id="typeNameX-2" class="form-control form-control-lg"></textarea>
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

    methods: {
        addList: async function () {
            const req = await fetch('/api/createlist', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('accessToken')
                },
                body: JSON.stringify({
                    name: this.name,
                    description: this.desc
                })
            })
            const d = await req.json()
            if (req.ok) {
                alert("List has been created!")
                this.$router.push({ path: '/dashboard' })
            } else {
                // const d = req.json()
                alert(d.message)
                this.$router.push({ path: '/dashboard' })
            }
        }
    }
}

export default addlist