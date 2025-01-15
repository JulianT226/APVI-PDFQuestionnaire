document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('pdfForm');
    if (!form) {
        return;
    }
    const formSections = form.querySelectorAll('.form-section');
    let currentSection = 0;

    let pendingNavigationIndex = null;

    // Get the confirm button from the modal
    const confirmButton = document.getElementById('jobTitleModalConfirm');
    if (confirmButton) {
        confirmButton.onclick = () => {
            if (pendingNavigationIndex !== null) {
                navigateSection(pendingNavigationIndex);
                pendingNavigationIndex = null;
            }
            // Hide the modal
            const jobTitleModal = bootstrap.Modal.getInstance(document.getElementById('jobTitleModal'));
            if (jobTitleModal) {
                jobTitleModal.hide();
            }
        };
    }
    
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

        const leftContainer = document.createElement('div');
        const rightContainer = document.createElement('div');

        // Previous button (except for first section)
        if (index > 0) {
            const prevButton = document.createElement('button');
            prevButton.type = 'button';
            prevButton.className = 'btn btn-outline-primary ms-3';
            prevButton.innerHTML = '<i class="fas fa-arrow-left me-2"></i>Previous';
            prevButton.onclick = () => navigateSection(index - 1);
            leftContainer.appendChild(prevButton);
        }
        
        // Next/Submit button
        if (index === formSections.length - 1) {
            // Last section - only add submit button
            const submitButton = document.createElement('button');
            submitButton.type = 'submit';
            submitButton.className = 'btn btn-primary ms-auto';
            submitButton.innerHTML = 'Download Application';
            rightContainer.appendChild(submitButton);

        } else {
            // Not last section - add next button
            navigationButton = document.createElement('button');
            navigationButton.type = 'button';
            navigationButton.className = 'btn btn-primary';
            navigationButton.innerHTML = 'Next<i class="fas fa-arrow-right ms-2"></i>';
            
            if (index === 2) {
                // Special handling for step 3
                navigationButton.onclick = () => {
                    if (validateSection(index)) {
                        // Show the confirmation modal
                        const jobTitleModal = new bootstrap.Modal(document.getElementById('jobTitleModal'));
                        jobTitleModal.show();
                        // Set the pending navigation index
                        pendingNavigationIndex = index + 1;
                    }
                };
            } else {
                navigationButton.onclick = () => {
                    if (validateSection(index)) {
                        navigateSection(index + 1);
                    }
                };
            }
            rightContainer.appendChild(navigationButton);
        }

        navButtons.appendChild(leftContainer);
        navButtons.appendChild(rightContainer);
        
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
        const requiredFields = section.querySelectorAll('[required]:not([style*="display: none"])');
        const checkedRadioGroups = {};

        requiredFields.forEach(field => {
            if (field.type === 'radio') {
                const parent = field.closest('.radio-card-group') || field.parentNode;
                const name = field.name;
                if (!checkedRadioGroups[name]) {
                    const checkedRadio = section.querySelector(`input[name="${name}"]:checked`);
                    if (!checkedRadio) {
                        isValid = false;
                        // Add invalid class to all radios in the group
                        const radios = section.querySelectorAll(`input[name="${name}"]`);
                        radios.forEach(radio => radio.classList.add('is-invalid'));
                        // Create or update feedback message
                        let feedback = parent.querySelector('.invalid-feedback');
                        if (!feedback) {
                            feedback = document.createElement('div');
                            feedback.className = 'invalid-feedback d-block';
                            feedback.textContent = 'Please select an option.';
                            parent.appendChild(feedback);
                        }
                    } else {
                        // Remove invalid class from all radios in the group
                        const radios = section.querySelectorAll(`input[name="${name}"]`);
                        radios.forEach(radio => radio.classList.remove('is-invalid'));
                        const feedback = parent.querySelector('.invalid-feedback');
                        if (feedback) feedback.remove();
                    }
                    checkedRadioGroups[name] = true;
                }
            } else {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');

                    // Create or update feedback message
                    let feedback = field.nextElementSibling;
                    if (!feedback || !feedback.classList.contains('invalid-feedback')) {
                        feedback = document.createElement('div');
                        field.parentNode.appendChild(feedback);
                    }
                    feedback.className = 'invalid-feedback d-block';
                    feedback.textContent = 'This field is required';
                } else {
                    field.classList.remove('is-invalid');
                    const feedback = field.nextElementSibling;
                    if (feedback && feedback.classList.contains('invalid-feedback')) {
                        feedback.remove();
                    }
                }
            }
        });

        if (index === 4) {  // Step 5 (Passport Information)
            const passIssuePlaceField = section.querySelector('[name="pass_issue_place"]');
            if (passIssuePlaceField) {
                const inputValue = passIssuePlaceField.value.trim().toLowerCase();
                const stateFound = usStates.some(state => state.toLowerCase() === inputValue);
                if (stateFound) {
                    isValid = false;
                    // Show modal instead of alert
                    const modalBody = document.querySelector('#validationModal .modal-body');
                    modalBody.textContent = 'Please only enter the country of issue. Do NOT enter a state or province.';
                    const validationModal = new bootstrap.Modal(document.getElementById('validationModal'));
                    validationModal.show();
                    // Add error class and message
                    passIssuePlaceField.classList.add('is-invalid');
                    let feedback = passIssuePlaceField.nextElementSibling;
                    if (!feedback || !feedback.classList.contains('invalid-feedback')) {
                        feedback = document.createElement('div');
                        feedback.className = 'invalid-feedback d-block';
                        feedback.textContent = 'Please only enter the country of issue. Do NOT enter a state or province.';
                        passIssuePlaceField.parentNode.appendChild(feedback);
                    }
                } else {
                    // Remove error if previously added
                    passIssuePlaceField.classList.remove('is-invalid');
                    const feedback = passIssuePlaceField.nextElementSibling;
                    if (feedback && feedback.classList.contains('invalid-feedback')) {
                        feedback.remove();
                    }
                }
            }
        }
        
        console.log('Validation result:', isValid);
        return isValid;
    }
});
