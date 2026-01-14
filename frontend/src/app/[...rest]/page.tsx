import Link from "next/link";

export default function NotFoundCatchAll() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-zinc-900 to-black text-white">
      {/* 404 Number */}
      <h1 className="text-[12rem] font-bold leading-none tracking-tighter bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">
        404
      </h1>

      {/* Message */}
      <h2 className="text-2xl font-semibold mt-4 text-zinc-300">
        Page Not Found
      </h2>
      <p className="text-zinc-500 mt-2 text-center max-w-md">
        The page you're looking for doesn't exist or has been moved.
      </p>

      {/* Back Home Button */}
      <Link
        href="/"
        className="mt-8 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors"
      >
        Go Back Home
      </Link>
    </div>
  );
}
