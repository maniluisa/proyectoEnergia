/*!
* Start Bootstrap - Freelancer v7.0.7 (https://startbootstrap.com/theme/freelancer)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-freelancer/blob/master/LICENSE)
*/
//
// Scripts
// 

 // Modo Oscuro / Claro
 var themeToggle = document.getElementById('theme-toggle');
 var themeIcon = document.getElementById('theme-icon');

 themeToggle.addEventListener('click', function() {
     document.documentElement.classList.toggle('dark');
     
     // Cambiar ícono
     if (document.documentElement.classList.contains('dark')) {
         // Ícono de sol para modo oscuro
         themeIcon.innerHTML = `
             <circle cx="12" cy="12" r="4"></circle>
             <path d="M12 2v2"></path>
             <path d="M12 20v2"></path>
             <path d="m4.93 4.93 1.41 1.41"></path>
             <path d="m17.66 17.66 1.41 1.41"></path>
             <path d="M2 12h2"></path>
             <path d="M20 12h2"></path>
             <path d="m6.34 17.66-1.41 1.41"></path>
             <path d="m19.07 4.93-1.41 1.41"></path>
         `;
     } else {
         // Ícono de luna para modo claro
         themeIcon.innerHTML = `
             <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z" />
         `;
     }
 });

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});