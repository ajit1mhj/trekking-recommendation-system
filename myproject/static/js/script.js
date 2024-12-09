document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const showSignup = document.getElementById('showSignup');
    const showLogin = document.getElementById('showLogin');

    // Toggle between login and signup forms
    showSignup.addEventListener('click', (e) => {
        e.preventDefault();
        loginForm.classList.add('hidden');
        signupForm.classList.remove('hidden');
    });

    showLogin.addEventListener('click', (e) => {
        e.preventDefault();
        signupForm.classList.add('hidden');
        loginForm.classList.remove('hidden');
    });

    // Login form validation
    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('loginEmail');
        const password = document.getElementById('loginPassword');
        
        let isValid = true;
        
        // Reset previous error states
        removeError(email);
        removeError(password);

        // Email validation
        if (!isValidEmail(email.value)) {
            showError(email, 'Please enter a valid email address');
            isValid = false;
        }

        // Password validation
        if (password.value.length < 6) {
            showError(password, 'Password must be at least 6 characters');
            isValid = false;
        }

        if (isValid) {
            // Here you would typically send the data to your server
            console.log('Login form submitted:', {
                email: email.value,
                password: password.value
            });
        }
    });

    // Signup form validation
    signupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('signupName');
        const email = document.getElementById('signupEmail');
        const password = document.getElementById('signupPassword');
        const confirmPassword = document.getElementById('confirmPassword');
        
        let isValid = true;

        // Reset previous error states
        removeError(name);
        removeError(email);
        removeError(password);
        removeError(confirmPassword);

        // Name validation
        if (name.value.length < 2) {
            showError(name, 'Name must be at least 2 characters');
            isValid = false;
        }

        // Email validation
        if (!isValidEmail(email.value)) {
            showError(email, 'Please enter a valid email address');
            isValid = false;
        }

        // Password validation
        if (password.value.length < 6) {
            showError(password, 'Password must be at least 6 characters');
            isValid = false;
        }

        // Confirm password validation
        if (password.value !== confirmPassword.value) {
            showError(confirmPassword, 'Passwords do not match');
            isValid = false;
        }

        if (isValid) {
            // Here you would typically send the data to your server
            console.log('Signup form submitted:', {
                name: name.value,
                email: email.value,
                password: password.value
            });
        }
    });
});

// Helper functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showError(input, message) {
    input.classList.add('error');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    input.parentNode.appendChild(errorDiv);
}

function removeError(input) {
    input.classList.remove('error');
    const errorMessage = input.parentNode.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.remove();
    }
}