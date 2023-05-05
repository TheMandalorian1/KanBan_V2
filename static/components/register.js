const register = {
    template: `
    <div class="top ">
        <div class="upbox card" style="height: 550px; width: 350px; background-color:#92a8d1;">

            <h1 class="head">Register</h1>

            <form @submit.prevent="doregister">

                <div class="info form-outline mb-4" >
                    <input type="text" id="typeNameX-2" class="form-control form-control-lg" name="name" placeholder="Name" required maxlength="30" 
                    pattern="[A-Za-z0-9_ ]{2,}" v-model="name">
                </div>

                <div class="info form-outline mb-4">
                    <input type="email" id="typeEmailX-2" class="form-control form-control-lg" name="mail" placeholder="Email" required maxlength="100" v-model="mail">
                </div>

                <div class="info form-outline mb-4">
                    <input type="password" id="typePasswordX-2" class="form-control form-control-lg" name="pass" placeholder="Password" required 
                    pattern="[A-Za-z0-9]{6,15}" maxlength="15" minlength="6" v-model="pass">
                </div>

                <div class="sub">
                    <button type="submit" class="btn btn-primary buton" id="">Register</button>    
                </div>
            </form>

            <div class="sub">
            <router-link to="/login"><button type="submit" class="btn btn-secondary buton">Login</button></router-link>    
            </div>
        </div>  
    </div>`,

    data() {
        return {
            name: "",
            mail: "",
            pass: "",
        }
    },

    methods: {
        doregister: async function() {
            console.log(this.mail, this.pass, this.name)
        const req = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: this.name,
                email: this.mail,
                password: this.pass
            })
            
        })
        const res = await req.json();
        if (req.ok){
            if (res.token){
                localStorage.setItem('accessToken', res.token);
                this.$router.push({ path: '/dashboard' })
                alert("User Registerd!")
            } else{
                alert("Invalid Input")
            }            
        }else{
            alert("Invalid Input")
        }
    }
}}

export default register 