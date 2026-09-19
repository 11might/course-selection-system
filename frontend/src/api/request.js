import axios from 'axios'

const request= axios.create({
    baseURL:'http://localhost:8080',
    timeout:15000,
})
// 请求发出前：自动带头
request.interceptors.request.use((config)=>{
    const token=localStorage.getItem('token')
    if(token){
        config.headers.Authorization=`Bearer ${token}`
    }
    return config
})
export default  request