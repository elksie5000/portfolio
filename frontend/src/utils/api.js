// Helper to get the correct API base URL
// In production (Vercel), VITE_API_BASE_URL should be set in environment variables.
// In development, it defaults to localhost.

export const getApiBaseUrl = () => {
    // Check if we are in production mode (Vercel sets this automatically)
    if (import.meta.env.PROD) {
        // Use the environment variable if set, otherwise fallback to the hardcoded Render URL
        const url = import.meta.env.VITE_API_BASE_URL || 'https://api-elksie5000.onrender.com';
        console.log('Using Production API URL:', url);
        return url;
    }

    // In development, use the current hostname to support local mobile testing
    // (e.g., if accessing via 192.168.x.x, the backend should also be accessed there)
    // Note: Backend must be running with --host 0.0.0.0 for this to work
    const hostname = window.location.hostname;
    const url = `http://${hostname}:8000`;
    console.log('Using Development API URL:', url);
    return url;
};
