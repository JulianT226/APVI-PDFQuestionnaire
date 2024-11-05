document.addEventListener('DOMContentLoaded', function() {
    const formSections = document.querySelectorAll('.form-section');
    const form = document.getElementById('pdfForm');
    let currentSection = 0;
    
    // Hide all sections except the first one
    formSections.forEach((section, index) => {
        if (index !== 0) {
            section.style.display = 'none';
        }
    });
    
    // Add navigation buttons to each section
    formSections.forEach((section, index) => {
        const navButtons = document.createElement('div');
        navButtons.className = 'form-navigation d-flex justify-content-between mt-4';
        
        // Previous button (except for first section)
        if (index > 0) {
            const prevButton = document.createElement('button');
            prevButton.type = 'button';
            prevButton.className = 'btn btn-outline-primary';
            prevButton.innerHTML = '<i class="fas fa-arrow-left me-2"></i>Previous';
            prevButton.onclick = () => navigateSection(index - 1);
            navButtons.appendChild(prevButton);
        }
        
        // Next/Submit button
        const nextButton = document.createElement('button');
        nextButton.type = 'button';  // Always button by default
        nextButton.className = 'btn btn-primary';
        
        if (index === formSections.length - 1) {
            // Replace next button with submit button in last section
            const submitButton = document.createElement('button');
            submitButton.type = 'submit';
            submitButton.className = 'btn btn-primary ms-auto';
            submitButton.innerHTML = 'Submit Application';
            navButtons.appendChild(submitButton);
        } else {
            // Regular next button for all other sections
            nextButton.innerHTML = 'Next<i class="fas fa-arrow-right ms-2"></i>';
            nextButton.onclick = () => {
                if (validateSection(index)) {
                    navigateSection(index + 1);
                }
            };
            navButtons.appendChild(nextButton);
        }
        
        section.querySelector('.section-content').appendChild(navButtons);
    });
    
    // Create progress indicator
    const progressContainer = document.createElement('div');
    progressContainer.className = 'progress-container mb-4';
    progressContainer.innerHTML = `
        <div class="progress-steps d-flex justify-content-between">
            ${Array.from(formSections).map((section, index) => `
                <div class="progress-step ${index === 0 ? 'active' : ''}">
                    <div class="step-number">${index + 1}</div>
                    <div class="step-label">${section.querySelector('h3').textContent}</div>
                </div>
            `).join('')}
        </div>
    `;
    form.insertBefore(progressContainer, form.firstChild);
    
    // Navigation function
    function navigateSection(index) {
        formSections[currentSection].style.display = 'none';
        formSections[index].style.display = 'block';
        currentSection = index;
        
        // Update progress indicator
        document.querySelectorAll('.progress-step').forEach((step, i) => {
            if (i === currentSection) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });
        
        // Scroll to top of the form
        formSections[index].scrollIntoView({ behavior: 'smooth' });
    }
    
    // Validation function
    function validateSection(index) {
        const section = formSections[index];
        let isValid = true;
        
        // Validate required fields in current section
        const requiredFields = section.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            if (!field.value) {
                isValid = false;
                field.classList.add('is-invalid');
                const feedback = field.nextElementSibling || document.createElement('div');
                feedback.className = 'invalid-feedback d-block';
                feedback.textContent = 'This field is required';
                if (!field.nextElementSibling) {
                    field.parentNode.appendChild(feedback);
                }
            } else {
                field.classList.remove('is-invalid');
                const feedback = field.nextElementSibling;
                if (feedback && feedback.classList.contains('invalid-feedback')) {
                    feedback.remove();
                }
            }
        });
        
        return isValid;
    }
});
