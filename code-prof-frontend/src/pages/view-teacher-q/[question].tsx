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
    
    const user = usercontext ? usercontext.user : undefined;
    const email = user ? user.email : "";

    const { classroom } = router.query;

    console.log("Classroom: ", classroom);

    const classroomData = classroom ? JSON.parse(classroom as string) : null;
    const classroomContext = classcontext ? classcontext.classroom : undefined;

    const { question } = router.query;

    console.log("Question: ", question);

    const questionData = question ? question : null;


    const classId = classroomContext ? classroomContext.class_id : undefined;

    const [questionId, setQuestionId] = useState([]);

    const setClassroom = classcontext ? classcontext.setClassroom : undefined;

    {/*useEffect(() => {
        if (setClassroom && classId) {
            setClassroom({ class_id: Number(classId), class_questions: [] });
        }
    }, [setClassroom, classId]);*/}

    {/*useEffect(() => {
        fetch("http://localhost:8080/api/classroom_id", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ classroomData })
        })
            .then(response => response.json())
            .then((data) => {
                setClassId(data);
            });
    }, [classroomData]);*/}

    console.log("Class Id is: ", classId);

    const [submissions, setSubmissions] = useState<Submission[]>([]);

    useEffect(() => {
        if (!question) {
            console.log("Question not present");
            return;
        }

        fetch(`http://localhost:8080/api/question/${questionData}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                setQuestionId(data['question_id']);
            })
            .catch(error => {
                console.error("Error fetching questionId:", error);
            })
    })

    console.log("Question Id Received: ", questionId);

    useEffect(() => {

        if (!questionId) {
            console.log("Question not present");
            return;
        }
        

        fetch(`http://localhost:8080/api/submission/results/${questionId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                setSubmissions(data);
            })
            .catch(error => {
                console.error("Error fetching questions:", error);
            });
    });

    const [selectedQuestion, setSelectedQuestion] = useState([]);

    const handleSubmit = (question : any) => {
      console.log("question ", question);
      console.log("classroom to send: ", classroom)
      router.push({
        pathname: `/student-question/${question}`,
        query: { question: JSON.stringify(question),
                classroom: JSON.stringify(classroom)
            }
      });
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
                            </tr>
                        </thead>
                        <tbody>
                            {submissions.map((submission, index) => (
                                <tr key={index} className={index % 2 === 0 ? "bg-black" : "bg-gray"}>
                                    <td className="border border-gray-400 px-4 py-2 text-center cursor-pointer hover:bg-blue-700" onClick={() => { handleSubmit(submission.first_name)}}>{submission.first_name} {submission.last_name}</td>
                                    <td className="border border-gray-400 px-4 py-2 text-center">{submission.is_accepted === 0 ? "Failed tests" : "Passed all tests"}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p>No submission made.</p>
                )}
            </main>
        </div>
    );
}

export default ViewAllSubmissions;