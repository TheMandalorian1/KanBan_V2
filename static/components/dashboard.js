const dashboard = {
  template: `<div>
  <nav style="text-align: left;">

  <h2>KanBan:&nbsp   <i class="bi bi-person-square"></i>{{username}}  </h2> 

  <ul>
    <router-link to="/addlist" ><button class="btn btn-primary"><i class="bi bi-plus-circle"></i> Add List</button></router-link>&nbsp;|&nbsp;
    <router-link to="/summary" ><button class="btn btn-warning">Summary <i class="bi bi-kanban"></i></button></router-link>&nbsp;|&nbsp;
    <button class="btn btn-success" @click="transporter">Export <i class="bi bi-arrow-down-square"></i></button>&nbsp;|&nbsp;
    <button class="btn btn-danger" @click="logout"><i class="bi bi-box-arrow-right"></i> Logout </button>
  </ul>       
</nav>

<!--<div v-if="Object.keys(lister).length == 0" >
        <h4>There is no list on the board.</h4>
        <router-link to="/addlist"><button >createlist</button ></router-link>
    </div>
    
    <div v-else="Object.keys(lister).length > 0">-->

    <div class="cont">
      <!-- Container of a List -->
      <div class="box1 card" v-for="d in lister">

        <h5 class="card-title">{{d[1]}}</h5>
     
            <ul class="list-group list-group-flush" style="margin: 0px;">
            <li class="list-group-item">
            <router-link :to="d[0] + '/addcard'"><button class="btn btn-primary" >Task <i class="bi bi-plus-circle"> </button></router-link>
            <router-link :to="'/editlist/' + d[0]"><button class="btn btn-success"><i class="bi bi-pencil"></i></button></router-link>
            <router-link :to="'/deletelist/' + d[0]"><button class="btn btn-danger"><i class="bi bi-trash3"></i></button></router-link>
            </li>
            </ul>
              
              <!-- Container in the list for all Cards -->
              <div class="nest" style="min-height: 500px;">

              <!-- Container of a Card -->
              <div class="card car1" v-for="c in d[3]" style="height: 220px; width: 270px;">
             

                    <h5 class="card-title" style="text-align: center;">{{c[1]}}</h5>
                    
                    <div class="list-group-item" style="align-items: center; text-align: center;">
                    <router-link :to="'/editcard/' + c[0]"><button class="btn btn-success" style="height: 36px; width: 40px;"><i class="bi bi-pencil"></i></button></router-link>
                    <router-link :to="/dcard/ + c[0]"><button class="btn btn-danger" style="height: 36px; width: 40px; "><i class="bi bi-trash3"></i></button></router-link>
                    
                    <!--<router-link :to="'/editcard/' + c[0]" style="align-items: center;"><i class="bi bi-pencil"></i></router-link> |
                    <router-link :to="/dcard/ + c[0]" style="align-items: center;"><i class="bi bi-trash3"></i></router-link>-->
                    </div>  
            

                <p class="present" style="height: 60px; border-radius: 5px;"> {{c[2]}} </p>
                <p class="present"> {{c[3]}} </p>                     
                
                <p class="present" id="fail" v-if="c[4] == 'Failed to complete'"> {{c[4]}} </p>
                <p class="present" id="pen" v-if="c[4] == 'Pending'"> {{c[4]}} </p>   
                <p class="present" id="comp" v-if="c[4] == 'Completed'"> {{c[4]}} </p>  

              </div>

            </div>

        </div>
    </div>
    </div>
    <!--</div>-->`,

  data() {
    return {
      lister: '',
      username: '',
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

    const d = await res.json()
    if (res.ok) {
      this.lister = d.lister;
      this.username = d.user;
    } else {
      this.$router.push({ path: '/login' })
      // alert(d.message)
    }

  },

  methods: {
    logout: async function () {
      const req = await fetch("/api/logout", {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
      })

      const d = await req.json();
      if (req.ok) {
        localStorage.removeItem('accessToken');
        this.$router.replace({ path: '/login' })
      } else {
        alert(d.message)
      }

    },
    expert: async function() {
      const res = await fetch('http://127.0.0.1:5000/export', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('accessToken')
        }
      })
  
      if (res.ok) {
        const d = await res.blob()  
        var a = document.createElement("a");
        a.href = window.URL.createObjectURL(d);
        a.download = `${this.username}_details.csv`;
        a.click();
        this.$router.push({ path: '/dashboard' })
        alert("Dasboard Exported")
      } else {
        const d = await res.json()
        this.$router.push({ path: '/login' })
        alert(d.message)
      }
  
    },


    transporter: async function() {
      const res = await fetch('/api/export', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('accessToken')
        }
      })
  
      if (res.ok) {
        const d = await res.json()  
        this.$router.push({ path: '/dashboard' })
        alert(d)
      } else {
        const d = await res.json()
        this.$router.push({ path: '/login' })
        alert(d.message)
      }
  
    }
  }
}

export default dashboard