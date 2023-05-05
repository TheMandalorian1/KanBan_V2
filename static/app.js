import dashboard from "./components/dashboard.js"
import summary from "./components/summary.js"
import login from "./components/login.js"
import register from "./components/register.js"
import addlist from "./components/addlist.js"
import addcard from "./components/addcard.js"
import editcard from "./components/editcard.js"
import editlist from "./components/editlist.js"
import deletelist from "./components/deletelist.js"
import deletecard from "./components/deletecard.js"

const routes = [
    { path: '/', component: login },
    { path: '/summary', component:summary },
    { path: '/dashboard', component: dashboard},
    { path: '/login', component: login },
    { path: '/register', component: register },
    { path: '/addlist', component: addlist },
    { path: '/:listId/addcard', component: addcard },
    { path: '/editcard/:cardId', component: editcard },
    { path: '/editlist/:listId', component: editlist, name: "editlist"},
    { path: '/deletelist/:listId', component: deletelist, name: "deletelist"},
    { path: '/dcard/:cardId', component: deletecard, name: "deletecard"},
]

const router = new VueRouter({
    routes,
    base: '/'
})
const add = new Vue({
    el: "#add",
    router,
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
})