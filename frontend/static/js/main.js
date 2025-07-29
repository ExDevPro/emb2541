/*
DeepMailer v1.0 - Main JavaScript
Professional Email Marketing Software
*/

// Global application state
window.DeepMailer = {
    config: {},
    socket: null,
    currentModule: 'dashboard',
    isConnected: false,
    stats: {},
    modules: {},
    
    // Initialize application
    init: function() {
        console.log('Initializing DeepMailer v1.0...');
        
        // Initialize socket connection
        this.initSocket();
        
        // Setup navigation
        this.setupNavigation();
        
        // Setup global event handlers
        this.setupEventHandlers();
        
        // Load initial data
        this.loadInitialData();
        
        // Hide loading screen
        setTimeout(() => {
            this.hideLoadingScreen();
        }, 1500);
        
        console.log('DeepMailer v1.0 initialized successfully');
    },
    
    // Initialize Socket.IO connection
    initSocket: function() {
        try {
            this.socket = io();
            
            this.socket.on('connect', () => {
                console.log('Connected to DeepMailer server');
                this.isConnected = true;
                this.updateConnectionStatus(true);
            });
            
            this.socket.on('disconnect', () => {
                console.log('Disconnected from DeepMailer server');
                this.isConnected = false;
                this.updateConnectionStatus(false);
            });
            
            this.socket.on('dashboard_stats_update', (data) => {
                this.updateDashboardStats(data);
            });
            
            this.socket.on('error', (error) => {
                console.error('Socket error:', error);
                this.showNotification('Connection Error: ' + error.message, 'danger');
            });
            
        } catch (error) {
            console.error('Failed to initialize socket connection:', error);
        }
    },
    
    // Setup navigation handlers
    setupNavigation: function() {
        const navItems = document.querySelectorAll('.nav-item');
        
        navItems.forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                
                const module = item.getAttribute('data-module');
                this.switchModule(module);
            });
        });
    },
    
    // Setup global event handlers
    setupEventHandlers: function() {
        // Refresh button
        document.getElementById('refresh-btn')?.addEventListener('click', () => {
            this.refreshCurrentModule();
        });
        
        // Theme toggle
        document.getElementById('theme-toggle')?.addEventListener('click', () => {
            this.toggleTheme();
        });
        
        // Quick actions
        document.querySelectorAll('[data-action]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.target.closest('[data-action]').getAttribute('data-action');
                this.handleQuickAction(action);
            });
        });
        
        // Global keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcuts(e);
        });
    },
    
    // Load initial application data
    loadInitialData: function() {
        // Load configuration
        this.loadConfig();
        
        // Load dashboard stats
        this.loadDashboardStats();
        
        // Request real-time updates
        if (this.socket) {
            this.socket.emit('dashboard_update_request');
        }
    },
    
    // Hide loading screen
    hideLoadingScreen: function() {
        const loadingScreen = document.getElementById('loading-screen');
        const appContainer = document.getElementById('app-container');
        
        if (loadingScreen && appContainer) {
            loadingScreen.style.opacity = '0';
            setTimeout(() => {
                loadingScreen.style.display = 'none';
                appContainer.style.display = 'flex';
                appContainer.style.opacity = '0';
                setTimeout(() => {
                    appContainer.style.opacity = '1';
                }, 50);
            }, 300);
        }
    },
    
    // Switch between modules
    switchModule: function(module) {
        if (this.currentModule === module) return;
        
        console.log(`Switching to module: ${module}`);
        
        // Update navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        
        document.querySelector(`[data-module="${module}"]`)?.classList.add('active');
        
        // Update content
        document.querySelectorAll('.module-content').forEach(content => {
            content.classList.remove('active');
        });
        
        const moduleContent = document.getElementById(`${module}-content`);
        if (moduleContent) {
            moduleContent.classList.add('active');
        }
        
        // Update page title
        const pageTitle = document.getElementById('page-title');
        if (pageTitle) {
            pageTitle.textContent = this.capitalizeFirst(module);
        }
        
        // Load module content if needed
        this.loadModule(module);
        
        this.currentModule = module;
    },
    
    // Load module content
    loadModule: function(module) {
        if (this.modules[module] && typeof this.modules[module].load === 'function') {
            this.modules[module].load();
        } else {
            // Load module content dynamically
            this.loadModuleContent(module);
        }
    },
    
    // Load module content dynamically
    loadModuleContent: function(module) {
        const contentDiv = document.getElementById(`${module}-content`);
        if (!contentDiv) return;
        
        // Show loading spinner
        contentDiv.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3">Loading ${this.capitalizeFirst(module)}...</p>
            </div>
        `;
        
        // Load module-specific content based on module type
        switch (module) {
            case 'leads':
                this.loadLeadsModule(contentDiv);
                break;
            case 'smtp':
                this.loadSmtpModule(contentDiv);
                break;
            case 'subjects':
                this.loadSubjectsModule(contentDiv);
                break;
            case 'messages':
                this.loadMessagesModule(contentDiv);
                break;
            case 'campaigns':
                this.loadCampaignsModule(contentDiv);
                break;
            case 'configurations':
                this.loadConfigurationsModule(contentDiv);
                break;
            case 'settings':
                this.loadSettingsModule(contentDiv);
                break;
            default:
                contentDiv.innerHTML = `
                    <div class="alert alert-info">
                        <h4>${this.capitalizeFirst(module)} Module</h4>
                        <p>This module is under development and will be available soon.</p>
                    </div>
                `;
        }
    },
    
    // Load configuration
    loadConfig: function() {
        fetch('/api/config')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.config = data.data;
                    this.applyConfig();
                }
            })
            .catch(error => {
                console.error('Failed to load configuration:', error);
            });
    },
    
    // Apply configuration
    applyConfig: function() {
        // Apply theme
        const theme = this.config.theme || 'dark';
        this.setTheme(theme);
        
        // Apply other configuration settings
        console.log('Configuration applied:', this.config);
    },
    
    // Load dashboard statistics
    loadDashboardStats: function() {
        fetch('/api/dashboard/stats')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.updateDashboardStats(data.data);
                }
            })
            .catch(error => {
                console.error('Failed to load dashboard stats:', error);
            });
    },
    
    // Update dashboard statistics
    updateDashboardStats: function(stats) {
        this.stats = stats;
        
        // Update leads stats
        if (stats.leads) {
            this.updateElement('total-leads', stats.leads.total || 0);
            this.updateElement('valid-emails', stats.leads.valid_emails || 0);
        }
        
        // Update SMTP stats
        if (stats.smtps) {
            this.updateElement('smtp-total', stats.smtps.total || 0);
            this.updateElement('smtp-active', stats.smtps.active || 0);
        }
        
        // Update template stats
        if (stats.templates) {
            this.updateElement('templates-total', stats.templates.total || 0);
        }
        
        // Update campaign stats
        if (stats.campaigns) {
            this.updateElement('campaigns-active', stats.campaigns.active || 0);
            this.updateElement('emails-sent', stats.campaigns.emails_sent || 0);
            this.updateElement('emails-failed', stats.campaigns.emails_failed || 0);
            
            // Calculate success rate
            const sent = stats.campaigns.emails_sent || 0;
            const failed = stats.campaigns.emails_failed || 0;
            const total = sent + failed;
            const successRate = total > 0 ? Math.round((sent / total) * 100) : 0;
            this.updateElement('success-rate', successRate + '%');
        }
        
        console.log('Dashboard stats updated:', stats);
    },
    
    // Update connection status
    updateConnectionStatus: function(connected) {
        const statusElement = document.getElementById('connection-status');
        if (!statusElement) return;
        
        const icon = statusElement.querySelector('i');
        const text = statusElement.querySelector('span');
        
        if (connected) {
            icon.className = 'fas fa-circle text-success';
            text.textContent = 'Connected';
        } else {
            icon.className = 'fas fa-circle text-danger';
            text.textContent = 'Disconnected';
        }
    },
    
    // Refresh current module
    refreshCurrentModule: function() {
        console.log(`Refreshing module: ${this.currentModule}`);
        
        if (this.currentModule === 'dashboard') {
            this.loadDashboardStats();
            if (this.socket) {
                this.socket.emit('dashboard_update_request');
            }
        } else {
            this.loadModule(this.currentModule);
        }
        
        this.showNotification('Module refreshed', 'success');
    },
    
    // Toggle theme
    toggleTheme: function() {
        const currentTheme = document.body.className.match(/theme-\w+/)?.[0] || 'theme-dark';
        const themes = ['theme-dark', 'theme-light', 'theme-blue', 'theme-green', 'theme-purple'];
        const currentIndex = themes.indexOf(currentTheme);
        const nextTheme = themes[(currentIndex + 1) % themes.length];
        
        this.setTheme(nextTheme.replace('theme-', ''));
    },
    
    // Set theme
    setTheme: function(theme) {
        document.body.className = document.body.className.replace(/theme-\w+/, '');
        document.body.classList.add(`theme-${theme}`);
        
        // Update theme toggle icon
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            const icon = themeToggle.querySelector('i');
            icon.className = theme === 'light' ? 'fas fa-sun' : 'fas fa-moon';
        }
        
        // Save theme preference
        this.config.theme = theme;
        this.saveConfig();
        
        console.log(`Theme changed to: ${theme}`);
    },
    
    // Save configuration
    saveConfig: function() {
        fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.config)
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                console.error('Failed to save configuration:', data.error);
            }
        })
        .catch(error => {
            console.error('Failed to save configuration:', error);
        });
    },
    
    // Handle quick actions
    handleQuickAction: function(action) {
        console.log(`Quick action: ${action}`);
        
        switch (action) {
            case 'new-campaign':
                this.switchModule('campaigns');
                // TODO: Open new campaign dialog
                break;
            case 'import-leads':
                this.switchModule('leads');
                // TODO: Open import dialog
                break;
            case 'add-smtp':
                this.switchModule('smtp');
                // TODO: Open new SMTP dialog
                break;
            case 'create-template':
                this.switchModule('messages');
                // TODO: Open template editor
                break;
            default:
                this.showNotification(`Action "${action}" not implemented yet`, 'info');
        }
    },
    
    // Handle keyboard shortcuts
    handleKeyboardShortcuts: function(e) {
        // Ctrl/Cmd + R - Refresh
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            e.preventDefault();
            this.refreshCurrentModule();
        }
        
        // Ctrl/Cmd + T - Toggle theme
        if ((e.ctrlKey || e.metaKey) && e.key === 't') {
            e.preventDefault();
            this.toggleTheme();
        }
        
        // Number keys 1-8 for navigation
        if (e.key >= '1' && e.key <= '8' && !e.ctrlKey && !e.metaKey && !e.altKey) {
            const modules = ['dashboard', 'leads', 'smtp', 'subjects', 'messages', 'campaigns', 'configurations', 'settings'];
            const moduleIndex = parseInt(e.key) - 1;
            if (modules[moduleIndex]) {
                this.switchModule(modules[moduleIndex]);
            }
        }
    },
    
    // Utility functions
    updateElement: function(id, value) {
        const element = document.getElementById(id);
        if (element) {
            // Add animation for number changes
            if (element.textContent !== value.toString()) {
                element.style.transform = 'scale(1.1)';
                element.textContent = value;
                setTimeout(() => {
                    element.style.transform = 'scale(1)';
                }, 200);
            }
        }
    },
    
    capitalizeFirst: function(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    },
    
    formatNumber: function(num) {
        return new Intl.NumberFormat().format(num);
    },
    
    showNotification: function(message, type = 'info', duration = 3000) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} notification`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            min-width: 300px;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        `;
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <span class="flex-grow-1">${message}</span>
                <button type="button" class="btn-close btn-close-white ms-2" aria-label="Close"></button>
            </div>
        `;
        
        // Add to document
        document.body.appendChild(notification);
        
        // Show notification
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Auto-hide after duration
        setTimeout(() => {
            this.hideNotification(notification);
        }, duration);
        
        // Close button handler
        notification.querySelector('.btn-close').addEventListener('click', () => {
            this.hideNotification(notification);
        });
    },
    
    hideNotification: function(notification) {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }
};

