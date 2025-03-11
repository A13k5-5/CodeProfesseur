import React from "react";
import Link from "next/link";
import "../styles/globals.css";

export default function StudentDashboard() {
  return (
    <div id="main" className="flex flex-col min-h-screen">
      <header className="w-full bg-gray-800 text-white py-4">
        <div className="flex flex-row container mx-auto px-4 space-x-4">
          <h2 className="text-center text-2xl font-bold">
            <Link href="/student-class">
              View Classrooms
            </Link>
          </h2>
          <h2 className="text-center text-2xl font-bold">
            <Link href="/join-class">
              Join a Classroom
            </Link>
          </h2>
        </div>
      </header>
      <main className="flex flex-row items-center justify-center flex-grow py-2">
        <p>Classroom</p>
      </main>
    </div>
  );
}