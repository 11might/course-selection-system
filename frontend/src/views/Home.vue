<script setup>
import {useUserStore} from "../store/user.js";
import {useRouter} from "vue-router";
const router = useRouter();
const userStore = useUserStore();
function  onLogout(){
  userStore.logout()
  router.push('/login')

}
</script>
<template>
  <div>欢迎，{{userStore.userInfo.username}}</div>
  <router-link to="/courses">查看课程</router-link>
  <button @click="onLogout">退出</button>
</template>