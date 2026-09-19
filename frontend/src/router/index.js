import {createRouter,createWebHistory} from "vue-router";
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'

const router=createRouter({
    history:createWebHistory(),
    routes:[
        {path:'/',redirect:'/login'},
        {path:'/login',component:Login},
        {path:'/home',component:Home},
    ],
})
router.beforeEach((to,from)=>{
    const token=localStorage.getItem('token')
    if (to.path=='/home' && !token){
        return '/login'
    }
})
export default router