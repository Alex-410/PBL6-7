import {ref} from 'vue'
import {useRouter} from 'vue-router'

// 从 localStorage 读取并标准化当前登录用户。各角色 Dashboard 页面共用。
export function useCurrentUser(){
  const router=useRouter()
  const cu=ref<any>({})
  function load(){
    const s=localStorage.getItem('user')
    if(!s){router.push('/');return}
    try{
      const u=JSON.parse(s)
      const rawRole=(u.role||'student').toLowerCase()
      const roleMap:Record<string,string>={user:'student',admin:'admin',publisher:'publisher',student_publisher:'student_publisher'}
      const mappedRole=roleMap[rawRole]||'student'
      cu.value={...u,role:mappedRole,name:u.nickname||u.username,college:u.college||'未知',grade:u.grade||'—',avatar:u.avatar||u.username?.charAt(0)||'?',tags:u.tags||[]}
    }catch{router.push('/')}
  }
  function logout(){
    sessionStorage.removeItem('selectedActivity')
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    router.push('/')
  }
  return {cu,load,logout}
}
