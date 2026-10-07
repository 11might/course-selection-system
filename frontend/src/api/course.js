import request from './request'

export function getCourses(){
    return request.get('/courses')
}
export function getMyCourses(){
    return request.get('/my-courses')
}