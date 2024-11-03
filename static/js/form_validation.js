document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('pdfForm');
    
    // Add client-side validation
    form.addEventListener('submit', function(event) {
        let isValid = true;
        
        // Validate full name
        const fullName = document.getElementById('full_name');
        if (fullName.value.trim().length < 2) {
            isValid = false;
            showError(fullName, 'Full name must be at least 2 characters long');
        }
        
        // Validate email
        const email = document.getElementById('email');
        if (!isValidEmail(email.value)) {
            isValid = false;
            showError(email, 'Please enter a valid email address');
        }
        
        // Validate phone
        const phone = document.getElementById('phone');
        if (!isValidPhone(phone.value)) {
            isValid = false;
            showError(phone, 'Please enter a valid phone number');
        }
        
        if (!isValid) {
            event.preventDefault();
        }
    });
    
    function showError(element, message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback d-block';
        errorDiv.textContent = message;
        
        // Remove any existing error messages
        const existingError = element.parentNode.querySelector('.invalid-feedback');
        if (existingError) {
            existingError.remove();
        }
        
        element.parentNode.appendChild(errorDiv);
        element.classList.add('is-invalid');
    }
    
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
    
    function isValidPhone(phone) {
        return /^\+?[\d\s-]{10,15}$/.test(phone);
    }
});
