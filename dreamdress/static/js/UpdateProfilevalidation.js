document.addEventListener("DOMContentLoaded", function(){
    const firstNameInput = document.getElementById("firstName");
    const lastNameInput = document.getElementById("lastName");
    const phoneNumberInput = document.getElementById("phoneNumber");

    firstNameInput.addEventListener("input", validateFirstName);
    lastNameInput.addEventListener("input", validateLastName);
    phoneNumberInput.addEventListener("input", validatePhoneNumber);

    updateForm.addEventListener("submit", function(e) {
        // Clear existing error messages before re-validating
        const firstNameError = document.getElementById("firstNameError");
        const lastNameError = document.getElementById("lastNameError");
        const phoneNumberError = document.getElementById("phoneNumberError");

        firstNameError.textContent = '';
        lastNameError.textContent = '';
        phoneNumberError.textContent = '';

        validateFirstName();
        validateLastName();
        validatePhoneNumber();

        if (firstNameError.textContent || lastNameError.textContent || phoneNumberError.textContent) {
            e.preventDefault(); // Prevent form submission if there are errors
        }
    });
});

function validateFirstName() {
    const regEx = /^[A-Za-z][A-Za-z\s]*$/;
    const firstNameError = document.getElementById("firstNameError");
    const firstName = firstNameInput.value.trim();

    if (!regEx.test(firstName)) {
        firstNameError.style.color = "red";
        firstNameError.textContent = "First name should start with a letter and contain only letters or spaces!";
    } else {
        firstNameError.textContent = "";
    }
}

function validateLastName() {
    const regEx = /^[A-Za-z]+$/;
    const lastNameError = document.getElementById("lastNameError");
    const lastName = lastNameInput.value.trim();

    if (!regEx.test(lastName)) {
        lastNameError.style.color = "red";
        lastNameError.textContent = "Last name should contain only letters!";
    } else {
        lastNameError.textContent = "";
    }
}

function validatePhoneNumber() {
    const phoneNumberError = document.getElementById("phoneNumberError");
    const phoneNumber = phoneNumberInput.value.trim();

    if (!/^\d{10}$/.test(phoneNumber) || /^(.)\1+$/.test(phoneNumber)) {
        phoneNumberError.style.color = "red";
        phoneNumberError.textContent = "Phone number must be 10 digits and not all digits should be the same!";
    } else {
        phoneNumberError.textContent = "";
    }
}
