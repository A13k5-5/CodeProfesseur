import React, { useState, useEffect, useContext } from 'react';
import { useRouter } from "next/router";
import { userContext, classContext } from '../context';
import "../styles/globals.css";

interface Submission {
    status: string;
    name: string;
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
    const classroomData = classroom ? JSON.parse(classroom as string) : null;
    const classroomContext = classcontext ? classcontext.classroom : undefined;

    const { question } = router.query;
    const questionData = classroom ? JSON.parse(question as string) : null;

    const [classId, setClassId] = useState<number>();
    const setClassroom = classcontext ? classcontext.setClassroom : undefined;

    useEffect(() => {
        if (setClassroom && classId) {
            setClassroom({ class_id: Number(classId), class_questions: [] });
        }
    }, [setClassroom, classId]);

    useEffect(() => {
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
    }, [classroomData]);

    console.log(classId);

    const [submissions, setSubmissions] = useState<Submission[]>([]);

    useEffect(() => {
        if (!classId || !question) {
            if (!classId) {
                console.log("ClassId not present");
            }
            if (!question) {
                console.log("Question not present");
            }
            return;
        }

        fetch(`http://localhost:8080/api/classroom/${classId}/questions`)
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
    }, [classId, question]);

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
                                <th className="border border-gray-400 px-4 py-2 text-center">Name</th>
                                <th className="border border-gray-400 px-4 py-2 text-center">Submission Count</th>
                                <th className="border border-gray-400 px-4 py-2 text-center">Due Date</th>
                                <th className="border border-gray-400 px-4 py-2 text-center">Success Rate</th>
                            </tr>
                        </thead>
                        <tbody>
                            {submissions.map((submission, index) => (
                                <tr key={index} className={index % 2 === 0 ? "bg-black" : "bg-gray"}>
                                    <td className="border border-gray-400 px-4 py-2 text-center cursor-pointer hover:bg-blue-700" onClick={() => { handleSubmit(submission.name)}}>{submission.name}</td>
                                    <td className="border border-gray-400 px-4 py-2 text-center">{submission.name ?? "N/A"}</td>
                                    <td className="border border-gray-400 px-4 py-2 text-center">{submission.is_accepted ?? "N/A"}</td>
                                    <td className="border border-gray-400 px-4 py-2 text-center">{submission.date ?? "N/A"}</td>
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