// Module-specific loaders (placeholder implementations)
DeepMailer.loadLeadsModule = function(contentDiv) {
    contentDiv.innerHTML = `
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-users"></i> Lead Management</h5>
                    </div>
                    <div class="card-body">
                        <p>Lead management functionality will be implemented here.</p>
                        <div class="row">
                            <div class="col-md-4">
                                <div class="stat-card">
                                    <h6>Total Leads</h6>
                                    <h3 class="text-primary">${this.stats.leads?.total || 0}</h3>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="stat-card">
                                    <h6>Valid Emails</h6>
                                    <h3 class="text-success">${this.stats.leads?.valid_emails || 0}</h3>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="stat-card">
                                    <h6>Lead Lists</h6>
                                    <h3 class="text-info">${this.stats.leads?.lists || 0}</h3>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
};

DeepMailer.loadSmtpModule = function(contentDiv) {
    contentDiv.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-envelope-open"></i> SMTP Server Management</h5>
            </div>
            <div class="card-body">
                <p>SMTP server management functionality will be implemented here.</p>
            </div>
        </div>
    `;
};

DeepMailer.loadSubjectsModule = function(contentDiv) {
    contentDiv.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-edit"></i> Subject Line Management</h5>
            </div>
            <div class="card-body">
                <p>Subject line management functionality will be implemented here.</p>
            </div>
        </div>
    `;
};

DeepMailer.loadMessagesModule = function(contentDiv) {
    contentDiv.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-file-alt"></i> Message Templates</h5>
            </div>
            <div class="card-body">
                <p>Message template management functionality will be implemented here.</p>
            </div>
        </div>
    `;
};

DeepMailer.loadCampaignsModule = function(contentDiv) {
    contentDiv.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-rocket"></i> Campaign Management</h5>
            </div>
            <div class="card-body">
                <p>Campaign management functionality will be implemented here.</p>
            </div>
        </div>
    `;
};

DeepMailer.loadConfigurationsModule = function(contentDiv) {
    contentDiv.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-cogs"></i> Configurations</h5>
            </div>
            <div class="card-body">
                <p>Configuration management functionality will be implemented here.</p>
            </div>
        </div>
    `;
};

DeepMailer.loadSettingsModule = function(contentDiv) {
    contentDiv.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-sliders-h"></i> Application Settings</h5>
            </div>
            <div class="card-body">
                <p>Application settings functionality will be implemented here.</p>
            </div>
        </div>
    `;
};

// Initialize application when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    DeepMailer.init();
});

// Handle window beforeunload
window.addEventListener('beforeunload', function() {
    if (DeepMailer.socket) {
        DeepMailer.socket.disconnect();
    }
});