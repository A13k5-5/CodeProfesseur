import React, { useState, useEffect, useContext } from 'react';
import { useRouter } from "next/router";
import { userContext, classContext } from '../context';
import "../styles/globals.css";
import Link from "next/link";

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

    const { classroom } = router.query;
    const classroomData = classroom ? JSON.parse(classroom as string) : null;
    const classroomContext = classcontext ? classcontext.classroom : undefined;

    const [classId, setClassId] = useState<number>();
    const setClassroom = classcontext ? classcontext.setClassroom : undefined;
    const [loading, setLoading] = useState(true);
    const [showLogout, setShowLogout] = useState(false);

    useEffect(() => {
        if (setClassroom && classId) {
            setClassroom({ class_id: Number(classId), class_questions: [] });
        }
    }, [setClassroom, classId]);

    useEffect(() => {
        setLoading(true);
        fetch("http://localhost:8080/api/classroom_id", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ classroom })
        })
            .then(response => response.json())
            .then((data) => {
                setClassId(data);
            })
            .catch(error => {
                console.error("Error fetching classroom ID:", error);
            });
    }, [classroomData]);

    console.log("Class Id: ", classId);
    console.log("Email: ", email);

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

        fetch(`http://localhost:8080/api/classroom/${classId}/questions/${email}`)
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
      console.log("classroom to send: ", classroom)
      router.push({
        pathname: `/student-question/${question}`,
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
                        href="/student-class"
                        className="text-center text-xl font-semibold hover:text-blue-300 transition-colors"
                    >
                        Back to Classrooms
                    </Link>
                </div>
            </header>

            <main className="container mx-auto py-8 px-4 flex-grow">
                <div className="mb-8">
                    <h2 className="text-3xl font-bold mb-6 text-gray-800 border-b-2 border-blue-500 pb-2">
                        {classroomData && typeof classroomData === 'string' ? classroomData.replace(/[^\w\s-]/g, '').trim() : 'Classroom Questions'}
                    </h2>
                    <p className="text-gray-600 text-lg mb-6">View and work on questions assigned to you in this class.</p>
                </div>

                {loading ? (
                    <div className="flex justify-center items-center h-64">
                        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
                    </div>
                ) : (
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        {questions.length > 0 ? (
                            <div className="overflow-x-auto">
                                <table className="table-auto border-collapse border border-gray-300 w-full">
                                    <thead>
                                        <tr className="bg-gray-100">
                                            <th className="border border-gray-300 px-4 py-2 text-left font-semibold text-gray-700">Question Name</th>
                                            <th className="border border-gray-300 px-4 py-2 text-center font-semibold text-gray-700">Submissions</th>
                                            <th className="border border-gray-300 px-4 py-2 text-center font-semibold text-gray-700">Due Date</th>
                                            <th className="border border-gray-300 px-4 py-2 text-center font-semibold text-gray-700">Status</th>
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
                                                <td className="border border-gray-300 px-4 py-3 text-center">
                                                    {question.submission_count ? (
                                                        <span className="inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white bg-blue-500 rounded">
                                                            {question.submission_count}
                                                        </span>
                                                    ) : (
                                                        <span className="text-gray-500">No submissions</span>
                                                    )}
                                                </td>
                                                <td className="border border-gray-300 px-4 py-3 text-center text-gray-700">
                                                    {question.due_date ? (
                                                        <span className={`inline-block px-2 py-1 rounded text-xs font-medium ${
                                                            new Date(question.due_date) < new Date() ? 
                                                            'bg-red-100 text-red-800' : 
                                                            'bg-green-100 text-green-800'
                                                        }`}>
                                                            {question.due_date}
                                                        </span>
                                                    ) : (
                                                        <span className="text-gray-500">No due date</span>
                                                    )}
                                                </td>
                                                <td className="border border-gray-300 px-4 py-3 text-center">
                                                    {question.success_rate !== undefined ? (
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
                                                        <span className="text-gray-500">Not attempted</span>
                                                    )}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        ) : (
                            <div className="text-center py-12">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                                </svg>
                                <p className="text-gray-500 text-lg mb-4">No questions have been assigned to you in this class yet.</p>
                                <p className="text-gray-400">Check back later or contact your instructor.</p>
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