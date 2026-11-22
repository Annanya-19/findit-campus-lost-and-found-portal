/**
 * FindIt - Client-Side Registration Form Validation & Password Toggle
 * Validates: full_name, email, phone_number, password, confirm_password, termsCheck
 * Handled strictly via JavaScript.
 */

document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("registerForm");
  if (!registerForm) return;

  // Input elements
  const fullNameInput = document.getElementById("full_name");
  const emailInput = document.getElementById("email");
  const phoneInput = document.getElementById("phone_number");
  const passwordInput = document.getElementById("password");
  const confirmPasswordInput = document.getElementById("confirm_password");
  const termsCheckbox = document.getElementById("termsCheck");

  // Feedback & helper elements
  const strengthFill = document.getElementById("strengthFill");
  const strengthText = document.getElementById("strengthText");
  const confirmSuccessFeedback = document.getElementById("confirmPasswordSuccessFeedback");

  // Toggle visibility buttons
  const togglePasswordBtn = document.getElementById("togglePassword");
  const togglePasswordIcon = document.getElementById("togglePasswordIcon");
  const toggleConfirmPasswordBtn = document.getElementById("toggleConfirmPassword");
  const toggleConfirmPasswordIcon = document.getElementById("toggleConfirmPasswordIcon");

  // =========================================================================
  // 1. Password Visibility Toggle
  // =========================================================================
  function setupPasswordToggle(button, input, icon) {
    if (!button || !input || !icon) return;

    button.addEventListener("click", () => {
      const isPassword = input.getAttribute("type") === "password";
      input.setAttribute("type", isPassword ? "text" : "password");

      if (isPassword) {
        icon.classList.remove("bi-eye");
        icon.classList.add("bi-eye-slash");
        button.setAttribute("title", "Hide password");
      } else {
        icon.classList.remove("bi-eye-slash");
        icon.classList.add("bi-eye");
        button.setAttribute("title", "Show password");
      }
    });
  }

  setupPasswordToggle(togglePasswordBtn, passwordInput, togglePasswordIcon);
  setupPasswordToggle(toggleConfirmPasswordBtn, confirmPasswordInput, toggleConfirmPasswordIcon);

  // =========================================================================
  // 2. Individual Field Validation Helpers
  // =========================================================================

  // Full Name: at least 2 characters, letters and spaces
  function validateFullName() {
    if (!fullNameInput) return true;
    const value = fullNameInput.value.trim();
    const isValid = value.length >= 2;

    setFieldState(fullNameInput, isValid);
    return isValid;
  }

  // College Email: standard email format regex
  function validateEmail() {
    if (!emailInput) return true;
    const value = emailInput.value.trim();
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    const isValid = emailRegex.test(value);

    setFieldState(emailInput, isValid);
    return isValid;
  }

  // Phone Number: 10 digits
  function validatePhone() {
    if (!phoneInput) return true;
    const value = phoneInput.value.trim();
    const phoneRegex = /^[0-9]{10}$/;
    const isValid = phoneRegex.test(value);

    setFieldState(phoneInput, isValid);
    return isValid;
  }

  // Password: at least 6 characters + strength meter calculation
  function validatePassword() {
    if (!passwordInput) return true;
    const value = passwordInput.value;
    const isValid = value.length >= 6;

    setFieldState(passwordInput, isValid);
    updatePasswordStrength(value);

    // Recheck confirm password if already typed
    if (confirmPasswordInput && confirmPasswordInput.value.length > 0) {
      validateConfirmPassword();
    }

    return isValid;
  }

  // Password Strength Meter
  function updatePasswordStrength(password) {
    if (!strengthFill || !strengthText) return;

    if (password.length === 0) {
      strengthFill.className = "password-strength-fill";
      strengthFill.style.width = "0%";
      strengthText.textContent = "Min. 6 characters";
      strengthText.className = "small text-muted mt-1";
      return;
    }

    let score = 0;
    if (password.length >= 6) score++;
    if (password.length >= 8 && /[0-9]/.test(password)) score++;
    if (/[A-Z]/.test(password) && /[^A-Za-z0-9]/.test(password)) score++;

    if (score === 1) {
      strengthFill.className = "password-strength-fill strength-weak";
      strengthText.textContent = "Weak password";
      strengthText.className = "small text-danger mt-1";
    } else if (score === 2) {
      strengthFill.className = "password-strength-fill strength-medium";
      strengthText.textContent = "Medium password";
      strengthText.className = "small text-warning mt-1";
    } else if (score >= 3) {
      strengthFill.className = "password-strength-fill strength-strong";
      strengthText.textContent = "Strong password!";
      strengthText.className = "small text-success mt-1";
    }
  }

  // Confirm Password: strictly match Password
  function validateConfirmPassword() {
    if (!confirmPasswordInput || !passwordInput) return true;
    const password = passwordInput.value;
    const confirm = confirmPasswordInput.value;

    const isValid = confirm.length > 0 && confirm === password;

    if (isValid) {
      confirmPasswordInput.classList.remove("is-invalid");
      confirmPasswordInput.classList.add("is-valid");
      if (confirmSuccessFeedback) confirmSuccessFeedback.classList.add("d-block");
    } else {
      confirmPasswordInput.classList.remove("is-valid");
      confirmPasswordInput.classList.add("is-invalid");
      if (confirmSuccessFeedback) confirmSuccessFeedback.classList.remove("d-block");
    }

    return isValid;
  }

  // Terms acceptance checkbox
  function validateTerms() {
    if (!termsCheckbox) return true;
    const isValid = termsCheckbox.checked;
    setFieldState(termsCheckbox, isValid);
    return isValid;
  }

  // Utility to set Bootstrap validation classes
  function setFieldState(input, isValid) {
    if (isValid) {
      input.classList.remove("is-invalid");
      input.classList.add("is-valid");
    } else {
      input.classList.remove("is-valid");
      input.classList.add("is-invalid");
    }
  }

  // =========================================================================
  // 3. Real-time Event Listeners
  // =========================================================================
  if (fullNameInput) {
    fullNameInput.addEventListener("input", validateFullName);
    fullNameInput.addEventListener("blur", validateFullName);
  }

  if (emailInput) {
    emailInput.addEventListener("input", validateEmail);
    emailInput.addEventListener("blur", validateEmail);
  }

  if (phoneInput) {
    // Only allow digits in phone number field
    phoneInput.addEventListener("input", (e) => {
      phoneInput.value = phoneInput.value.replace(/\D/g, "");
      validatePhone();
    });
    phoneInput.addEventListener("blur", validatePhone);
  }

  if (passwordInput) {
    passwordInput.addEventListener("input", validatePassword);
    passwordInput.addEventListener("blur", validatePassword);
  }

  if (confirmPasswordInput) {
    confirmPasswordInput.addEventListener("input", validateConfirmPassword);
    confirmPasswordInput.addEventListener("blur", validateConfirmPassword);
  }

  if (termsCheckbox) {
    termsCheckbox.addEventListener("change", validateTerms);
  }

  // =========================================================================
  // 4. Form Submit Guard
  // =========================================================================
 
  // =========================================================================
  // 4. Form Validation and API Submission
  // =========================================================================
  
registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const isFormValid =
        validateFullName() &&
        validateEmail() &&
        validatePhone() &&
        validatePassword() &&
        validateConfirmPassword() &&
        validateTerms();

    if (!isFormValid) {
        const firstInvalid = registerForm.querySelector(".is-invalid");
        if (firstInvalid) firstInvalid.focus();
        return;
    }

    const submitBtn = document.getElementById("registerSubmitBtn");
    const originalText = submitBtn.innerHTML;

    submitBtn.disabled = true;
    submitBtn.textContent = "Creating account...";

    try {
        const formData = new FormData(registerForm);

        const response = await fetch("/api/register", {
            method: "POST",
            body: formData,
            credentials: "same-origin"
        });

        const result = await response.json();

        if (result.success) {
            alert("Registration successful! Please log in.");
            window.location.href = "/login";
        } else {
            alert(result.message || "Registration failed. Please try again.");
        }

    } catch (error) {
        alert("Unable to connect to the server. Please try again.");
        console.error(error);
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
});

});