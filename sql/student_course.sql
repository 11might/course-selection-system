use course_selection;
create table `student_course`(
id int primary key auto_increment,
student_id int not null,
course_id int not null,
unique key uk_student_course(student_id,course_id)
);