/* Utility functions */
window.Utils = {
    formatNumber: function(num) {
        return new Intl.NumberFormat().format(num);
    },
    
    formatDate: function(date) {
        return new Date(date).toLocaleDateString();
    },
    
    formatTime: function(date) {
        return new Date(date).toLocaleTimeString();
    },
    
    formatDateTime: function(date) {
        return new Date(date).toLocaleString();
    },
    
    formatFileSize: function(bytes) {
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        if (bytes === 0) return '0 Bytes';
        const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
        return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
    },
    
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};