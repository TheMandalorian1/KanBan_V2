const summary = {
    template: `<div>
    <nav>
        <h2>KanBan:&nbsp   <i class="bi bi-person-square"></i>{{username}}  </h2>
        <ul>
            <router-link to="/dashboard"><button class="btn btn-primary"><i class="bi bi-kanban-fill"></i> Dashboard</button></router-link>&nbsp;|&nbsp; 
            <button class="btn btn-danger" @click="logout"><i class="bi bi-box-arrow-right"></i> Logout</button>
        </ul>
    </nav>
    <!--<div v-if="Object.keys(lister).length == 0">
        <h4>There is no list on the board.</h4>
        <router-link to="/addlist"><button>createlist</button></router-link>
    </div>

    <div v-else="Object.keys(lister).length > 0">-->
        <div class="cont">
            <!-- Container of a List -->
            <div class="box1 card" v-for="d in lister" >
                <h5 class="card-title">{{d[0]}} : Summary</h5>
                <ul class="list-group list-group-flush" style="margin: 0px;">
                <li class="list-group-item"><p class="present" id="comp" style="height: 30px; width: 220px">{{d[2]}}/{{d[1]}} Completed</p></li>
                <li class="list-group-item"><p class="present" id="pen" style="height: 30px; width: 220px">{{d[3]}}/{{d[1]}} Pending</p></li>
                <li class="list-group-item"><p class="present" id="fail" style="height: 30px; width: 220px">{{d[4]}}/{{d[1]}} Failed to complete</p></li>
                </ul>
                <div class="nest" style="min-height: 420px;">
                <div>
                    <img :src="'/static/images/'+ d[5]+ '.PNG'" alt="pie chart" width="320px" height="300px">
                    <img :src="'/static/images/'+ d[5]+ 'tdline.PNG'" alt="trendline chart" width="320px" height="300px">
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
      const res = await fetch('/api/summary', {
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
    methods:{
      logout: async function(){
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
      
      }
  }
  }
  
export default summary