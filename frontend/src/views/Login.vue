<script setup>
import {ref} from 'vue'
import {login} from '../api/auth'
import {useUserStore} from '../store/user'
import {useRouter} from "vue-router";

const router=useRouter()
const userStore=useUserStore()
const username=ref('')
const password=ref('')

async function onLogin(){
  const res=await login(username.value,password.value)
  if (res.data.msg!='ok'){
    alert(res.data.msg || '登录失败')
    return
  }
  userStore.setLogin(res.data.data)
  router.push('/home')
  alert('登录成功')

}
</script>

<template>
  <div>
    <input v-model="username" placeholder="用户名">
    <input v-model="password" type="password" placeholder="密码">
    <button @click="onLogin">登录</button>
  </div>
</template>
