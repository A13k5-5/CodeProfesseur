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

    interface UserData {
      question_count?: number;
      submission_count?: number;
      recent_activity?: { description: string; date: string }[];
      [key: string]: any;
    }

    const [userData, setUserData] = useState<UserData[]>([]);
    const [classrooms, setClassrooms] = useState([]);
    const [questions, setQuestions] = useState([]);
    const [loading, setLoading] = useState(true);
        
    useEffect(() => {
      // Get user data
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
        })
        .catch(error => {
          console.error("Error fetching user data:", error);
        });
        
      // Get classrooms
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
    }, [email, pwd, role]);

    const [showLogout, setShowLogout] = useState(false); 

    const handleLogOut = () => {
      window.location.href = "/sign-in";
    }

    interface Classroom {
      class_name?: string;
      [key: string]: any;
    }

    const handleClassClick = (classroom: Classroom): void => {
      const router = useRouter();
      router.push({
      pathname: role === 1 ? `/teacher-class-menu` : `/classroom`,
      query: { classroom: JSON.stringify(classroom) }
      });
    }

    return (
      <div id="main" className="flex flex-col min-h-screen bg-gray-100">
        <header className="w-full bg-gray-800 text-white py-4 shadow-md">
          <div className="container mx-auto px-4 flex justify-between items-center">
            <h1 className="text-2xl font-bold">Code Professor</h1>
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
            <Link 
              href={role === 1 ? "/teacher-class" : "/student-class"} 
              className="text-center text-xl font-semibold hover:text-blue-300 transition-colors"
            >
              View Classrooms
            </Link>
            <Link 
              href="/join-class" 
              className="text-center text-xl font-semibold hover:text-blue-300 transition-colors"
            >
              {role === 1 ? "Create a Classroom" : "Join a Classroom"}
            </Link>
          </div>
        </header>

        <main className="container mx-auto py-8 px-4 flex-grow">
          <div className="mb-8">
            <h2 className="text-3xl font-bold mb-6 text-gray-800 border-b-2 border-blue-500 pb-2">Dashboard</h2>
            <p className="text-gray-600 text-lg mb-6">Welcome back! Here's an overview of your classes and recent activities.</p>
          </div>

          {loading ? (
            <div className="flex justify-center items-center h-64">
              <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Classrooms Section */}
              <div className="md:col-span-2">
                <div className="bg-white rounded-lg shadow-lg p-6 h-full">
                  <h3 className="text-xl font-bold mb-4 text-gray-700 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                    </svg>
                    Your Classes
                  </h3>
                  
                  {classrooms.length > 0 ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      {classrooms.map((classroom: Classroom, index) => (
                        <div 
                          key={index}
                          className="border border-gray-200 rounded-lg p-4 hover:bg-blue-50 transition-colors cursor-pointer shadow-sm"
                          onClick={() => handleClassClick(classroom.class_name || Object.values(classroom)[0])}
                        >
                          <h4 className="font-semibold text-lg text-gray-800">
                            {classroom.class_name || Object.values(classroom)[0]}
                          </h4>
                          <div className="mt-2 flex justify-between text-sm text-gray-600">
                            <span>{role === 1 ? "Teacher" : "Student"}</span>
                            <span>Active</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <p className="text-gray-500">No classes found. Join a class to get started!</p>
                      <Link 
                        href="/join-class" 
                        className="inline-block mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
                      >
                        {role === 1 ? "Create a Class" : "Join a Class"}
                      </Link>
                    </div>
                  )}
                </div>
              </div>

              {/* Stats Section */}
              <div>
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h3 className="text-xl font-bold mb-4 text-gray-700 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                    Your Stats
                  </h3>
                  <div className="space-y-4">
                    <div className="bg-blue-50 p-4 rounded-md">
                      <div className="text-sm text-gray-600">Total Classes</div>
                      <div className="text-2xl font-bold text-blue-600">{classrooms.length}</div>
                    </div>
                    <div className="bg-green-50 p-4 rounded-md">
                      <div className="text-sm text-gray-600">Questions Assigned</div>
                      <div className="text-2xl font-bold text-green-600">{userData[0]?.question_count || 0}</div>
                    </div>
                    <div className="bg-purple-50 p-4 rounded-md">
                      <div className="text-sm text-gray-600">Submissions</div>
                      <div className="text-2xl font-bold text-purple-600">{userData[0]?.submission_count || 0}</div>
                    </div>
                  </div>
                </div>

                {/* Recent Activity */}
                <div className="bg-white rounded-lg shadow-lg p-6 mt-6">
                  <h3 className="text-xl font-bold mb-4 text-gray-700 flex items-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Recent Activity
                  </h3>
                  <div className="space-y-3">
                    {userData[0]?.recent_activity ? (
                      userData[0].recent_activity.map((activity, index) => (
                        <div key={index} className="border-b border-gray-100 pb-2">
                          <p className="text-sm text-gray-600">{activity.description}</p>
                          <p className="text-xs text-gray-400">{activity.date}</p>
                        </div>
                      ))
                    ) : (
                      <p className="text-gray-500 text-sm">No recent activity</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}
        </main>

        <footer className="bg-gray-800 text-white py-4 text-center">
          <p>© {new Date().getFullYear()} Code Professor - All rights reserved</p>
        </footer>
      </div>
    );
  }

export default StudentHome;