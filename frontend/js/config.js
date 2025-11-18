// API Configuration
const API_CONFIG = {
    // Change this to switch between development and production
    environment: 'development', // 'development' or 'production'
    
    endpoints: {
        development: 'http://localhost:3000',
        production: 'https://webinar-75c9.onrender.com'
    },
    
    // Get the current API base URL
    getBaseURL() {
        return this.endpoints[this.environment];
    },
    
    // Get full endpoint URL
    getEndpoint(path) {
        return `${this.getBaseURL()}${path}`;
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API_CONFIG;
}
