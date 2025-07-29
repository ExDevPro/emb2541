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
        <div class="leads-management">
            <!-- Header Actions -->
            <div class="module-header">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <div>
                        <h4><i class="fas fa-users"></i> Lead Management</h4>
                        <p class="text-muted">Import, manage, and organize your email leads</p>
                    </div>
                    <div class="header-actions">
                        <button class="btn btn-success" id="import-leads-btn">
                            <i class="fas fa-upload"></i> Import Leads
                        </button>
                        <button class="btn btn-primary" id="create-list-btn">
                            <i class="fas fa-plus"></i> Create List
                        </button>
                    </div>
                </div>
            </div>

            <!-- Statistics Cards -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="stat-card">
                        <div class="stat-header">
                            <i class="fas fa-list text-primary"></i>
                            <h6>Total Lists</h6>
                        </div>
                        <div class="stat-value">
                            <span id="leads-total-lists">${this.stats.leads?.lists || 0}</span>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <div class="stat-header">
                            <i class="fas fa-users text-info"></i>
                            <h6>Total Leads</h6>
                        </div>
                        <div class="stat-value">
                            <span id="leads-total-count">${this.stats.leads?.total || 0}</span>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <div class="stat-header">
                            <i class="fas fa-envelope text-success"></i>
                            <h6>Valid Emails</h6>
                        </div>
                        <div class="stat-value">
                            <span id="leads-valid-emails">${this.stats.leads?.valid_emails || 0}</span>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <div class="stat-header">
                            <i class="fas fa-exclamation-triangle text-warning"></i>
                            <h6>Invalid Emails</h6>
                        </div>
                        <div class="stat-value">
                            <span id="leads-invalid-emails">${(this.stats.leads?.total || 0) - (this.stats.leads?.valid_emails || 0)}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Lead Lists Table -->
            <div class="card">
                <div class="card-header">
                    <div class="d-flex justify-content-between align-items-center">
                        <h5><i class="fas fa-table"></i> Lead Lists</h5>
                        <div class="table-controls">
                            <div class="input-group input-group-sm" style="width: 250px;">
                                <input type="text" class="form-control" placeholder="Search lists..." id="lists-search">
                                <button class="btn btn-outline-secondary" type="button" id="lists-search-btn">
                                    <i class="fas fa-search"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped table-hover" id="leads-lists-table">
                            <thead>
                                <tr>
                                    <th>List Name</th>
                                    <th>Leads Count</th>
                                    <th>File Size</th>
                                    <th>Created</th>
                                    <th>Modified</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody id="leads-lists-tbody">
                                <tr>
                                    <td colspan="6" class="text-center">
                                        <div class="spinner-border text-primary" role="status">
                                            <span class="visually-hidden">Loading...</span>
                                        </div>
                                        <p class="mt-2">Loading lead lists...</p>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Selected List Details (Initially Hidden) -->
            <div class="card mt-4" id="list-details-card" style="display: none;">
                <div class="card-header">
                    <div class="d-flex justify-content-between align-items-center">
                        <h5><i class="fas fa-list-alt"></i> List Details: <span id="selected-list-name">-</span></h5>
                        <div class="list-actions">
                            <button class="btn btn-sm btn-outline-primary" id="export-list-btn">
                                <i class="fas fa-download"></i> Export
                            </button>
                            <button class="btn btn-sm btn-outline-warning" id="edit-list-btn">
                                <i class="fas fa-edit"></i> Edit
                            </button>
                            <button class="btn btn-sm btn-outline-danger" id="delete-list-btn">
                                <i class="fas fa-trash"></i> Delete
                            </button>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <!-- Pagination and Search for List Items -->
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <div class="pagination-info">
                            <span id="list-pagination-info">Showing 0 of 0 leads</span>
                        </div>
                        <div class="d-flex align-items-center gap-2">
                            <input type="text" class="form-control form-control-sm" placeholder="Search leads..." id="leads-search" style="width: 200px;">
                            <select class="form-select form-select-sm" id="leads-per-page" style="width: auto;">
                                <option value="25">25 per page</option>
                                <option value="50">50 per page</option>
                                <option value="100" selected>100 per page</option>
                                <option value="250">250 per page</option>
                            </select>
                        </div>
                    </div>

                    <!-- Leads Table -->
                    <div class="table-responsive">
                        <table class="table table-sm table-striped" id="leads-data-table">
                            <thead id="leads-data-thead">
                                <!-- Dynamic headers will be inserted here -->
                            </thead>
                            <tbody id="leads-data-tbody">
                                <!-- Dynamic data will be inserted here -->
                            </tbody>
                        </table>
                    </div>

                    <!-- Pagination Controls -->
                    <nav aria-label="Leads pagination" id="leads-pagination">
                        <!-- Pagination buttons will be inserted here -->
                    </nav>
                </div>
            </div>
        </div>

        <!-- Import Modal -->
        <div class="modal fade" id="importLeadsModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title"><i class="fas fa-upload"></i> Import Leads</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="import-leads-form" enctype="multipart/form-data">
                            <div class="mb-3">
                                <label for="list-name" class="form-label">List Name</label>
                                <input type="text" class="form-control" id="list-name" required>
                                <div class="form-text">Enter a name for your lead list</div>
                            </div>
                            
                            <div class="mb-3">
                                <label for="leads-file" class="form-label">Select File</label>
                                <input type="file" class="form-control" id="leads-file" accept=".csv,.xlsx,.xls,.txt" required>
                                <div class="form-text">Supported formats: CSV, Excel (.xlsx, .xls), Text files</div>
                            </div>
                            
                            <div class="mb-3">
                                <label for="duplicate-handling" class="form-label">Duplicate Handling</label>
                                <select class="form-select" id="duplicate-handling">
                                    <option value="skip">Skip duplicates</option>
                                    <option value="replace">Replace duplicates</option>
                                    <option value="merge">Merge duplicate data</option>
                                    <option value="keep">Keep all (including duplicates)</option>
                                </select>
                                <div class="form-text">How to handle duplicate email addresses</div>
                            </div>
                            
                            <div class="import-preview" id="import-preview" style="display: none;">
                                <h6>File Preview:</h6>
                                <div class="table-responsive">
                                    <table class="table table-sm table-bordered">
                                        <thead id="preview-thead"></thead>
                                        <tbody id="preview-tbody"></tbody>
                                    </table>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" id="import-leads-submit">
                            <i class="fas fa-upload"></i> Import Leads
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Initialize leads management functionality
    this.initializeLeadsModule();
};

