import React from "react";
import { useRouter } from "next/router";
import { useState, useEffect, useContext } from "react";
import { userContext } from '../context';
import Link from "next/link";
import "../styles/globals.css";

function Classrooms() {
    const context = useContext(userContext);
    const user = context ? context.user : undefined;
    const email = user ? user.email : '';
    const pwd = user ? user.pwd : '';
    const role = user ? user.type : '';

    const [classrooms, setClassrooms] = useState([]);
        
    useEffect( () => {
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
        })
    })

    const router = useRouter();
    const [userClassroom, setUserClassroom] = useState([]);
    
    const handleSubmit = (classroom: any) => {
      setUserClassroom(classroom);
      router.push({
        pathname: `/teacher-class-menu/${userClassroom}`,
        query: { classroom: JSON.stringify(classroom) }
      });
    }

  return (
    <div id="main" className="flex flex-col min-h-screen">
      <header className="w-full bg-gray-800 text-white py-4">
       
      </header>
    <main className="flex flex-row items-center justify-center flex-grow py-2">
      <div>
        {classrooms.map((data, index) => (
          <div key={index} className="mb-4">
            {Object.keys(data).map((key, idx) => (
              <p 
                key = {idx + 1} 
                className="cursor-pointer text-blue-500 hover:underline"
                onClick={() => handleSubmit(data[key])}
              >
                <strong>Classroom {idx + 1}: </strong> {data[key]}
              </p>
            ))}
          </div>
        ))}
      </div>
    </main>
  </div>
  );
}

export default Classrooms;