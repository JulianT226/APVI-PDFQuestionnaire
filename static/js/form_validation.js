document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('pdfForm');
    
    // Add client-side validation
    form.addEventListener('submit', function(event) {
        let isValid = true;
        
        // Validate email
        const email = document.getElementById('email');
        if (!isValidEmail(email.value)) {
            isValid = false;
            showError(email, 'Please enter a valid email address');
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
    
});
