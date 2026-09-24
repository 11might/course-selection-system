import request from './request'

export function getCourses(){
    return request.get('/courses')
}
