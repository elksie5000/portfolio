// Helper to get the correct API base URL
// In production (Vercel), VITE_API_BASE_URL should be set in environment variables.
// In development, it defaults to localhost.

export const getApiBaseUrl = () => {
    if (import.meta.env.PROD) {
        return import.meta.env.VITE_API_BASE_URL || 'https://api-elksie5000.onrender.com';
    }
    return 'http://127.0.0.1:8000';
};
