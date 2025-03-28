import React, { useState, useEffect, useContext, useMemo } from 'react';
import { useRouter } from "next/router";
import { userContext, classContext } from '../../context';
import "../../styles/globals.css";
import Link from "next/link";

interface Submission {
    status: string;
    first_name: string;
    last_name: string;
    content: string;
    submission_path: string;
    is_accepted: string;
    date: string;
    code: string;
}

function ViewAllSubmissions() {
    const router = useRouter();
    const usercontext = useContext(userContext);
    const classcontext = useContext(classContext);
    
    const user = usercontext ? usercontext.user : undefined;
    const email = user ? user.email : "";
    
    const { question, classroom } = router.query;
    
    const parsedQuestion = question;

    const [submissions, setSubmissions] = useState<Submission[]>([]);
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState(true);
    const [questionId, setQuestionId] = useState<number>();
    const [showLogout, setShowLogout] = useState(false);
    const [selectedCode, setSelectedCode] = useState<string | null>(null);
    const [selectedStudent, setSelectedStudent] = useState<string | null>(null);

    useEffect(() => {
        setLoading(true);
        const fetchQuestionId = async () => {
            try {
                const response = await fetch(`http://localhost:8080/api/question/${parsedQuestion}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();
                setQuestionId(data.question_id);
            } catch (error) {
                console.error("Error fetching question ID:", error);
                setError("Could not fetch current question");
                setLoading(false);
            }
        };

        if (parsedQuestion) {
            fetchQuestionId();
        }
    }, [parsedQuestion]);

    useEffect(() => {
        if (!parsedQuestion || !questionId) {
            return;
        }

        fetch(`http://localhost:8080/api/submission/results/${questionId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            setSubmissions(data);
            setLoading(false);
        })
        .catch(error => {
            console.error("Error fetching submissions:", error);
            setError(error.message);
            setLoading(false);
        });
    }, [parsedQuestion, questionId]);

    const handleSubmit = (submissionFirstName: string) => {
        router.push({
            pathname: `/student-question/${submissionFirstName}`,
            query: { 
                question: JSON.stringify(question),
                classroom: JSON.stringify(classroom)
            }
        });
    }

    const handleViewCode = (code: string, studentName: string) => {
        setSelectedCode(code);
        setSelectedStudent(studentName);
    }

    const handleCloseCode = () => {
        setSelectedCode(null);
        setSelectedStudent(null);
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
                        href={{ pathname: "/teacher-class-qs", query: { classroom } }}
                        className="text-center text-xl font-semibold hover:text-blue-300 transition-colors"
                    >
                        Back to Questions
                    </Link>
                </div>
            </header>

            <main className="container mx-auto py-8 px-4 flex-grow">
                <div className="mb-8">
                    <h2 className="text-3xl font-bold mb-6 text-gray-800 border-b-2 border-blue-500 pb-2">
                        Submissions for: {parsedQuestion}
                    </h2>
                    <p className="text-gray-600 text-lg mb-6">
                        View all student submissions for this question.
                    </p>
                </div>

                {loading ? (
                    <div className="flex justify-center items-center h-64">
                        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
                    </div>
                ) : error ? (
                    <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded">
                        <p className="font-bold">Error</p>
                        <p>{error}</p>
                    </div>
                ) : (
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        {submissions.length > 0 ? (
                            <div className="overflow-x-auto">
                                <table className="table-auto border-collapse border border-gray-300 w-full">
                                    <thead>
                                        <tr className="bg-gray-100">
                                            <th className="border border-gray-300 px-4 py-2 text-left font-semibold text-gray-700">Student Name</th>
                                            <th className="border border-gray-300 px-4 py-2 text-center font-semibold text-gray-700">Submission Date</th>
                                            <th className="border border-gray-300 px-4 py-2 text-center font-semibold text-gray-700">Status</th>
                                            <th className="border border-gray-300 px-4 py-2 text-center font-semibold text-gray-700">Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {submissions.map((submission, index) => (
                                            <tr key={index} className={index % 2 === 0 ? "bg-white" : "bg-gray-50"}>
                                                <td className="border border-gray-300 px-4 py-3 text-left font-medium text-gray-700">
                                                    {submission.first_name} {submission.last_name}
                                                </td>
                                                <td className="border border-gray-300 px-4 py-3 text-center text-gray-700">
                                                    {new Date(submission.date).toLocaleString()}
                                                </td>
                                                <td className="border border-gray-300 px-4 py-3 text-center text-gray-700">
                                                    {submission.is_accepted}
                                                </td>
                                                <td className="border border-gray-300 px-4 py-3 text-center text-gray-700">
                                                    <div className="flex justify-center space-x-2">
                                                        <button 
                                                            onClick={() => handleViewCode(submission.code, `${submission.first_name} ${submission.last_name}`)}
                                                            className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm transition-colors"
                                                        >
                                                            View Code
                                                        </button>
                                                        <button 
                                                            onClick={() => handleSubmit(submission.first_name)}
                                                            className="bg-purple-500 hover:bg-purple-600 text-white px-3 py-1 rounded text-sm transition-colors"
                                                        >
                                                            Details
                                                        </button>
                                                    </div>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        ) : (
                            <div className="text-center py-12">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                                <p className="text-gray-500 text-lg mb-4">No submissions have been made for this question yet.</p>
                                <p className="text-gray-400">Students will appear here once they submit their answers.</p>
                            </div>
                        )}
                    </div>
                )}

                {/* Code Viewer Modal */}
                {selectedCode && (
                    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                        <div className="bg-white rounded-lg shadow-xl max-w-6xl w-full mx-4 max-h-[90vh] flex flex-col">
                            <div className="flex justify-between items-center border-b border-gray-200 px-6 py-4">
                                <h3 className="text-xl font-bold text-gray-800">
                                    Code Submission from {selectedStudent}
                                </h3>
                                <button 
                                    onClick={handleCloseCode}
                                    className="text-black hover:text-gray-700"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                    </svg>
                                </button>
                            </div>
                            <div className="overflow-auto p-6 flex-grow">
                                <pre className="bg-gray-800 text-gray-100 p-4 rounded font-mono text-sm whitespace-pre-wrap">
                                    {selectedCode}
                                </pre>
                            </div>
                            <div className="border-t border-gray-200 px-6 py-4 flex justify-end">
                                <button 
                                    onClick={handleCloseCode}
                                    className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded"
                                >
                                    Close
                                </button>
                            </div>
                        </div>
                    </div>
                )}
            </main>

            <footer className="bg-gray-800 text-white py-4 text-center">
                <p>© {new Date().getFullYear()} CodeProfesseur - All rights reserved</p>
            </footer>
        </div>
    );
}

export default ViewAllSubmissions;