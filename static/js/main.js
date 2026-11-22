/**
 * FindIt - Main Global UI Script
 * Handles navigation states, alerts auto-dismiss, file upload preview, and form helpers.
 */

document.addEventListener("DOMContentLoaded", () => {
  // 1. Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll(".alert.alert-dismissible");
  alerts.forEach((alert) => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });

  // 2. Image upload preview for report-item.html
  const imageInput = document.getElementById("image");
  const imagePreview = document.getElementById("imagePreview");
  const placeholderPreview = document.getElementById("placeholderPreview");
  const removeImageBtn = document.getElementById("removeImageBtn");

  if (imageInput && imagePreview) {
    imageInput.addEventListener("change", function () {
      const file = this.files[0];
      if (file) {
        // Validate file size (< 5MB)
        if (file.size > 5 * 1024 * 1024) {
          alert("Image file size should be less than 5MB.");
          this.value = "";
          return;
        }

        const reader = new FileReader();
        reader.onload = function (e) {
          imagePreview.src = e.target.result;
          imagePreview.classList.remove("d-none");
          if (placeholderPreview) placeholderPreview.classList.add("d-none");
          if (removeImageBtn) removeImageBtn.classList.remove("d-none");
        };
        reader.readAsDataURL(file);
      } else {
        imagePreview.src = "";
        imagePreview.classList.add("d-none");
        if (placeholderPreview) placeholderPreview.classList.remove("d-none");
        if (removeImageBtn) removeImageBtn.classList.add("d-none");
      }
    });

    if (removeImageBtn) {
      removeImageBtn.addEventListener("click", () => {
        imageInput.value = "";
        imagePreview.src = "";
        imagePreview.classList.add("d-none");
        if (placeholderPreview) placeholderPreview.classList.remove("d-none");
        removeImageBtn.classList.add("d-none");
      });
    }
  }

  // 3. Dynamic labels when toggling Lost vs Found in report-item.html
  const lostRadio = document.getElementById("typeLost");
  const foundRadio = document.getElementById("typeFound");
  const dateLabel = document.getElementById("dateLabel");
  const locationLabel = document.getElementById("locationLabel");
  const locationHelp = document.getElementById("locationHelp");

  function updateFormTypeHelpers() {
    if (!lostRadio || !foundRadio) return;
    if (lostRadio.checked) {
      if (dateLabel) dateLabel.textContent = "Date Lost";
      if (locationLabel) locationLabel.textContent = "Location where you lost it";
      if (locationHelp) locationHelp.textContent = "E.g., Central Library 2nd Floor, Room 302, Cafeteria";
    } else {
      if (dateLabel) dateLabel.textContent = "Date Found";
      if (locationLabel) locationLabel.textContent = "Location where you found it";
      if (locationHelp) locationHelp.textContent = "E.g., Near Auditorium Gate, Sports Complex Bench (mention if submitted to Security)";
    }
  }

  if (lostRadio && foundRadio) {
    lostRadio.addEventListener("change", updateFormTypeHelpers);
    foundRadio.addEventListener("change", updateFormTypeHelpers);
    updateFormTypeHelpers();
  }

  // 4. Highlight active navigation link based on current path
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll(".navbar-nav .nav-link");
  navLinks.forEach((link) => {
    const href = link.getAttribute("href");
    if (href && (currentPath.endsWith(href) || currentPath === href)) {
      link.classList.add("active");
    }
  });

  // 5. Global password toggle helper (for login & other pages)
  const toggleButtons = document.querySelectorAll("[data-toggle='password']");
  toggleButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-target") || "password";
      const targetInput = document.getElementById(targetId);
      const icon = btn.querySelector("i");
      if (!targetInput) return;
      const isPassword = targetInput.getAttribute("type") === "password";
      targetInput.setAttribute("type", isPassword ? "text" : "password");
      if (icon) {
        icon.classList.toggle("bi-eye", !isPassword);
        icon.classList.toggle("bi-eye-slash", isPassword);
      }
      btn.setAttribute("title", isPassword ? "Hide password" : "Show password");
    });
  });
});
