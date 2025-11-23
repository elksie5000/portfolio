// Helper to get the correct API base URL
// In production (Vercel), VITE_API_BASE_URL should be set in environment variables.
// In development, it defaults to localhost.

export const getApiBaseUrl = () => {
    // Check if we are in production mode (Vercel sets this automatically)
    if (import.meta.env.PROD) {
        // Use the environment variable if set, otherwise fallback to the hardcoded Render URL
        // This ensures that even if the Vercel env var is missing, it will still point to the live backend.
        return import.meta.env.VITE_API_BASE_URL || 'https://api-elksie5000.onrender.com';
    }
    // Default to local development server
    return 'http://127.0.0.1:8000';
};
