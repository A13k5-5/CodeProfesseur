import React from "react";
import { useRouter } from "next/router";
import { useState, useEffect, useContext } from "react";
import { userContext, classContext } from '../context';
import "../styles/globals.css";
import Link from "next/link";

function TeacherClassMenu() {
  const context = useContext(userContext);
  const user = context ? context.user : undefined;
  const email = user ? user.email : '';
  const pwd = user ? user.pwd : '';
  const role = user ? user.type : '';

  const router = useRouter();
  const { classroom } = router.query;

  console.log("Classroom Received: ", classroom);

  const classroomContext = useContext(classContext);
  if (!classroomContext){
    console.log("Classroom Context does not appear")
  }
  const class_interface = classroomContext ? classroomContext.classroom : undefined;
  if (!class_interface){
    console.log("Class Interface does not appear")
  }
  const setClassroom = classroomContext ? classroomContext.setClassroom : undefined;

  const [classrooms, setClassrooms] = useState([]);
      
  useEffect(() => {
    fetch("http://localhost:8080/api/classrooms", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, pwd, role })
    })
      .then(response => response.json())
      .then((data) => {
        setClassrooms(data);
      });
  }, [email, pwd, role]);

  useEffect(() => {
          fetch("http://localhost:8080/api/classroom_id", {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ classroom })
          })
              .then(response => response.json())
              .then((data) => {
                  if (setClassroom) {
                      setClassroom({
                        class_id: data,
                        class_questions: []
                      });
                  }
              });
      }, [classroom]);

  if (class_interface) {
    console.log("ClassId in context: ", class_interface.class_id);
  } else {
    console.log("ClassId: Not available");
  }

  const handleSubmit = (classroom: any) => {
    router.push({
      pathname: `/teacher-class-menu`,
      query: { classroom: JSON.stringify(classroom) }
    });
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <header className="w-full bg-blue-600 text-white py-4 shadow-md">
        <h1 className="text-center text-3xl font-bold">Teacher Class Menu</h1>
      </header>
      <main className="flex flex-col items-center justify-center flex-grow space-y-6 mt-10">
        <Link href={{pathname: "/teacher-class-qs", query: {classroom : classroom}}} className="w-64 text-center bg-blue-500 text-white font-bold py-3 px-6 rounded-lg shadow-md hover:bg-blue-700 transition duration-300">
          View Questions
        </Link>
        <Link href={{pathname: "/teacher-class-students", query: {classroom : classroom}}} className="w-64 text-center bg-green-500 text-white font-bold py-3 px-6 rounded-lg shadow-md hover:bg-green-700 transition duration-300">
          View Students
        </Link>
        <Link href="/create-question" className="w-64 text-center bg-yellow-500 text-white font-bold py-3 px-6 rounded-lg shadow-md hover:bg-yellow-600 transition duration-300">
          Create a Question
        </Link>
      </main>
      <footer className="w-full bg-gray-800 text-white py-4 text-center">
        <p className="text-sm">© 2025 Teacher Portal</p>
      </footer>
    </div>
  );
}

export default TeacherClassMenu;