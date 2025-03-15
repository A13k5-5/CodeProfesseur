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
    const id = user ? user.id : '';

    const [userData, setUserData] = useState([]);
        
    useEffect( () => {
      fetch("http://localhost:8080/api/classrooms", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, id })
      })
        .then(response => response.json())
        .then((data) => {
          setUserData(data);
        })
    })

  return (
    <div id="main" className="flex flex-col min-h-screen">
      <header className="w-full bg-gray-800 text-white py-4">
       
      </header>
    <main className="flex flex-row items-center justify-center flex-grow py-2">
      <p>
        {userData}
      </p>
    </main>
  </div>
  );
}

export default Classrooms;