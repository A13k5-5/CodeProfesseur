import { useState, useContext } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import "../styles/globals.css";
import { userContext } from "../context";

export default function SignIn() {
    const userCtx = useContext(userContext);
    if (!userCtx) {
        throw new Error("userContext must be used within a UserProvider");
    }
    const { setUser } = userCtx;
    const [localEmail, setLocalEmail] = useState("");
    const [localId, setLocalId] = useState("");
    const router = useRouter();

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        setUser({ email: localEmail, id: localId });
        router.push("/student-home");
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen py-2">
            <h1 className="text-2xl font-bold mb-4">Sign In</h1>
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                <label htmlFor="username" className="flex flex-col">
                    Email Address:
                    <input 
                        type="text" 
                        id="username" 
                        value={localEmail} 
                        onChange={(e)=>setLocalEmail(e.target.value)} 
                        className="border border-gray-3" 
                        required
                    />
                </label>
                <label htmlFor="ID" className="flex flex-col">
                    ID:
                    <input
                        type="text"
                        id="ID"
                        value={localId}
                        onChange={(e)=>setLocalId(e.target.value)}
                        className="border border-gray-3"
                        required
                    />
                </label>
                <button type="submit" className="bg-blue-500 text-white py-2 px-4 rounded-full hover:bg-yellow-700 transition duration-300">
                    Sign In
                </button>
            </form>
        </div>
    )
}
