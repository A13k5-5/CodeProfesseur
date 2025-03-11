import Image from "next/image";
import Link from "next/link";
import "../styles/globals.css"

export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-center">
        <div className="flex flex-row gap-8 items-center sm:items-center">
          <Image
            className="dark:invert"
            src="/prof.png"
            alt="Code Professor"
            width={250}
            height={45}
            priority
          />
          <h1 className="code-prof text-center">
            Code Professeur
          </h1>
        </div>
        <p className="description text-center mt-4">
          THE Coding Education Platform
        </p>
        <div className="flex flex-row gap-16 items-center sm:items-center mt-8">
          <Link href="/sign-in">
            <button className="s-sign-in bg-white-500 text-white py-2 px-4 rounded-full border-2 border-yellow-700 hover:bg-yellow-700 transition duration-300">
              Student Sign In
            </button>
          </Link>
          <Link href="/sign-in">
            <button className="t-sign-in bg-white-500 text-white py-2 px-4 rounded-full border-2 border-yellow-700 hover:bg-yellow-700 transition duration-300">
              Teacher Sign In
            </button>
          </Link>
        </div>
      </main>
    </div>
  );
}
