"use client";

import React, { createContext, useState, ReactNode } from "react";

interface User {
    email: string;
    pwd: string;
}

interface Classroom {
    class_id: number,
    class_questions: [],
}

interface UserContextType {
    user: User | null;
    setUser: (user: User) => void;
}

interface ClassroomContextType {
    classroom: Classroom | null;
    setClassroom: (classroom: Classroom) => void;
}

export const userContext = createContext<UserContextType | undefined>(undefined);

export const classContext = createContext<ClassroomContextType | undefined>(undefined);

export const ClassProvider = ({ children }: { children: ReactNode }) => {
    const [classroom, setClassroom] = useState<Classroom | null>(null);

    return (
        <classContext.Provider value={{ classroom, setClassroom }}>
            {children}
        </classContext.Provider>
    )
}

export const UserProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);

    return (
        <userContext.Provider value={{ user, setUser }}>
            {children}
        </userContext.Provider>
    );
};

export const AppProvider = ({ children }: { children: ReactNode }) => {
    return (
        <UserProvider>
            <ClassProvider>
                {children}
            </ClassProvider>
        </UserProvider>
    )
}