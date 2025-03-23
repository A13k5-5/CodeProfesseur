import React, { useState, useEffect, useContext } from 'react';
import { useRouter } from "next/router";
import { userContext, classContext } from '../../context';
import "../../styles/globals.css";
import Link from "next/link";

interface Submissions {
    status: string;
    name: string;
    submission_path: string;
    is_accepted: any;
    date: string;
}

function Submission(){
    const router = useRouter();
    const usercontext = useContext(userContext);
    
    const user = usercontext ? usercontext.user : undefined;
    const email = user ? user.email : "";
       
    const { question } = router.query;
    const parsedQuestion = typeof question === "string" && question.startsWith("{") ? JSON.parse(question) : question;
    console.log("Question: ", parsedQuestion);

    const [submission, setSubmission] = useState<Submissions[]>([]);

    const [questionId, setQuestionId] = useState<number | null>(null);

    useEffect(() => {
        fetch(`http://localhost:8080/api/question/${parsedQuestion}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            setQuestionId(data.question_id); 
        })
        .catch(error => {
            console.error("Error fetching question ID:", error);
        });
    }, [parsedQuestion]); 

    console.log("Question Id is ", questionId);
    
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
        })
        .catch(error => {
            console.error("Error fetching submissions:", error);
        });
    }, [questionId, email]); 

    console.log("Submission Data: ", submission.map(sub => sub.submission_path))

    for (let sub of submission) {
        if (sub.is_accepted === 0) {
            sub.is_accepted = "Failed tests";
        }
        else {
            sub.is_accepted = "Passed all tests";
        }
    }

    console.log("Submission Status: ", submission.map(sub => sub.status));

    return(<div id="main" className="flex flex-col min-h-screen">
        <header className="w-full bg-gray-800 text-white py-4">
            <h1 className="text-center text-xl">{question}</h1>
        </header>
        <main className="flex flex-col items-center justify-center flex-grow py-4">
            {submission.length > 0 ? (
                <table className="table-auto border-collapse border border-gray-400 w-full max-w-4xl">
                    <thead>
                        <tr className="bg-black-200">
                            <th className="border border-gray-400 px-4 py-2 text-center">Name</th>
                            <th className="border border-gray-400 px-4 py-2 text-center">Accepted?</th>
                            <th className="border border-gray-400 px-4 py-2 text-center">Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {submission.map((submission, index) => (
                            <tr key={index} className={index % 2 === 0 ? "bg-black" : "bg-gray-350"}>
                                <td className="border border-gray-400 px-4 py-2 text-center" >{question} {index + 1}</td>
                                <td className="border border-gray-400 px-4 py-2 text-center">{submission.is_accepted ?? "N/A"}</td>
                                <td className="border border-gray-400 px-4 py-2 text-center">{submission.date ?? "N/A"}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            ) : (
                <div>
                <p>No submissions made.</p>
                </div>
            )}
            <Link className="bg-blue-500 text-white font-bold py-2 px-4 rounded hover:bg-yellow-500 transition duration-300 mt-20" href={`/add-submission/${question}/`}>
                Make a submission
            </Link>
        </main>
    </div>);

}

export default Submission;