/**
 * Cypress Point Strata - Navigation & Mobile Menu
 * Handles hamburger menu toggle and dropdown functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

    // Hamburger menu toggle
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }

    // Close menu when a link is clicked (mobile)
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Don't close if it's a dropdown toggle
            if (!this.classList.contains('dropdown-toggle')) {
                if (hamburger && hamburger.classList.contains('active')) {
                    hamburger.classList.remove('active');
                    navMenu.classList.remove('active');
                }
            }
        });
    });

    // Dropdown menu toggle for mobile
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            // Check if we're on mobile
            if (window.innerWidth < 768) {
                e.preventDefault();
                const parentItem = this.closest('.nav-item');
                const dropdownMenu = parentItem.querySelector('.dropdown-menu');
                
                if (dropdownMenu) {
                    dropdownMenu.classList.toggle('active');
                    toggle.classList.toggle('active');
                }
            }
        });
    });

    // Collapsible sections
    const collapsibleHeaders = document.querySelectorAll('.collapsible-header');
    collapsibleHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const collapsible = this.closest('.collapsible');
            collapsible.classList.toggle('active');
        });
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // Handle window resize to reset menu state
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            if (window.innerWidth >= 768) {
                // Reset mobile menu on resize to desktop
                if (hamburger) {
                    hamburger.classList.remove('active');
                }
                if (navMenu) {
                    navMenu.classList.remove('active');
                }
            }
        }, 250);
    });

    // Mark active page in navigation
    setActivePage();

    function setActivePage() {
        const currentPath = window.location.pathname.split('/').pop() || 'index.html';
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href === currentPath || (currentPath === '' && href === 'index.html')) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }
});

/**
 * Utility function to expand a specific collapsible section
 * Usage: expandCollapsible('section-id')
 */
function expandCollapsible(id) {
    const element = document.getElementById(id);
    if (element && element.classList.contains('collapsible')) {
        element.classList.add('active');
    }
}

/**
 * Utility function to collapse a specific collapsible section
 * Usage: collapseCollapsible('section-id')
 */
function collapseCollapsible(id) {
    const element = document.getElementById(id);
    if (element && element.classList.contains('collapsible')) {
        element.classList.remove('active');
    }
}

/**
 * Utility function to toggle a specific collapsible section
 * Usage: toggleCollapsible('section-id')
 */
function toggleCollapsible(id) {
    const element = document.getElementById(id);
    if (element && element.classList.contains('collapsible')) {
        element.classList.toggle('active');
    }
}

/**
 * Close all open collapsibles
 */
function closeAllCollapsibles() {
    document.querySelectorAll('.collapsible.active').forEach(item => {
        item.classList.remove('active');
    });
}

/**
 * Open all collapsibles
 */
function openAllCollapsibles() {
    document.querySelectorAll('.collapsible').forEach(item => {
        item.classList.add('active');
    });
}
