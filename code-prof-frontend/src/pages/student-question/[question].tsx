import React, { useState, useEffect, useContext, useMemo } from 'react';
import { useRouter } from "next/router";
import { userContext, classContext } from '../../context';
import "../../styles/globals.css";
import Link from "next/link";

interface Submissions {
    status: string;
    name: string;
    content: string;
    submission_path: string;
    is_accepted: string;
    date: string;
    code: string;
}

function Submission(){
    const router = useRouter();
    const usercontext = useContext(userContext);
    
    const user = usercontext ? usercontext.user : undefined;
    const email = user ? user.email : "";
       
    const { question, classroom } = router.query;
    
    // Safely parse query parameters
    const parsedQuestion = useMemo(() => {
        if (!question) return null;
        try {
            return typeof question === "string" && question.startsWith("{") ? 
                JSON.parse(question) : question;
        } catch (error) {
            return question;
        }
    }, [question]);
    
    const parsedClassroom = useMemo(() => {
        if (!classroom) return null;
        try {
            return JSON.parse(classroom as string);
        } catch (error) {
            return classroom;
        }
    }, [classroom]);
    
    const [submission, setSubmission] = useState<Submissions[]>([]);
    const [questionId, setQuestionId] = useState<number | null>(null);
    const [questionDetails, setQuestionDetails] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [showLogout, setShowLogout] = useState(false);
    const [viewCode, setViewCode] = useState<string | null>(null);

    useEffect(() => {
        if (!parsedQuestion) return;
        
        setLoading(true);
        fetch(`http://localhost:8080/api/question/${parsedQuestion}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            setQuestionId(data.question_id);
            setQuestionDetails(data);
        })
        .catch(error => {
            console.error("Error fetching question ID:", error);
        });
    }, [parsedQuestion]); 
    
    useEffect(() => {
        if (!questionId || !email) return;
        
        fetch(`http://localhost:8080/api/question/${questionId}/${email}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const submissionData = Array.isArray(data) ? data : [data];
            setSubmission(submissionData);
            setLoading(false);
        })
        .catch(error => {
            console.error("Error fetching submissions:", error);
            setLoading(false);
        });
    }, [questionId, email]);

    const handleLogOut = () => {
        window.location.href = "/sign-in";
    }

    const handleViewCode = (code: string) => {
        setViewCode(code);
    }

    const handleCloseCode = () => {
        setViewCode(null);
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
                        href={{
                            pathname: '/classroom',
                            query: { classroom: JSON.stringify(parsedClassroom)}
                        }}
                        className="text-center text-xl font-semibold hover:text-blue-300 transition-colors"
                    >
                        Back to Classroom
                    </Link>
                </div>
            </header>

            <main className="container mx-auto py-8 px-4 flex-grow">
                <div className="mb-8">
                    <h2 className="text-3xl font-bold mb-6 text-gray-800 border-b-2 border-blue-500 pb-2">
                        Question: {parsedQuestion}
                    </h2>
                    
                    {questionDetails && questionDetails.description && (
                        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
                            <h3 className="text-xl font-semibold mb-4 text-gray-700">Problem Description</h3>
                            <p className="text-gray-600 whitespace-pre-line">
                                {questionDetails.description}
                            </p>
                        </div>
                    )}
                    
                    <p className="text-gray-600 text-lg mb-6">
                        View your submissions for this question and make new ones.
                    </p>
                </div>

                {loading ? (
                    <div className="flex justify-center items-center h-64">
                        <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
                    </div>
                ) : (
                    <div className="bg-white rounded-lg shadow-lg p-6">
                        <h3 className="text-xl font-bold mb-4 text-gray-700 flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                            </svg>
                            Your Submissions
                        </h3>
                        
                        {submission.length > 0 ? (
                            <div className="overflow-x-auto">
                                <table className="table-auto border-collapse border border-gray-300 w-full">
                                    <thead>
                                        <tr className="bg-gray-100">
                                            <th className="border border-gray-300 px-4 py-2 text-left font-semibold text-gray-700">Submission</th>
                                            <th className="border border-gray-300 px-4 py-2 text-center font-semibold text-gray-700">Status</th>
                                            <th className="border border-gray-300 px-4 py-2 text-center font-semibold text-gray-700">Date</th>
                                            <th className="border border-gray-300 px-4 py-2 text-center font-semibold text-gray-700">Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {submission.map((item, index) => (
                                            <tr key={index} className={index % 2 === 0 ? "bg-white" : "bg-gray-50"}>
                                                <td className="border border-gray-300 px-4 py-3 text-left font-medium text-gray-700">
                                                    Attempt {index + 1}
                                                </td>
                                                <td className="border border-gray-300 px-4 py-3 text-center text-black">
                                                    {item.is_accepted}
                                                </td>
                                                <td className="border border-gray-300 px-4 py-3 text-center text-gray-700">
                                                    {new Date(item.date).toLocaleString()}
                                                </td>
                                                <td className="border border-gray-300 px-4 py-3 text-center">
                                                    <button 
                                                        onClick={() => handleViewCode(item.code)}
                                                        className="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm transition-colors"
                                                    >
                                                        View Code
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        ) : (
                            <div className="text-center py-8">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-gray-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                </svg>
                                <p className="text-gray-500 text-lg mb-4">You haven't made any submissions yet.</p>
                                <p className="text-gray-400 mb-8">Submit your solution to see your progress here.</p>
                            </div>
                        )}
                        
                        <div className="flex justify-center mt-8">
                            <Link 
                                href={{
                                    pathname: `/add-submission/${parsedQuestion}`,
                                    query: { classroom: JSON.stringify(parsedClassroom)}
                                }}
                                className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-6 rounded-lg shadow-md transition duration-300 flex items-center"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                                </svg>
                                Make a New Submission
                            </Link>
                        </div>
                    </div>
                )}
            </main>

            {/* Code Viewer Modal */}
            {viewCode && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-lg shadow-xl max-w-6xl w-full mx-4 max-h-[90vh] flex flex-col">
                        <div className="flex justify-between items-center border-b border-gray-200 px-6 py-4">
                            <h3 className="text-xl font-bold text-gray-800">
                                Your Code Submission
                            </h3>
                            <button 
                                onClick={handleCloseCode}
                                className="text-gray-500 hover:text-gray-700"
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                        </div>
                        <div className="overflow-auto p-6 flex-grow">
                            <pre className="bg-gray-800 text-gray-100 p-4 rounded font-mono text-sm whitespace-pre-wrap">
                                {viewCode}
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

            <footer className="bg-gray-800 text-white py-4 text-center">
                <p>© {new Date().getFullYear()} CodeProfesseur - All rights reserved</p>
            </footer>
        </div>
    );
}

export default Submission;