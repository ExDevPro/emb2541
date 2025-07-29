/* API Helper functions */
window.API = {
    baseURL: '',
    
    // Generic request method
    request: function(method, endpoint, data = null) {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        return fetch(this.baseURL + endpoint, options)
            .then(response => response.json())
            .catch(error => {
                console.error('API Error:', error);
                return { success: false, error: error.message };
            });
    },
    
    // Dashboard API
    getDashboardStats: function() {
        return this.request('GET', '/api/dashboard/stats');
    },
    
    // Leads API
    getLeadLists: function() {
        return this.request('GET', '/api/leads/lists');
    },
    
    getLeadList: function(listName, page = 1, perPage = 100, search = '') {
        const params = new URLSearchParams({ page, per_page: perPage, search });
        return this.request('GET', `/api/leads/list/${listName}?${params}`);
    },
    
    importLeads: function(formData) {
        return fetch(this.baseURL + '/api/leads/import', {
            method: 'POST',
            body: formData
        }).then(response => response.json());
    },
    
    // SMTP API
    getSmtpServers: function() {
        return this.request('GET', '/api/smtp/servers');
    },
    
    saveSmtpServer: function(data) {
        return this.request('POST', '/api/smtp/server', data);
    },
    
    testSmtpServer: function(data) {
        return this.request('POST', '/api/smtp/test', data);
    },
    
    // Subjects API
    getSubjectLists: function() {
        return this.request('GET', '/api/subjects/lists');
    },
    
    // Templates API
    getTemplates: function() {
        return this.request('GET', '/api/templates');
    },
    
    // Campaigns API
    getCampaigns: function() {
        return this.request('GET', '/api/campaigns');
    },
    
    // Placeholders API
    getPlaceholders: function() {
        return this.request('GET', '/api/placeholders');
    },
    
    // Configuration API
    getConfig: function() {
        return this.request('GET', '/api/config');
    },
    
    saveConfig: function(data) {
        return this.request('POST', '/api/config', data);
    }
};