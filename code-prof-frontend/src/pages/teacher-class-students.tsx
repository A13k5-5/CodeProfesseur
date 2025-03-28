import React, { useState, useEffect, useContext, useMemo } from 'react';
import { useRouter } from "next/router";
import { userContext, classContext } from '../context';
import Link from "next/link";
import "../styles/globals.css";

interface Student {
    first_name: string;
    last_name?: string;
    user_id?: string;
    num_submissions: number;
}

function SelectedClassroom() {
    const router = useRouter();
    const usercontext = useContext(userContext);
    const classcontext = useContext(classContext);
    
    const user = usercontext ? usercontext.user : undefined;
    const email = user ? user.email : "";

    const { classroom } = router.query;

    console.log("Classroom Name is : ", classroom);

    const classroomData = useMemo(() => {
        return classroom ? JSON.parse(classroom as string) : null;
    }, [classroom]);

    console.log("Classroom Data is : ", classroomData);

    const classroomContext = classcontext ? classcontext.classroom : undefined;
    const class_id = classroomContext ? classroomContext.class_id : undefined;

    const [classId, setClassId] = useState<number>();
    const setClassroom = classcontext ? classcontext.setClassroom : undefined;

    const [students, setStudents] = useState<Student[]>([]);
    const [loading, setLoading] = useState(true);
    const [showLogout, setShowLogout] = useState(false);

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
            })
            .catch(error => {
                console.error("Error fetching classroom ID:", error);
            });
    }, [classroom, setClassroom]);

    console.log("Class Id in context: ", class_id);

    useEffect(() => {
        if (!class_id || !email) {
            if (!class_id) {
                console.log("ClassId not present");
            }
            if (!email) {
                console.log("Email not present");
            }
            return;
        }

        setLoading(true);
        fetch(`http://localhost:8080/api/classroom/${class_id}/students`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                setStudents(data);
                setLoading(false);
            })
            .catch(error => {
                console.error("Error fetching students:", error);
                setLoading(false);
            });
    }, [class_id, email]);

    const handleSubmit = (studentId: any) => {
        console.log("student ID: ", studentId);
        console.log("classroom to send: ", classroom);
        router.push({
            pathname: `/classroom/${class_id}`,
            query: {
                student: JSON.stringify(studentId),
                classroom: JSON.stringify(classroom)
            }
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
                    <Link
                        href={{ pathname: "/teacher-class-menu", query: { classroom } }}
                        className="text-center text-xl font-semibold hover:text-blue-300 transition-colors"
                    >
                        Back to Class Menu
                    </Link>
                </div>
            </header>

            <main className="container mx-auto py-8 px-4 flex-grow">
                <div className="mb-8">
                    <h2 className="text-3xl font-bold mb-6 text-gray-800 border-b-2 border-blue-500 pb-2">Students</h2>
                    <p className="text-gray-600 text-lg mb-6">View and monitor students enrolled in this class.</p>
                </div>

                {loading ? (
                    <div className="flex justify-center items-center h-64">
                        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
                    </div>
                ) : (
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        {students.length > 0 ? (
                            <div className="overflow-x-auto">
                                <table className="table-auto border-collapse border border-gray-300 w-full">
                                    <thead>
                                        <tr className="bg-gray-100">
                                            <th className="border border-gray-300 px-4 py-2 text-left font-semibold text-gray-700">Name</th>
                                            <th className="border border-gray-300 px-4 py-2 text-left font-semibold text-gray-700">Email</th>
                                            <th className="border border-gray-300 px-4 py-2 text-center font-semibold text-gray-700">Total Submissions</th>
                                            <th className="border border-gray-300 px-4 py-2 text-center font-semibold text-gray-700">Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {students.map((student, index) => (
                                            <tr key={index} className={index % 2 === 0 ? "bg-white" : "bg-gray-50"}>
                                                <td className="border border-gray-300 px-4 py-3 text-left font-medium text-gray-700">
                                                    {student.first_name} {student.last_name}
                                                </td>
                                                <td className="border border-gray-300 px-4 py-3 text-left text-gray-700">
                                                    {student.user_id ?? "N/A"}
                                                </td>
                                                <td className="border border-gray-300 px-4 py-3 text-center">
                                                    <div className="flex items-center justify-center space-x-1">
                                                        <span className="inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white bg-blue-500 rounded">
                                                            {student.num_submissions}
                                                        </span>
                                                        <span className="text-sm text-gray-500">submissions</span>
                                                    </div>
                                                </td>
                                                <td className="border border-gray-300 px-4 py-3 text-center">
                                                    <button 
                                                        onClick={() => handleSubmit(student.user_id)}
                                                        className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm transition-colors"
                                                    >
                                                        View Progress
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        ) : (
                            <div className="text-center py-8">
                                <p className="text-gray-500 mb-4">No students have joined this class yet.</p>
                                <div className="p-6 border border-dashed border-gray-300 rounded-lg max-w-lg mx-auto">
                                    <h3 className="text-lg font-semibold text-gray-700 mb-2">Share Class Code</h3>
                                    <p className="text-gray-600 mb-4">
                                        Students can join this class by using the class code or invitation link.
                                    </p>
                                    <div className="bg-gray-100 p-3 rounded-md text-center mb-3">
                                        <span className="font-mono text-lg">{classroomData}</span>
                                    </div>
                                </div>
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

export default SelectedClassroom;