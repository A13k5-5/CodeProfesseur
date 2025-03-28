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
    const [loading, setLoading] = useState(true);
    const [showLogout, setShowLogout] = useState(false);
        
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
          setLoading(false);
        })
        .catch(error => {
          console.error("Error fetching classrooms:", error);
          setLoading(false);
        });
    }, [email, pwd, role]); // Added dependency array to prevent infinite loop

    const router = useRouter();
    const [userClassroom, setUserClassroom] = useState<Classroom | null>(null);
    
    interface Classroom {
      [key: string]: string;
    }

    const handleSubmit = (classroom: Classroom) => {
      setUserClassroom(classroom);
      router.push({
      pathname: `/teacher-class-menu`,
      query: { classroom: JSON.stringify(classroom) }
      });
    }

    const handleLogOut = () => {
      window.location.href = "/sign-in";
    }

  return (
    <div id="main" className="flex flex-col min-h-screen bg-gray-100">
      <header className="w-full bg-gray-800 text-white py-4 shadow-md">
        <div className="container mx-auto px-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">CodeProfesseur</h1>
          <div className="relative">
            <h2
              className="text-right text-xl cursor-pointer hover:text-blue-300 transition-colors"
              onClick={() => setShowLogout(!showLogout)}
            >
              {email}
            </h2>
            {showLogout && (
              <button
                className="absolute top-10 right-0 bg-red-500 text-white px-4 py-2 rounded shadow-md hover:bg-red-600 transition-colors"
                onClick={handleLogOut}
              >
                Log Out
              </button>
            )}
          </div>
        </div>
        <div className="container mx-auto flex justify-center space-x-6 mt-4">
          <Link href="/teacher-home" className="text-center text-xl font-semibold hover:text-blue-300 transition-colors">
            Back to Home
          </Link>
          <Link href="/join-class" className="text-center text-xl font-semibold hover:text-blue-300 transition-colors">
            Create a Classroom
          </Link>
        </div>
      </header>

      <main className="container mx-auto py-8 px-4 flex-grow">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-6 text-gray-800 border-b-2 border-blue-500 pb-2">Your Classrooms</h2>
          <p className="text-gray-600 text-lg mb-6">Select a classroom to view its content and manage students.</p>
        </div>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow-lg p-6">
            {classrooms.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {classrooms.map((data, index) => (
                  <div key={index} className="mb-4">
                    {Object.keys(data).map((key, idx) => (
                      <div 
                        key={idx} 
                        className="border border-gray-200 rounded-lg p-4 hover:bg-blue-50 transition-colors cursor-pointer shadow-sm"
                        onClick={() => handleSubmit(data[key])}
                      >
                        <h4 className="font-semibold text-lg text-gray-800">{data[key]}</h4>
                        <div className="mt-2 flex justify-between text-sm text-gray-600">
                          <span>Teacher</span>
                          <span>Active</span>
                        </div>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8">
                <p className="text-gray-500">No classrooms found. Create a classroom to get started.</p>
                <Link 
                  href="/join-class" 
                  className="inline-block mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
                >
                  Create a Classroom
                </Link>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="bg-gray-800 text-white py-4 text-center">
        <p>© {new Date().getFullYear()} CodeProfesseur - All rights reserved</p>
      </footer>
    </div>
  );
}

export default Classrooms;