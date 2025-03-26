import React, { useState, useEffect, useContext } from 'react';
import { useRouter } from "next/router";
import { userContext, classContext } from '../../context';
import "../../styles/globals.css";
import Link from "next/link";

function AddSubmission(){
    const getUser = useContext(userContext);
    const email = getUser ? (getUser.user ? getUser.user.email : "") : "";
    const router = useRouter();
    const { question } = router.query;
    const { classroom } = router.query;

    console.log("Classroom received in AddSubmission: ", classroom);

    const [code, setCode] = useState("");

    const [questionId, setQuestionId] = useState<number | null>(null);
    
    useEffect(() => {
        fetch(`http://localhost:8080/api/question/${question}`)
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
    }); 

    const [questionContent, setQuestionContent] = useState([]);
    
    useEffect(() => {
        fetch(`http://localhost:8080/api/question/${questionId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            setQuestionContent(data['content']); 
        })
        .catch(error => {
            console.error("Error fetching question ID:", error);
        });
    }, [questionId]); 

    console.log("Content is: ", questionContent);

    const handleSubmit = () => {
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
            })
            .then(data => {
                router.push({
                    pathname: `/student-question/${question}`,
                    query: {classroom : JSON.stringify(classroom)}
                });
            })
            .catch(error => {
                console.error("Error in posting submitted code ", error);
            });
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