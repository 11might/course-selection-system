import request from './request'

// 登录：把用户名密码发给后端
export function login(username,password){
    return request.post('/login',null,{
        params:{username,password}
    })
}