// Initialize leads module functionality
DeepMailer.initializeLeadsModule = function() {
    this.currentLeadsList = null;
    this.currentPage = 1;
    this.perPage = 100;
    
    // Load initial data
    this.loadLeadLists();
    
    // Event handlers
    document.getElementById('import-leads-btn')?.addEventListener('click', () => {
        this.showImportModal();
    });
    
    document.getElementById('create-list-btn')?.addEventListener('click', () => {
        this.showCreateListModal();
    });
    
    document.getElementById('lists-search')?.addEventListener('input', (e) => {
        this.filterLeadLists(e.target.value);
    });
    
    document.getElementById('leads-search')?.addEventListener('input', (e) => {
        this.searchLeads(e.target.value);
    });
    
    document.getElementById('leads-per-page')?.addEventListener('change', (e) => {
        this.perPage = parseInt(e.target.value);
        this.loadLeadsData(this.currentLeadsList, 1);
    });
    
    document.getElementById('import-leads-submit')?.addEventListener('click', () => {
        this.submitImportForm();
    });
    
    document.getElementById('leads-file')?.addEventListener('change', (e) => {
        this.previewImportFile(e.target.files[0]);
    });
};

// Load all lead lists
DeepMailer.loadLeadLists = function() {
    API.getLeadLists()
        .then(response => {
            if (response.success) {
                this.renderLeadLists(response.data);
            } else {
                this.showNotification('Failed to load lead lists: ' + response.error, 'danger');
            }
        })
        .catch(error => {
            this.showNotification('Error loading lead lists: ' + error.message, 'danger');
        });
};

