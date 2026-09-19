import { defineStore } from 'pinia'
import { ref } from 'vue'

// 准备「用户仓」里有什么货、能做什么操作
function setupUserStore() {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))

  function setLogin(data) {
    token.value = data.token
    userInfo.value = data.userInfo
    localStorage.setItem('token', data.token)
    localStorage.setItem('userInfo', JSON.stringify(data.userInfo))
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  return { token, userInfo, setLogin, logout }
}

// 建一个叫 user 的仓；useUserStore 是给别人用的「钥匙」
export const useUserStore = defineStore('user', setupUserStore)
