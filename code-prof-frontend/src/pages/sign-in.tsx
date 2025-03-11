import { useState } from "react";
import Link from "next/link";
import "../styles/globals.css";

export default function SignIn() {
    const [email, setEmail] = useState("");
    const [id, setId] = useState("");

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        console.log("Email:", email);
        console.log("ID:", id);
    }

    return (
        <div className="flex flex-col items-center justify-center min-h-screen py-2">
            <h1 className="text-2xl font-bold mb-4">Sign In</h1>
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                <label htmlFor="username" className="flex flex-col">
                    Email Address:
                    <input 
                        type="text" 
                        id="username" 
                        value={email} 
                        onChange={(e)=>setEmail(e.target.value)} 
                        className="border border-gray-3" 
                        required
                    />
                </label>
                <label htmlFor="ID" className="flex flex-col">
                    ID:
                    <input
                        type="text"
                        id="ID"
                        value={id}
                        onChange={(e)=>setId(e.target.value)}
                        className="border border-gray-3"
                        required
                    />
                </label>
                <Link href="student-home">
                <button
                    type="submit"
                    className="bg-blue-500 text-white y-2 px-4 rounded-full hover:bg-yellow-700 transition duration-300">
                    Sign In            
                </button>
                </Link>
            </form>
        </div>
    )
}
