const deletecard = {
    template: `
    <div class="top">
      <div class="upbox card" style="width: 25rem; height:300px; background-color:#f7786b">
     
        <h3 class="head">Are you sure, you want to delete this card?</h3>
        <form @submit.prevent="delCard">

          <div class="sub">
            <button class="newb" id="btn">Yes</button>
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
        lcardId: this.$route.params.listId,
        list: ""
      }
    },
  
    // async beforeMount() {
    //   const res = await fetch('/api/dashboard')
    //   if (res.ok) {
    //     const d = await res.json()
    //     this.lister = d;
    //   } else (
    //     alert(res.message)
    //   )
    // },
  
    methods: {
      delCard: async function () {
        const req = await fetch(`/api/dcard/${this.$route.params.cardId}`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('accessToken')
          },
        })
  
        if (req.ok) {
          alert("Card has been deleted!")
          this.$router.push({ path: '/dashboard' })
        } else {
          alert(await req.json().message)
        }
      }
    }
  }
  
  export default deletecard