// Render lead lists table
DeepMailer.renderLeadLists = function(lists) {
    const tbody = document.getElementById('leads-lists-tbody');
    if (!tbody) return;
    
    if (lists.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-muted">
                    <i class="fas fa-inbox fa-2x mb-2"></i>
                    <p>No lead lists found. Import your first list to get started.</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = lists.map(list => `
        <tr data-list-name="${list.name}">
            <td>
                <strong>${list.name}</strong>
                <br><small class="text-muted">${list.filename}</small>
            </td>
            <td>
                <span class="badge bg-primary">${Utils.formatNumber(list.row_count)}</span>
            </td>
            <td>${Utils.formatFileSize(list.size)}</td>
            <td>
                <small>${Utils.formatDateTime(list.created)}</small>
            </td>
            <td>
                <small>${Utils.formatDateTime(list.modified)}</small>
            </td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary view-list-btn" data-list="${list.name}">
                        <i class="fas fa-eye"></i> View
                    </button>
                    <button class="btn btn-outline-secondary export-list-btn" data-list="${list.name}">
                        <i class="fas fa-download"></i>
                    </button>
                    <button class="btn btn-outline-danger delete-list-btn" data-list="${list.name}">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
    
    // Add event listeners to action buttons
    tbody.querySelectorAll('.view-list-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const listName = e.target.closest('button').getAttribute('data-list');
            this.viewLeadList(listName);
        });
    });
    
    tbody.querySelectorAll('.export-list-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const listName = e.target.closest('button').getAttribute('data-list');
            this.exportLeadList(listName);
        });
    });
    
    tbody.querySelectorAll('.delete-list-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const listName = e.target.closest('button').getAttribute('data-list');
            this.deleteLeadList(listName);
        });
    });
};

// View specific lead list
DeepMailer.viewLeadList = function(listName) {
    this.currentLeadsList = listName;
    this.currentPage = 1;
    
    // Update UI
    document.getElementById('selected-list-name').textContent = listName;
    document.getElementById('list-details-card').style.display = 'block';
    
    // Load list data
    this.loadLeadsData(listName, 1);
    
    // Scroll to details
    document.getElementById('list-details-card').scrollIntoView({ behavior: 'smooth' });
};

// Load leads data for specific list
DeepMailer.loadLeadsData = function(listName, page = 1) {
    const search = document.getElementById('leads-search')?.value || '';
    
    API.getLeadList(listName, page, this.perPage, search)
        .then(response => {
            if (response.success) {
                this.renderLeadsData(response.data);
                this.renderPagination(response.data);
            } else {
                this.showNotification('Failed to load leads: ' + response.error, 'danger');
            }
        })
        .catch(error => {
            this.showNotification('Error loading leads: ' + error.message, 'danger');
        });
};

// Render leads data table
DeepMailer.renderLeadsData = function(data) {
    const thead = document.getElementById('leads-data-thead');
    const tbody = document.getElementById('leads-data-tbody');
    const paginationInfo = document.getElementById('list-pagination-info');
    
    if (!thead || !tbody) return;
    
    // Update pagination info
    if (paginationInfo) {
        const start = (data.page - 1) * data.per_page + 1;
        const end = Math.min(start + data.leads.length - 1, data.total);
        paginationInfo.textContent = `Showing ${start}-${end} of ${Utils.formatNumber(data.total)} leads`;
    }
    
    // Render headers
    if (data.headers && data.headers.length > 0) {
        thead.innerHTML = `
            <tr>
                ${data.headers.map(header => `<th>${header}</th>`).join('')}
            </tr>
        `;
    }
    
    // Render data
    if (data.leads.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="${data.headers?.length || 1}" class="text-center text-muted">
                    <i class="fas fa-search fa-2x mb-2"></i>
                    <p>No leads found matching your criteria.</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = data.leads.map((lead, index) => `
        <tr>
            ${data.headers.map(header => `
                <td>
                    ${this.formatCellData(lead[header] || '', header)}
                </td>
            `).join('')}
        </tr>
    `).join('');
};

// Format cell data based on type
DeepMailer.formatCellData = function(value, header) {
    if (!value) return '<span class="text-muted">-</span>';
    
    // Email formatting
    if (header.toLowerCase().includes('email')) {
        const isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
        return `
            <span class="${isValid ? 'text-success' : 'text-danger'}">
                ${value}
                <i class="fas fa-${isValid ? 'check' : 'times'} ms-1"></i>
            </span>
        `;
    }
    
    // Phone formatting
    if (header.toLowerCase().includes('phone')) {
        return `<span class="text-info">${value}</span>`;
    }
    
    // Default formatting
    return value;
};

// Render pagination controls
DeepMailer.renderPagination = function(data) {
    const pagination = document.getElementById('leads-pagination');
    if (!pagination || data.total_pages <= 1) {
        pagination.innerHTML = '';
        return;
    }
    
    const currentPage = data.page;
    const totalPages = data.total_pages;
    let paginationHTML = '<ul class="pagination pagination-sm justify-content-center">';
    
    // Previous button
    paginationHTML += `
        <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
            <a class="page-link" href="#" data-page="${currentPage - 1}">Previous</a>
        </li>
    `;
    
    // Page numbers
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);
    
    if (startPage > 1) {
        paginationHTML += '<li class="page-item"><a class="page-link" href="#" data-page="1">1</a></li>';
        if (startPage > 2) {
            paginationHTML += '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
    }
    
    for (let i = startPage; i <= endPage; i++) {
        paginationHTML += `
            <li class="page-item ${i === currentPage ? 'active' : ''}">
                <a class="page-link" href="#" data-page="${i}">${i}</a>
            </li>
        `;
    }
    
    if (endPage < totalPages) {
        if (endPage < totalPages - 1) {
            paginationHTML += '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
        paginationHTML += `<li class="page-item"><a class="page-link" href="#" data-page="${totalPages}">${totalPages}</a></li>`;
    }
    
    // Next button
    paginationHTML += `
        <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
            <a class="page-link" href="#" data-page="${currentPage + 1}">Next</a>
        </li>
    `;
    
    paginationHTML += '</ul>';
    pagination.innerHTML = paginationHTML;
    
    // Add click handlers
    pagination.querySelectorAll('a[data-page]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = parseInt(e.target.getAttribute('data-page'));
            if (page && page !== currentPage) {
                this.currentPage = page;
                this.loadLeadsData(this.currentLeadsList, page);
            }
        });
    });
};

// Show import modal
DeepMailer.showImportModal = function() {
    // Reset form
    document.getElementById('import-leads-form').reset();
    document.getElementById('import-preview').style.display = 'none';
    
    // Show modal (using basic JS since Bootstrap might not be fully available)
    const modal = document.getElementById('importLeadsModal');
    if (modal) {
        modal.style.display = 'block';
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
        
        // Close handlers
        modal.querySelector('.btn-close, [data-bs-dismiss="modal"]').addEventListener('click', () => {
            this.hideImportModal();
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.hideImportModal();
            }
        });
    }
};

// Hide import modal
DeepMailer.hideImportModal = function() {
    const modal = document.getElementById('importLeadsModal');
    if (modal) {
        modal.style.display = 'none';
        modal.classList.remove('show');
        document.body.style.overflow = '';
    }
};

// Preview import file
DeepMailer.previewImportFile = function(file) {
    if (!file) return;
    
    // For now, show a simple preview message
    const preview = document.getElementById('import-preview');
    const previewThead = document.getElementById('preview-thead');
    const previewTbody = document.getElementById('preview-tbody');
    
    if (preview && previewThead && previewTbody) {
        preview.style.display = 'block';
        previewThead.innerHTML = '<tr><th>File Info</th></tr>';
        previewTbody.innerHTML = `
            <tr><td><strong>Name:</strong> ${file.name}</td></tr>
            <tr><td><strong>Size:</strong> ${Utils.formatFileSize(file.size)}</td></tr>
            <tr><td><strong>Type:</strong> ${file.type || 'Unknown'}</td></tr>
            <tr><td><em>Preview functionality will be enhanced in future updates</em></td></tr>
        `;
    }
};

// Submit import form
DeepMailer.submitImportForm = function() {
    const form = document.getElementById('import-leads-form');
    const listName = document.getElementById('list-name').value;
    const file = document.getElementById('leads-file').files[0];
    const duplicateHandling = document.getElementById('duplicate-handling').value;
    
    if (!listName || !file) {
        this.showNotification('Please fill in all required fields', 'warning');
        return;
    }
    
    // Create FormData
    const formData = new FormData();
    formData.append('file', file);
    formData.append('list_name', listName);
    formData.append('duplicate_handling', duplicateHandling);
    
    // Show loading state
    const submitBtn = document.getElementById('import-leads-submit');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Importing...';
    submitBtn.disabled = true;
    
    // Submit import
    API.importLeads(formData)
        .then(response => {
            if (response.success) {
                this.showNotification('Leads imported successfully!', 'success');
                this.hideImportModal();
                this.loadLeadLists(); // Refresh the lists
            } else {
                this.showNotification('Import failed: ' + response.error, 'danger');
            }
        })
        .catch(error => {
            this.showNotification('Import error: ' + error.message, 'danger');
        })
        .finally(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        });
};

// Filter lead lists
DeepMailer.filterLeadLists = function(searchTerm) {
    const tbody = document.getElementById('leads-lists-tbody');
    if (!tbody) return;
    
    const rows = tbody.querySelectorAll('tr[data-list-name]');
    rows.forEach(row => {
        const listName = row.getAttribute('data-list-name').toLowerCase();
        const visible = listName.includes(searchTerm.toLowerCase());
        row.style.display = visible ? '' : 'none';
    });
};

// Search leads in current list
DeepMailer.searchLeads = function(searchTerm) {
    if (this.currentLeadsList) {
        this.currentPage = 1;
        this.loadLeadsData(this.currentLeadsList, 1);
    }
};

// Export lead list
DeepMailer.exportLeadList = function(listName) {
    this.showNotification('Export functionality will be implemented soon', 'info');
};

// Delete lead list
DeepMailer.deleteLeadList = function(listName) {
    if (confirm(`Are you sure you want to delete the lead list "${listName}"? This action cannot be undone.`)) {
        this.showNotification('Delete functionality will be implemented soon', 'info');
    }
};

DeepMailer.loadSmtpModule = function(contentDiv) {
    contentDiv.innerHTML = `
        <div class="smtp-management">
            <!-- Header Actions -->
            <div class="module-header">
                <div class="d-flex justify-content-between align-items-center mb-4">
                    <div>
                        <h4><i class="fas fa-envelope-open"></i> SMTP Server Management</h4>
                        <p class="text-muted">Configure and manage your email sending servers</p>
                    </div>
                    <div class="header-actions">
                        <button class="btn btn-success" id="test-all-smtp-btn">
                            <i class="fas fa-check-circle"></i> Test All
                        </button>
                        <button class="btn btn-primary" id="add-smtp-btn">
                            <i class="fas fa-plus"></i> Add SMTP Server
                        </button>
                    </div>
                </div>
            </div>

            <!-- Statistics Cards -->
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="stat-card">
                        <div class="stat-header">
                            <i class="fas fa-server text-primary"></i>
                            <h6>Total Servers</h6>
                        </div>
                        <div class="stat-value">
                            <span id="smtp-total-count">${this.stats.smtps?.total || 0}</span>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <div class="stat-header">
                            <i class="fas fa-check-circle text-success"></i>
                            <h6>Active Servers</h6>
                        </div>
                        <div class="stat-value">
                            <span id="smtp-active-count">${this.stats.smtps?.active || 0}</span>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <div class="stat-header">
                            <i class="fas fa-times-circle text-danger"></i>
                            <h6>Inactive Servers</h6>
                        </div>
                        <div class="stat-value">
                            <span id="smtp-inactive-count">${this.stats.smtps?.inactive || 0}</span>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="stat-card">
                        <div class="stat-header">
                            <i class="fas fa-paper-plane text-info"></i>
                            <h6>Ready to Send</h6>
                        </div>
                        <div class="stat-value">
                            <span id="smtp-ready-count">0</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- SMTP Servers Table -->
            <div class="card">
                <div class="card-header">
                    <div class="d-flex justify-content-between align-items-center">
                        <h5><i class="fas fa-table"></i> SMTP Servers</h5>
                        <div class="table-controls">
                            <div class="input-group input-group-sm" style="width: 250px;">
                                <input type="text" class="form-control" placeholder="Search servers..." id="smtp-search">
                                <button class="btn btn-outline-secondary" type="button" id="smtp-search-btn">
                                    <i class="fas fa-search"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-striped table-hover" id="smtp-servers-table">
                            <thead>
                                <tr>
                                    <th>Server Name</th>
                                    <th>Host:Port</th>
                                    <th>Username</th>
                                    <th>From Email</th>
                                    <th>Security</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody id="smtp-servers-tbody">
                                <tr>
                                    <td colspan="7" class="text-center">
                                        <div class="spinner-border text-primary" role="status">
                                            <span class="visually-hidden">Loading...</span>
                                        </div>
                                        <p class="mt-2">Loading SMTP servers...</p>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Add/Edit SMTP Modal -->
        <div class="modal fade" id="smtpModal" tabindex="-1">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-server"></i> <span id="smtp-modal-title">Add SMTP Server</span>
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="smtp-form">
                            <div class="row">
                                <!-- Basic Configuration -->
                                <div class="col-md-6">
                                    <h6 class="border-bottom pb-2 mb-3"><i class="fas fa-cog"></i> Basic Configuration</h6>
                                    
                                    <div class="mb-3">
                                        <label for="smtp-name" class="form-label">Server Name *</label>
                                        <input type="text" class="form-control" id="smtp-name" required>
                                        <div class="form-text">Unique name for this SMTP server</div>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="smtp-description" class="form-label">Description</label>
                                        <input type="text" class="form-control" id="smtp-description">
                                        <div class="form-text">Optional description</div>
                                    </div>
                                    
                                    <div class="row">
                                        <div class="col-md-8">
                                            <div class="mb-3">
                                                <label for="smtp-host" class="form-label">SMTP Host *</label>
                                                <input type="text" class="form-control" id="smtp-host" required>
                                            </div>
                                        </div>
                                        <div class="col-md-4">
                                            <div class="mb-3">
                                                <label for="smtp-port" class="form-label">Port *</label>
                                                <select class="form-select" id="smtp-port">
                                                    <option value="587">587 (TLS)</option>
                                                    <option value="465">465 (SSL)</option>
                                                    <option value="25">25 (Plain)</option>
                                                    <option value="2525">2525 (Alt)</option>
                                                </select>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="smtp-security" class="form-label">Security Type</label>
                                        <select class="form-select" id="smtp-security">
                                            <option value="auto">Auto Detect</option>
                                            <option value="none">None</option>
                                            <option value="ssl">SSL</option>
                                            <option value="tls">TLS</option>
                                        </select>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="smtp-auth" class="form-label">Authentication</label>
                                        <select class="form-select" id="smtp-auth">
                                            <option value="auto">Auto</option>
                                            <option value="plain">PLAIN</option>
                                            <option value="login">LOGIN</option>
                                            <option value="cram-md5">CRAM-MD5</option>
                                        </select>
                                    </div>
                                </div>
                                
                                <!-- Credentials -->
                                <div class="col-md-6">
                                    <h6 class="border-bottom pb-2 mb-3"><i class="fas fa-key"></i> Credentials</h6>
                                    
                                    <div class="mb-3">
                                        <label for="smtp-username" class="form-label">Username/Email *</label>
                                        <input type="email" class="form-control" id="smtp-username" required>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="smtp-password" class="form-label">Password *</label>
                                        <div class="input-group">
                                            <input type="password" class="form-control" id="smtp-password" required>
                                            <button type="button" class="btn btn-outline-secondary" id="toggle-password">
                                                <i class="fas fa-eye"></i>
                                            </button>
                                        </div>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <label for="smtp-from-email" class="form-label">From Email *</label>
                                        <input type="email" class="form-control" id="smtp-from-email" required>
                                        <div class="form-text">The email address emails will be sent from</div>
                                    </div>
                                    
                                    <!-- From Name Configuration -->
                                    <div class="mb-3">
                                        <div class="d-flex justify-content-between align-items-center">
                                            <label class="form-label">From Name Header</label>
                                            <div class="form-check form-switch">
                                                <input class="form-check-input" type="checkbox" id="enable-from-name">
                                                <label class="form-check-label" for="enable-from-name">Enable</label>
                                            </div>
                                        </div>
                                        <div id="from-name-config" style="display: none;">
                                            <div class="mb-2">
                                                <select class="form-select form-select-sm" id="from-name-mode">
                                                    <option value="custom">Custom Names</option>
                                                    <option value="faker">Auto-generated (Faker)</option>
                                                </select>
                                            </div>
                                            <textarea class="form-control form-control-sm" id="from-name-values" rows="3" placeholder="Enter custom names (one per line)"></textarea>
                                            <div class="row mt-2">
                                                <div class="col-6">
                                                    <select class="form-select form-select-sm" id="from-name-rotation">
                                                        <option value="each">Each email</option>
                                                        <option value="range">After X emails</option>
                                                    </select>
                                                </div>
                                                <div class="col-6">
                                                    <select class="form-select form-select-sm" id="from-name-policy">
                                                        <option value="must">Must use</option>
                                                        <option value="random">Random use</option>
                                                    </select>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Advanced Settings -->
                            <div class="row mt-4">
                                <div class="col-12">
                                    <h6 class="border-bottom pb-2 mb-3"><i class="fas fa-cogs"></i> Advanced Settings</h6>
                                </div>
                                
                                <!-- Rate Limiting -->
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <div class="d-flex justify-content-between align-items-center">
                                            <label class="form-label">Rate Limiting</label>
                                            <div class="form-check form-switch">
                                                <input class="form-check-input" type="checkbox" id="enable-rate-limit">
                                                <label class="form-check-label" for="enable-rate-limit">Enable</label>
                                            </div>
                                        </div>
                                        <div id="rate-limit-config" style="display: none;">
                                            <div class="row">
                                                <div class="col-6">
                                                    <select class="form-select form-select-sm" id="rate-limit-type">
                                                        <option value="minute">Per Minute</option>
                                                        <option value="hour">Per Hour</option>
                                                        <option value="day">Per Day</option>
                                                        <option value="week">Per Week</option>
                                                        <option value="month">Per Month</option>
                                                    </select>
                                                </div>
                                                <div class="col-6">
                                                    <input type="number" class="form-control form-control-sm" id="rate-limit-value" min="1" placeholder="Limit">
                                                </div>
                                            </div>
                                            <div class="mt-2">
                                                <input type="number" class="form-control form-control-sm" id="total-limit" placeholder="Total limit (0 = unlimited)">
                                                <div class="form-text">Maximum total emails before deactivation</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Proxy Settings -->
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <div class="d-flex justify-content-between align-items-center">
                                            <label class="form-label">Proxy Configuration</label>
                                            <div class="form-check form-switch">
                                                <input class="form-check-input" type="checkbox" id="enable-proxy">
                                                <label class="form-check-label" for="enable-proxy">Enable</label>
                                            </div>
                                        </div>
                                        <div id="proxy-config" style="display: none;">
                                            <div class="row">
                                                <div class="col-8">
                                                    <input type="text" class="form-control form-control-sm" id="proxy-host" placeholder="Proxy Host/IP">
                                                </div>
                                                <div class="col-4">
                                                    <input type="number" class="form-control form-control-sm" id="proxy-port" placeholder="Port">
                                                </div>
                                            </div>
                                            <div class="row mt-2">
                                                <div class="col-6">
                                                    <select class="form-select form-select-sm" id="proxy-type">
                                                        <option value="http">HTTP</option>
                                                        <option value="https">HTTPS</option>
                                                        <option value="socks5">SOCKS5</option>
                                                    </select>
                                                </div>
                                                <div class="col-6">
                                                    <div class="form-check form-check-sm">
                                                        <input class="form-check-input" type="checkbox" id="proxy-auth">
                                                        <label class="form-check-label" for="proxy-auth">Auth Required</label>
                                                    </div>
                                                </div>
                                            </div>
                                            <div id="proxy-auth-fields" style="display: none;" class="mt-2">
                                                <div class="row">
                                                    <div class="col-6">
                                                        <input type="text" class="form-control form-control-sm" id="proxy-username" placeholder="Username">
                                                    </div>
                                                    <div class="col-6">
                                                        <input type="password" class="form-control form-control-sm" id="proxy-password" placeholder="Password">
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </form>
                        
                        <!-- Test Results -->
                        <div id="test-results" style="display: none;" class="mt-4">
                            <h6><i class="fas fa-flask"></i> Test Results</h6>
                            <div class="alert" id="test-results-alert"></div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary" id="test-smtp-connection">
                            <i class="fas fa-flask"></i> Test Connection
                        </button>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" id="save-smtp-server">
                            <i class="fas fa-save"></i> Save Server
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Initialize SMTP management functionality
    this.initializeSmtpModule();
};

// Initialize SMTP module functionality  
DeepMailer.initializeSmtpModule = function() {
    this.currentSmtpData = null;
    this.editingSmtp = false;
    
    // Load initial data
    this.loadSmtpServers();
    
    // Event handlers
    document.getElementById('add-smtp-btn')?.addEventListener('click', () => {
        this.showSmtpModal();
    });
    
    document.getElementById('test-all-smtp-btn')?.addEventListener('click', () => {
        this.testAllSmtpServers();
    });
    
    document.getElementById('smtp-search')?.addEventListener('input', (e) => {
        this.filterSmtpServers(e.target.value);
    });
    
    document.getElementById('save-smtp-server')?.addEventListener('click', () => {
        this.saveSmtpServer();
    });
    
    document.getElementById('test-smtp-connection')?.addEventListener('click', () => {
        this.testSmtpConnection();
    });
    
    // Toggle switches
    document.getElementById('enable-from-name')?.addEventListener('change', (e) => {
        document.getElementById('from-name-config').style.display = e.target.checked ? 'block' : 'none';
    });
    
    document.getElementById('enable-rate-limit')?.addEventListener('change', (e) => {
        document.getElementById('rate-limit-config').style.display = e.target.checked ? 'block' : 'none';
    });
    
    document.getElementById('enable-proxy')?.addEventListener('change', (e) => {
        document.getElementById('proxy-config').style.display = e.target.checked ? 'block' : 'none';
    });
    
    document.getElementById('proxy-auth')?.addEventListener('change', (e) => {
        document.getElementById('proxy-auth-fields').style.display = e.target.checked ? 'block' : 'none';
    });
    
    // Password toggle
    document.getElementById('toggle-password')?.addEventListener('click', () => {
        const passwordField = document.getElementById('smtp-password');
        const icon = document.querySelector('#toggle-password i');
        if (passwordField.type === 'password') {
            passwordField.type = 'text';
            icon.className = 'fas fa-eye-slash';
        } else {
            passwordField.type = 'password';
            icon.className = 'fas fa-eye';
        }
    });
    
    // Port suggestions
    document.getElementById('smtp-port')?.addEventListener('change', (e) => {
        const port = e.target.value;
        const securityField = document.getElementById('smtp-security');
        if (port === '465') {
            securityField.value = 'ssl';
        } else if (port === '587') {
            securityField.value = 'tls';
        } else if (port === '25') {
            securityField.value = 'none';
        }
    });
};

// Load all SMTP servers
DeepMailer.loadSmtpServers = function() {
    API.getSmtpServers()
        .then(response => {
            if (response.success) {
                this.renderSmtpServers(response.data);
                this.updateSmtpStats(response.data);
            } else {
                this.showNotification('Failed to load SMTP servers: ' + response.error, 'danger');
            }
        })
        .catch(error => {
            this.showNotification('Error loading SMTP servers: ' + error.message, 'danger');
        });
};

// Render SMTP servers table
DeepMailer.renderSmtpServers = function(servers) {
    const tbody = document.getElementById('smtp-servers-tbody');
    if (!tbody) return;
    
    if (servers.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-muted">
                    <i class="fas fa-server fa-2x mb-2"></i>
                    <p>No SMTP servers configured. Add your first server to get started.</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = servers.map(server => {
        const statusClass = this.getStatusClass(server.status || 'unknown');
        const statusIcon = this.getStatusIcon(server.status || 'unknown');
        
        return `
            <tr data-server-name="${server.name || server.server_name || 'Unknown'}">
                <td>
                    <strong>${server.name || server.server_name || 'Unknown'}</strong>
                    ${server.description ? `<br><small class="text-muted">${server.description}</small>` : ''}
                </td>
                <td>
                    <code>${server.host || 'Unknown'}:${server.port || 'Unknown'}</code>
                </td>
                <td>
                    <span class="text-info">${server.username || server.email || 'Not set'}</span>
                </td>
                <td>
                    <span class="text-primary">${server.from_email || server.username || 'Not set'}</span>
                </td>
                <td>
                    <span class="badge bg-secondary">${(server.security || 'auto').toUpperCase()}</span>
                </td>
                <td>
                    <span class="badge bg-${statusClass}">
                        <i class="fas fa-${statusIcon}"></i> ${(server.status || 'unknown').toUpperCase()}
                    </span>
                </td>
                <td>
                    <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary test-server-btn" data-server="${server.name || server.server_name}">
                            <i class="fas fa-flask"></i>
                        </button>
                        <button class="btn btn-outline-secondary edit-server-btn" data-server="${server.name || server.server_name}">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn btn-outline-info details-server-btn" data-server="${server.name || server.server_name}">
                            <i class="fas fa-info-circle"></i>
                        </button>
                        <button class="btn btn-outline-danger delete-server-btn" data-server="${server.name || server.server_name}">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
    
    // Add event listeners to action buttons
    tbody.querySelectorAll('.test-server-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const serverName = e.target.closest('button').getAttribute('data-server');
            this.testSingleServer(serverName);
        });
    });
    
    tbody.querySelectorAll('.edit-server-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const serverName = e.target.closest('button').getAttribute('data-server');
            this.editSmtpServer(serverName);
        });
    });
    
    tbody.querySelectorAll('.details-server-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const serverName = e.target.closest('button').getAttribute('data-server');
            this.showServerDetails(serverName);
        });
    });
    
    tbody.querySelectorAll('.delete-server-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const serverName = e.target.closest('button').getAttribute('data-server');
            this.deleteSmtpServer(serverName);
        });
    });
};

// Update SMTP statistics
DeepMailer.updateSmtpStats = function(servers) {
    const totalCount = servers.length;
    const activeCount = servers.filter(s => s.status === 'active').length;
    const inactiveCount = servers.filter(s => s.status === 'inactive').length;
    const readyCount = servers.filter(s => s.status === 'active' && !s.limit_reached).length;
    
    this.updateElement('smtp-total-count', totalCount);
    this.updateElement('smtp-active-count', activeCount);
    this.updateElement('smtp-inactive-count', inactiveCount);
    this.updateElement('smtp-ready-count', readyCount);
};

// Get status CSS class
DeepMailer.getStatusClass = function(status) {
    switch (status.toLowerCase()) {
        case 'active': return 'success';
        case 'inactive': return 'danger';
        case 'testing': return 'warning';
        case 'limited': return 'warning';
        default: return 'secondary';
    }
};

// Get status icon
DeepMailer.getStatusIcon = function(status) {
    switch (status.toLowerCase()) {
        case 'active': return 'check-circle';
        case 'inactive': return 'times-circle';
        case 'testing': return 'spinner fa-spin';
        case 'limited': return 'exclamation-triangle';
        default: return 'question-circle';
    }
};

// Show SMTP modal
DeepMailer.showSmtpModal = function(editData = null) {
    this.editingSmtp = !!editData;
    this.currentSmtpData = editData;
    
    // Reset form
    document.getElementById('smtp-form').reset();
    document.getElementById('test-results').style.display = 'none';
    
    // Update modal title
    const title = document.getElementById('smtp-modal-title');
    if (title) {
        title.textContent = editData ? 'Edit SMTP Server' : 'Add SMTP Server';
    }
    
    // Hide advanced config sections
    document.getElementById('from-name-config').style.display = 'none';
    document.getElementById('rate-limit-config').style.display = 'none';
    document.getElementById('proxy-config').style.display = 'none';
    document.getElementById('proxy-auth-fields').style.display = 'none';
    
    // Fill form if editing
    if (editData) {
        this.fillSmtpForm(editData);
    }
    
    // Show modal
    const modal = document.getElementById('smtpModal');
    if (modal) {
        modal.style.display = 'block';
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
        
        // Close handlers
        modal.querySelector('.btn-close, [data-bs-dismiss="modal"]').addEventListener('click', () => {
            this.hideSmtpModal();
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.hideSmtpModal();
            }
        });
    }
};

// Hide SMTP modal
DeepMailer.hideSmtpModal = function() {
    const modal = document.getElementById('smtpModal');
    if (modal) {
        modal.style.display = 'none';
        modal.classList.remove('show');
        document.body.style.overflow = '';
    }
};

// Fill SMTP form with data
DeepMailer.fillSmtpForm = function(data) {
    document.getElementById('smtp-name').value = data.name || data.server_name || '';
    document.getElementById('smtp-description').value = data.description || '';
    document.getElementById('smtp-host').value = data.host || '';
    document.getElementById('smtp-port').value = data.port || '587';
    document.getElementById('smtp-security').value = data.security || 'auto';
    document.getElementById('smtp-auth').value = data.auth || 'auto';
    document.getElementById('smtp-username').value = data.username || data.email || '';
    document.getElementById('smtp-password').value = data.password || '';
    document.getElementById('smtp-from-email').value = data.from_email || data.username || '';
    
    // Advanced settings would be filled here
};

// Save SMTP server
DeepMailer.saveSmtpServer = function() {
    const formData = {
        name: document.getElementById('smtp-name').value,
        description: document.getElementById('smtp-description').value,
        host: document.getElementById('smtp-host').value,
        port: parseInt(document.getElementById('smtp-port').value),
        security: document.getElementById('smtp-security').value,
        auth: document.getElementById('smtp-auth').value,
        username: document.getElementById('smtp-username').value,
        password: document.getElementById('smtp-password').value,
        from_email: document.getElementById('smtp-from-email').value,
        
        // Advanced settings
        from_name_enabled: document.getElementById('enable-from-name').checked,
        rate_limit_enabled: document.getElementById('enable-rate-limit').checked,
        proxy_enabled: document.getElementById('enable-proxy').checked,
        
        status: 'inactive', // Will be set to active after successful test
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
    };
    
    // Validation
    if (!formData.name || !formData.host || !formData.username || !formData.password || !formData.from_email) {
        this.showNotification('Please fill in all required fields', 'warning');
        return;
    }
    
    // Show loading state
    const saveBtn = document.getElementById('save-smtp-server');
    const originalText = saveBtn.innerHTML;
    saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
    saveBtn.disabled = true;
    
    // Save server
    API.saveSmtpServer(formData)
        .then(response => {
            if (response.success) {
                this.showNotification('SMTP server saved successfully!', 'success');
                this.hideSmtpModal();
                this.loadSmtpServers(); // Refresh the list
            } else {
                this.showNotification('Failed to save SMTP server: ' + response.error, 'danger');
            }
        })
        .catch(error => {
            this.showNotification('Error saving SMTP server: ' + error.message, 'danger');
        })
        .finally(() => {
            saveBtn.innerHTML = originalText;
            saveBtn.disabled = false;
        });
};

// Test SMTP connection
DeepMailer.testSmtpConnection = function() {
    const formData = {
        host: document.getElementById('smtp-host').value,
        port: parseInt(document.getElementById('smtp-port').value),
        security: document.getElementById('smtp-security').value,
        auth: document.getElementById('smtp-auth').value,
        username: document.getElementById('smtp-username').value,
        password: document.getElementById('smtp-password').value,
        from_email: document.getElementById('smtp-from-email').value
    };
    
    // Validation
    if (!formData.host || !formData.username || !formData.password) {
        this.showNotification('Please fill in host, username, and password for testing', 'warning');
        return;
    }
    
    // Show loading state
    const testBtn = document.getElementById('test-smtp-connection');
    const originalText = testBtn.innerHTML;
    testBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testing...';
    testBtn.disabled = true;
    
    // Show test results area
    const testResults = document.getElementById('test-results');
    const testAlert = document.getElementById('test-results-alert');
    testResults.style.display = 'block';
    testAlert.className = 'alert alert-info';
    testAlert.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testing SMTP connection...';
    
    // Test connection
    API.testSmtpServer(formData)
        .then(response => {
            if (response.success) {
                testAlert.className = 'alert alert-success';
                testAlert.innerHTML = `
                    <i class="fas fa-check-circle"></i> 
                    <strong>Connection Successful!</strong><br>
                    ${response.data.message || 'SMTP server is working correctly.'}
                `;
            } else {
                testAlert.className = 'alert alert-danger';
                testAlert.innerHTML = `
                    <i class="fas fa-times-circle"></i> 
                    <strong>Connection Failed</strong><br>
                    ${response.error || 'Unable to connect to SMTP server.'}
                `;
            }
        })
        .catch(error => {
            testAlert.className = 'alert alert-danger';
            testAlert.innerHTML = `
                <i class="fas fa-exclamation-triangle"></i> 
                <strong>Test Error</strong><br>
                ${error.message}
            `;
        })
        .finally(() => {
            testBtn.innerHTML = originalText;
            testBtn.disabled = false;
        });
};

// Test all SMTP servers
DeepMailer.testAllSmtpServers = function() {
    this.showNotification('Testing all SMTP servers...', 'info');
    // Implementation would test all servers
};

// Test single server
DeepMailer.testSingleServer = function(serverName) {
    this.showNotification(`Testing ${serverName}...`, 'info');
    // Implementation would test specific server
};

// Edit SMTP server
DeepMailer.editSmtpServer = function(serverName) {
    // Find server data and show modal with edit mode
    API.getSmtpServers()
        .then(response => {
            if (response.success) {
                const server = response.data.find(s => (s.name || s.server_name) === serverName);
                if (server) {
                    this.showSmtpModal(server);
                }
            }
        });
};

// Show server details
DeepMailer.showServerDetails = function(serverName) {
    this.showNotification('Server details functionality will be implemented soon', 'info');
};

// Delete SMTP server
DeepMailer.deleteSmtpServer = function(serverName) {
    if (confirm(`Are you sure you want to delete the SMTP server "${serverName}"? This action cannot be undone.`)) {
        this.showNotification('Delete functionality will be implemented soon', 'info');
    }
};

// Filter SMTP servers
DeepMailer.filterSmtpServers = function(searchTerm) {
    const tbody = document.getElementById('smtp-servers-tbody');
    if (!tbody) return;
    
    const rows = tbody.querySelectorAll('tr[data-server-name]');
    rows.forEach(row => {
        const serverName = row.getAttribute('data-server-name').toLowerCase();
        const serverData = row.textContent.toLowerCase();
        const visible = serverData.includes(searchTerm.toLowerCase());
        row.style.display = visible ? '' : 'none';
    });
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