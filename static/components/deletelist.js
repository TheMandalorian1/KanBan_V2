const deletelist = {
  template: `
  <div class="top">
  <div class="upbox card" style="width: 30rem; background-color:#f7786b">    
      <h3 class="head">Are you sure, you want to delete this list?</h3>
      
      <form @submit.prevent="delList" >
        <div>
        <p class="head"><label for="name">Move cards to: </label>
          <select name="list" id="in" v-model="list"
          id="typeNameX-2" class="form-control form-control" id="in" style="height:32px; width: 220px">
            <option :value="l[0]" v-for="l in lister" v-if="l[0] != listId">{{l[1]}}</option>
          </select></p>

          <div class="sub">
            <button class="newb " id="btn">Yes</button>
          </div>  
        </div>

      </form>
      <div class="sub">
          <button onclick="history.back()" class="newb" id="btnc">Cancel</button>
      </div>    
  </div>  
</div>`,
  data() {
    return {
      lister: "",
      listId: this.$route.params.listId,
      list: ""
    }
  },

  async mounted() {
    const res = await fetch('/api/dashboard', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + localStorage.getItem('accessToken')
      }
    })
    
    if (res.ok) {
      const d = await res.json()
      this.lister = d.lister;
    } else (
      alert(res.message)
    )
  },

  methods: {
    delList: async function () {
      const req = await fetch(`/api/dlist/${this.$route.params.listId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('accessToken')
        },
        body: JSON.stringify({
          mlistId: this.list,

        })
      })

      if (req.ok) {
        alert("List has been deleted!")
        this.$router.push({ path: '/dashboard' })
      } else {
        alert(await req.json().message)
      }
    }
  }
}

export default deletelist