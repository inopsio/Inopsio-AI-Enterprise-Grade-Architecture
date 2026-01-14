import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * The "cn" helper (Class Name)
 * ----------------------------
 * This is the standard utility for Inopsio AI Enterprise projects.
 * It merges Tailwind CSS classes and handles conditional logic.
 *
 * Why it's here:
 * 1. It uses 'clsx' to toggle classes (e.g., show red if error).
 * 2. It uses 'twMerge' to prevent Tailwind v4 class conflicts.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
