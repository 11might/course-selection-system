<script setup>
import {ref, onMounted} from 'vue'
import {getCourses} from '../api/course'

const courses = ref([])

async function loadCourses(){
  const res = await getCourses()
  courses.value = res.data.courses
}

onMounted(loadCourses)
</script>

<template>
  <div>
    <h2>课程列表</h2>
    <table border="1">
      <tr><th>课程名</th><th>学分</th><th>容量</th></tr>
      <tr v-for="c in courses" :key="c.id">
        <td>{{ c.course_name }}</td>
        <td>{{ c.credit }}</td>
        <td>{{ c.capacity }}</td>
      </tr>
    </table>
  </div>
</template>