import React, { useState, useEffect, useContext } from 'react';
import { useRouter } from "next/router";
import { userContext, classContext } from '../context';
import "../styles/globals.css";

interface Student {
    first_name: string;
    last_name?: number;
    user_id?: number;
}

function SelectedClassroom() {
    const router = useRouter();
    const usercontext = useContext(userContext);
    const classcontext = useContext(classContext);
    
    const user = usercontext ? usercontext.user : undefined;
    const email = user ? user.email : "";

    const class_id = classcontext && classcontext.classroom ? classcontext.classroom.class_id : "";

    const { classroom } = router.query;

    console.log("Classroom Name is : ", classroom);

    const classroomData = classroom ? JSON.parse(classroom as string) : null;

    console.log("Classroom Data is : ", classroomData);

    const classroomContext = classcontext ? classcontext.classroom : undefined;

    const [classId, setClassId] = useState<number>();
    const setClassroom = classcontext ? classcontext.setClassroom : undefined;

    console.log("Class Id in context here is : ", class_id);

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

    console.log("Class Id is: ", classId);

    const [students, setStudents] = useState<Student[]>([]);

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

        fetch(`http://localhost:8080/api/classroom/${classId}/students`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                setStudents(data);
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
        pathname: `/classroom/${classId}`,
        query: { question: JSON.stringify(question),
                classroom: JSON.stringify(classroom)
            }
      });
    }

    return (
        <div id="main" className="flex flex-col min-h-screen">
            <header className="w-full bg-gray-800 text-white py-4">
                <h1 className="text-center text-xl">Students</h1>
            </header>
            <main className="flex flex-col items-center justify-center flex-grow py-4">
                {students.length > 0 ? (
                    <table className="table-auto border-collapse border border-gray-400 w-full max-w-4xl">
                        <thead>
                            <tr className="bg-black-200">
                                <th className="border border-gray-400 px-4 py-2 text-center">Name</th>
                                <th className="border border-gray-400 px-4 py-2 text-center">Email</th>
                            </tr>
                        </thead>
                        <tbody>
                            {students.map((student, index) => (
                                <tr key={index} className={index % 2 === 0 ? "bg-black" : "bg-gray"}>
                                    <td className="border border-gray-400 px-4 py-2 text-center cursor-pointer hover:bg-blue-700" onClick={() => { handleSubmit(student.user_id)}}>{student.first_name} {student.last_name}</td>
                                    <td className="border border-gray-400 px-4 py-2 text-center">{student.user_id ?? "N/A"}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p>No students in the class.</p>
                )}
            </main>
        </div>
    );
}

export default SelectedClassroom;