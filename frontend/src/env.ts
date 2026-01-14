/**
 * Inopsio AI Enterprise - Environment Guard
 * Uses T3 Env + Zod to validate environment variables at build time.
 * If a required variable is missing, the app crashes immediately with a clear error.
 */
import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";

export const env = createEnv({
  /**
   * Server-side Environment Variables (Private)
   * These are only available in server components and API routes.
   */
  server: {
    NODE_ENV: z.enum(["development", "test", "production"]),
  },

  /**
   * Client-side Environment Variables (Public)
   * These connect your frontend to the backend API.
   * Must start with NEXT_PUBLIC_ to be exposed to the browser.
   */
  client: {
    NEXT_PUBLIC_APP_URL: z.string().url(),
    NEXT_PUBLIC_API_URL: z.string().url(),
  },

  /**
   * Runtime Environment Mapping
   * You must manually destructure them here for Next.js 16.1.
   */
  runtimeEnv: {
    NODE_ENV: process.env.NODE_ENV,
    NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },

  /**
   * Run `build` or `dev` with `SKIP_ENV_VALIDATION` to skip validation.
   * Useful for Docker builds where some vars are injected later.
   */
  skipValidation: !!process.env.SKIP_ENV_VALIDATION,
  emptyStringAsUndefined: true,
});
