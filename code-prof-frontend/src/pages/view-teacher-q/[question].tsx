import React, { useState, useEffect, useContext } from 'react';
import { useRouter } from "next/router";
import { userContext, classContext } from '../../context';
import "../../styles/globals.css";

interface Submission {
    status: string;
    first_name: string;
    last_name: string;
    content: string;
    submission_path: string;
    is_accepted: any;
    date: string;
    code: string;
}

function ViewAllSubmissions() {
    const router = useRouter();
    const usercontext = useContext(userContext);
    const classcontext = useContext(classContext);
    
    const { question, classroom } = router.query;

    const [submissions, setSubmissions] = useState<Submission[]>([]);
    const [error, setError] = useState<string | null>(null);

    const [questionId, setQuestionId] = useState<number>();

    useEffect(() => {
        const fetchQuestionId = async () => {
            try {
                const response = await fetch(`http://localhost:8080/api/question/${question}`, {
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
            }
        };

        fetchQuestionId();
    }, []);

    console.log("Question Id is: ", questionId);

    useEffect(() => {
        if (!question || !questionId) {
            return;
        }

        fetch(`http://localhost:8080/api/submission/results/${questionId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            console.log("Response status:", response.status);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Fetched submissions:", data);
            setSubmissions(data);
        })
        .catch(error => {
            console.error("Error fetching submissions:", error);
            setError(error.message);
        });
    }, [question, questionId]);

    const handleSubmit = (submissionFirstName: string) => {
        router.push({
            pathname: `/student-question/${submissionFirstName}`,
            query: { 
                question: JSON.stringify(question),
                classroom: JSON.stringify(classroom)
            }
        });
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div id="main" className="flex flex-col min-h-screen">
            <header className="w-full bg-gray-800 text-white py-4">
                <h1 className="text-center text-xl">Class Submissions</h1>
            </header>
            <main className="flex flex-col items-center justify-center flex-grow py-4">
                {submissions.length > 0 ? (
                    <table className="table-auto border-collapse border border-gray-400 w-full max-w-4xl">
                        <thead>
                            <tr className="bg-black-200">
                                <th className="border border-gray-400 px-4 py-2 text-center">Student Name</th>
                                <th className="border border-gray-400 px-4 py-2 text-center">Accepted?</th>
                                <th className="border border-gray-400 px-4 py-2 text-center">Code</th>
                            </tr>
                        </thead>
                        <tbody>
                            {submissions.map((submission, index) => (
                                <tr key={index} className={index % 2 === 0 ? "bg-black" : "bg-gray"}>
                                    <td 
                                        className="border border-gray-400 px-4 py-2 text-center cursor-pointer hover:bg-blue-700" 
                                        onClick={() => handleSubmit(submission.first_name)}
                                    >
                                        {submission.first_name} {submission.last_name} 
                                    </td>
                                    <td className="border border-gray-400 px-4 py-2 text-center">
                                        {submission.is_accepted == null
                                            ? "N/A"
                                            : submission.is_accepted === 0
                                            ? "Failed tests"
                                            : "Passed all tests"
                                        }
                                    </td>
                                    <td className="border border-gray-400 px-4 py-2 text-center cursor-pointer hover:bg-blue-700"
                                    >{submission.code}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p>No submissions made.</p>
                )}
            </main>
        </div>
    );
}

export default ViewAllSubmissions;