import React, { useState, useEffect, useContext } from 'react';
import { useRouter } from "next/router";
import { userContext, classContext } from '../context';
import "../styles/globals.css";
import Link from "next/link";

interface Question {
    name: string;
    content: string;
    input: string;
    output: string;
    difficulty: string;
    due_date: string;
}

function CreateQuestion(){
    const getUser = useContext(userContext);
    const email = getUser ? (getUser.user ? getUser.user.email : "") : "";
    const router = useRouter();
    const { question } = router.query;
    const { classroom } = router.query;

    const getClassroom = useContext(classContext);
    const class_interface = getClassroom ? getClassroom.classroom : undefined;
    const class_id = class_interface ? class_interface.class_id : undefined;

    console.log("Class Id is ", class_id);

    console.log("Classroom received in AddSubmission: ", classroom);

    const [newQuestion, setNewQuestion] = useState<Question>({
        name: "",
        content: "",
        input: "",
        output: "",
        difficulty: "",
        due_date: "",
    });

    const handleSubmit = ( () => {
        fetch (`http://localhost:8080/api/question/create`, {
            method: 'POST',
            headers: {
                "Content-Type" : "application/json"
            },
            body: JSON.stringify({
                name: newQuestion.name,
                content: newQuestion.content,
                input: newQuestion.input,
                output: newQuestion.output,
                difficulty: newQuestion.difficulty,
                due_date: newQuestion.due_date,
                classroom_ids: class_id
            })
        })
        .then(response => {
            if (!response.ok){
                throw new Error(`HTTP Error! Status: ${response.status}`);
            }
        })
        .then(data => {
            router.push({
                pathname: `/teacher-class-qs`,
                query: {classroom : classroom}
            });
        })
        .catch(error => {
            console.error("Error in posting submitted code ", error);
        });
    })

    
    
    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <h1 className="text-2xl font-bold mb-4 text-black">Create Question for: {classroom}</h1>
            <textarea
                value={newQuestion?.name || ""}
                onChange={(e) => setNewQuestion({ ...newQuestion, name: e.target.value } as Question)}
                rows={1}
                className="shadow appearance-none border rounded w-full max-w-2xl py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter the question name"
            ></textarea>
            <textarea
                value={newQuestion?.content || ""}
                onChange={(e) => setNewQuestion({ ...newQuestion, content: e.target.value } as Question)}
                rows={5}
                className="shadow appearance-none border rounded w-full max-w-2xl py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter the question"
            >
            </textarea>
            <textarea
                value={newQuestion?.input || ""}
                onChange={(e) => setNewQuestion({ ...newQuestion, input: e.target.value } as Question)}
                rows={10}
                className="shadow appearance-none border rounded w-full max-w-2xl py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter the test inputs"
            >
            </textarea>
            <textarea
                value={newQuestion?.output || ""}
                onChange={(e) => setNewQuestion({ ...newQuestion, output: e.target.value } as Question)}
                rows={10}
                className="shadow appearance-none border rounded w-full max-w-2xl py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter the expected outputs"
            >
            </textarea>
            <textarea
                value={newQuestion?.difficulty || ""}
                onChange={(e) => setNewQuestion({ ...newQuestion, difficulty: e.target.value} as Question)}
                rows={1}
                className="shadow appearance-none border rounded w-full max-w-2xl py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter the question difficulty"
            >
            </textarea>
            <textarea
                value={newQuestion?.due_date || ""}
                onChange={(e) => setNewQuestion({ ...newQuestion, due_date: e.target.value} as Question)}
                rows={1}
                className="shadow appearance-none border rounded w-full max-w-2xl py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter the due date"
            >
            </textarea>
            <button
                onClick={handleSubmit}
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-4"
            >
                Submit
            </button>
        </div>
    );
}

export default CreateQuestion;