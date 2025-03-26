import React, { useState, useEffect, useContext } from 'react';
import { useRouter } from "next/router";
import { userContext, classContext } from '../../context';
import "../../styles/globals.css";
import Link from "next/link";

function AddSubmission() {
    const getUser = useContext(userContext);
    const email = getUser ? (getUser.user ? getUser.user.email : "") : "";
    const router = useRouter();
    const { question } = router.query;

    const [code, setCode] = useState("");
    const [questionId, setQuestionId] = useState<number | null>(null);
    const [questionContent, setQuestionContent] = useState("");
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        console.log("Router is ready:", router.isReady);
        console.log("Question from query:", question);
    }, [router.isReady, question]);

    useEffect(() => {
        if (router.isReady && question && typeof question === 'string') {
            const fetchQuestionId = async () => {
                try {
                    setIsLoading(true);
                    const response = await fetch(`http://localhost:8080/api/question/${question}`);
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    setQuestionId(data.question_id);
                    
                    const contentResponse = await fetch(`http://localhost:8080/api/question/${data.question_id}`);
                    if (!contentResponse.ok) {
                        throw new Error(`HTTP error! Status: ${contentResponse.status}`);
                    }
                    
                    const contentData = await contentResponse.json();
                    setQuestionContent(contentData['content'] || '');
                } catch (err) {
                    console.error("Error fetching question details:", err);
                    setError(err instanceof Error ? err.message : "Failed to fetch question details");
                } finally {
                    setIsLoading(false);
                }
            };

            fetchQuestionId();
        } else if (router.isReady) {
            setError("Invalid question identifier");
            setIsLoading(false);
        }
    }, [router.isReady, question]);

    const handleSubmit = () => {
        if (!questionId) {
            setError("Question ID is not available");
            return;
        }

        fetch('http://localhost:8080/api/submission/add_student_submission', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user: email,
                question_id: questionId,
                question: question,
                text: code
            })
        })
        .then(response => {
            if (!response.ok){
                throw new Error(`HTTP Error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(() => {
            router.push({
                pathname: `/student-question/${question}`,
                query: {classroom : router.query.classroom}
            });
        })
        .catch(error => {
            console.error("Error in posting submitted code ", error);
            setError("Failed to submit code");
        });
    }
    
    if (isLoading || error) {
        return <div>Loading...</div>;
    }

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <h1 className="text-2xl font-bold mb-4 text-black">Add Submission for: {question}</h1>
            <p className="text-xl mb-4 text-black">{questionContent}</p>
            <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                rows={10}
                className="shadow appearance-none border rounded w-full max-w-2xl py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter your Python code here..."
            ></textarea>
            <button
                onClick={handleSubmit}
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-4"
            >
                Submit
            </button>
        </div>
    );
}

export default AddSubmission;