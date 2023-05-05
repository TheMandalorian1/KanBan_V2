const login = {
    template: `
<div class="top">
    <div class="upbox card" style="height: 450px; width: 350px; background-color:#92a8d1;">

        <h1 class="head">Login</h1>
        
        <form @submit.prevent="dologin">
            <div class="info form-outline mb-4">
                <input type="email" id="typeEmailX-2" class="form-control form-control-lg" 
                 placeholder="Email" required v-model="mail" name="mail"/>
            </div>

            <div class="info form-outline mb-4">
                <input type="password" id="typePasswordX-2" class="form-control form-control-lg" 
                pattern="[A-Za-z0-9]{0,15}" placeholder="Password" required v-model="pass" name="pass"/>
            </div>

            <div class="sub">
                <button class="buton btn btn-primary" type="submit">Login</button>    
            </div>
        </form>

        <div class="sub">
            <router-link to="/register"><button type="submit" class="buton btn btn-secondary">Register</button></router-link>
        </div>
    </div>  
</div>`,

    data() {
        return {
            mail: "",
            pass: ""
        }
    },

    methods: {
        dologin: async function () {
            const req = await fetch('/api/login?' + "email=" + this.mail + "&" + "password=" + this.pass, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },

            })
            const res = await req.json();
            if (req.ok) {
                
                if (res.token){
                    // console.log(res.token);
                    localStorage.setItem('accessToken', res.token);
                    this.$router.push({ path: '/dashboard' })
                } else{
                    alert(res.message)
                }
            } else {
                alert(res.message)
            }
        }
    }
}

export default login