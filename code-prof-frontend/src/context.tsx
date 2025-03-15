"use client";

import React, { createContext, useState, ReactNode } from "react";

interface User {
    email: string;
    id: string;
}

interface UserContextType {
    user: User | null;
    setUser: (user: User) => void;
}

export const userContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);

    return (
        <userContext.Provider value={{ user, setUser }}>
            {children}
        </userContext.Provider>
    );
};