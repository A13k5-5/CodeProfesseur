import React, { useState, useEffect, useContext } from 'react';
import { useRouter } from "next/router";
import { userContext, classContext } from '../context';
import Link from "next/link";
import "../styles/globals.css";

interface Question {
    name: string;
    success_rate?: number;
    submission_count?: number;
    due_date?: string;
}

function SelectedClassroom() {
    const router = useRouter();
    const usercontext = useContext(userContext);
    const classcontext = useContext(classContext);
    
    const user = usercontext ? usercontext.user : undefined;
    const email = user ? user.email : "";
    const role = user ? user.type : "";

    const { classroom } = router.query;
    const classroomData = classroom ? JSON.parse(classroom as string) : null;
    const classroomContext = classcontext ? classcontext.classroom : undefined;

    const class_id = classroomContext ? classroomContext.class_id : "";

    console.log("Class Id in teacher-class-qs: ", class_id);
    console.log("Classroom Data received: ", classroomData);

    const [classId, setClassId] = useState<number>();
    const setClassroom = classcontext ? classcontext.setClassroom : undefined;
    const [loading, setLoading] = useState(true);
    const [showLogout, setShowLogout] = useState(false);

    useEffect(() => {
        if (!class_id){
            fetch("http://localhost:8080/api/classroom_id", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ classroom: classroomData })
            })
                .then(response => response.json())
                .then((data) => {
                    setClassId(data);
                })
                .catch(error => {
                    console.error("Error fetching class ID:", error);
                });
        }
        else if (class_id) {
            setClassId(class_id);
        }
    }, [class_id, classroomData]);

    console.log(classId);

    useEffect(() => {
        if (setClassroom && classId) {
            setClassroom({ class_id: Number(classId), class_questions: [] });
        }
    }, [setClassroom, classId]);
    
    const [questions, setQuestions] = useState<Question[]>([]);

    useEffect(() => {
        if (!classId || !email) {
            if (!classId) {
                console.log("ClassId not present");
            }
            if (!email) {
                console.log("Email not present");
            }
            return;
        }

        setLoading(true);
        fetch(`http://localhost:8080/api/classroom/${classId}/questions`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                setQuestions(data);
                setLoading(false);
            })
            .catch(error => {
                console.error("Error fetching questions:", error);
                setLoading(false);
            });
    }, [classId, email]);

    const handleSubmit = (question : any) => {
      console.log("question ", question);
      console.log("classroom to send: ", classroom);
      router.push({
        pathname: `/view-teacher-q/${question}`,
        query: { 
          question: JSON.stringify(question),
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
                    <Link 
                        href={{ pathname: "/create-question", query: { classroom } }}
                        className="text-center text-xl font-semibold hover:text-blue-300 transition-colors"
                    >
                        Create a Question
                    </Link>
                </div>
            </header>

            <main className="container mx-auto py-8 px-4 flex-grow">
                <div className="mb-8">
                    <h2 className="text-3xl font-bold mb-6 text-gray-800 border-b-2 border-blue-500 pb-2">Classroom Questions</h2>
                    <p className="text-gray-600 text-lg mb-6">View and manage questions for your class.</p>
                </div>

                {loading ? (
                    <div className="flex justify-center items-center h-64">
                        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
                    </div>
                ) : (
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        {questions.length > 0 ? (
                            <table className="table-auto border-collapse border border-gray-300 w-full">
                                <thead>
                                    <tr className="bg-gray-100">
                                        <th className="border border-gray-300 px-4 py-2 text-left font-semibold text-gray-700">Name</th>
                                        <th className="border border-gray-300 px-4 py-2 text-center font-semibold text-gray-700">Submission Count</th>
                                        <th className="border border-gray-300 px-4 py-2 text-center font-semibold text-gray-700">Due Date</th>
                                        <th className="border border-gray-300 px-4 py-2 text-center font-semibold text-gray-700">Success Rate</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {questions.map((question, index) => (
                                        <tr key={index} className={index % 2 === 0 ? "bg-white" : "bg-gray-50"}>
                                            <td 
                                                className="border border-gray-300 px-4 py-3 text-left font-medium text-blue-600 cursor-pointer hover:bg-blue-50 transition-colors" 
                                                onClick={() => handleSubmit(question.name)}
                                            >
                                                {question.name}
                                            </td>
                                            <td className="border border-gray-300 px-4 py-3 text-center text-gray-700">
                                                {question.submission_count ?? "N/A"}
                                            </td>
                                            <td className="border border-gray-300 px-4 py-3 text-center text-gray-700">
                                                {question.due_date ?? "N/A"}
                                            </td>
                                            <td className="border border-gray-300 px-4 py-3 text-center">
                                                {question.success_rate ? (
                                                    <div className="flex items-center justify-center">
                                                        <div className="w-full bg-gray-200 rounded-full h-2.5 mr-2 max-w-[100px]">
                                                            <div 
                                                                className={`h-2.5 rounded-full ${
                                                                    question.success_rate >= 70 ? 'bg-green-500' : 
                                                                    question.success_rate >= 40 ? 'bg-yellow-500' : 'bg-red-500'
                                                                }`}
                                                                style={{ width: `${question.success_rate}%` }}
                                                            ></div>
                                                        </div>
                                                        <span className="text-gray-700">{question.success_rate}%</span>
                                                    </div>
                                                ) : (
                                                    <span className="text-gray-500">N/A</span>
                                                )}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        ) : (
                            <div className="text-center py-8">
                                <p className="text-gray-500 mb-4">No questions available for this classroom.</p>
                                <Link 
                                    href={{ pathname: "/create-question", query: { classroom } }}
                                    className="inline-block px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors"
                                >
                                    Create Your First Question
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

export default SelectedClassroom;