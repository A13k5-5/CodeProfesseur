import React from "react";
import { useRouter } from "next/router";
import { useState, useEffect, useContext } from "react";
import { userContext } from '../context';
import Link from "next/link";
import "../styles/globals.css";
import Image from "next/image";

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

    const [showLogout, setShowLogout] = useState(false); 

    const handleLogOut = () => {
      window.location.href = "/sign-in";
    }

    return (
      <div id="main" className="flex flex-col min-h-screen">
        <header className="w-full bg-gray-800 text-white py-4">
          <div className="container mx-auto px-4 flex justify-between items-center">
            <h2
              className="ml-auto text-right text-xl cursor-pointer"
              onClick={() => setShowLogout(!showLogout)} 
            >
              {email}
            </h2>
            {showLogout && (
              <button
                className="absolute top-16 right-4 bg-red-500 text-white px-4 py-2 rounded shadow-md"
                onClick={handleLogOut}
              >
                Log Out
              </button>
            )}
          </div>
          <div className="container mx-auto flex justify-center space-x-4">
            <h2 className="text-center text-2xl font-bold">
              <Link href={role === 1 ? "/teacher-class" : "/student-class"}>
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
          {/*<Image 
            src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3l5Y3M5OGt6dHlmNzVjbWtpbmJtcXYwZG44Nmh5aWx1Y3o1MGFzMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/a5viI92PAF89q/giphy.gif" 
            alt="Loading animation" 
            width={500} 
            height={500} 
          />*/}
      </div>
    );
  }

export default StudentHome;