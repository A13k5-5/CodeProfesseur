import React from "react";
import { useRouter } from "next/router";
import { useState, useEffect, useContext } from "react";
import { userContext } from '../context';
import Link from "next/link";
import "../styles/globals.css";

function StudentHome() {
    const context = useContext(userContext);
    const user = context ? context.user : undefined;
    const email = user ? user.email : '';
    const pwd = user ? user.pwd : '';
    const role = user ? user.type: '';
    const setUser = context ? context.setUser : undefined;

    const [userData, setUserData] = useState([]);
        
    useEffect(() => {
      fetch("http://localhost:8080/api/user", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, pwd })
      })
        .then(response => response.json())
        .then((data) => {
          setUserData(data);
          console.log(data[0]);
        })
    })

  return (
    <div id="main" className="flex flex-col min-h-screen">
      <header className="w-full bg-gray-800 text-white py-4">
        <div className="container mx-auto px-4 flex justify-between items-center">
          <h2 className="text-right text-xl flex-grow">
            {email}
          </h2>
        </div>
        <div className="container mx-auto flex justify-center space-x-4">
          <h2 className="text-center text-2xl font-bold">
            <Link href={role === 1 ? "/teacher-class" : "student-class"}>
              View Classrooms
            </Link>
          </h2>
          <h2 className="text-center text-2xl font-bold">
            <Link href="/join-class">
            {role === 1 ? "Create a Classroom" : "Join a Classroom"}
            </Link>
          </h2>
        </div>
      </header>
    <main className="flex flex-row items-center justify-center flex-grow py-2">
      <p>Details</p>
        {userData.map((data, index) => (
          <div key={index} className="mb-4">
            <p><strong>Length of Data:</strong>{Object.keys(data).length}</p>
            <p><strong>Classroom:</strong> {data[5]}</p> 
            <p><strong>Question:</strong> {data[7]}</p> 
            <p><strong>Submission:</strong> {data[12]}</p>
          </div>
        ))}
    </main>
  </div>
  );
}

export default StudentHome;