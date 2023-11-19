document.getElementById('updateForm').addEventListener('submit', function(event) {
    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const email = document.getElementById('email').value.trim();
    const phoneNumber = document.getElementById('phoneNumber').value.trim();
    const profileImage = document.getElementById('profileImage').value.trim();

    // Validate First Name
    if (!/^[A-Za-z]+$/.test(firstName)) {
        document.getElementById('firstNameError').textContent = 'First Name should only contain letters';
        event.preventDefault();
    } else {
        document.getElementById('firstNameError').textContent = '';
    }

    // Validate Last Name
    if (!/^[A-Za-z]+$/.test(lastName)) {
        document.getElementById('lastNameError').textContent = 'Last Name should only contain letters';
        event.preventDefault();
    } else {
        document.getElementById('lastNameError').textContent = '';
    }

    // Validate Email
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        document.getElementById('emailError').textContent = 'Enter a valid email address';
        event.preventDefault();
    } else {
        document.getElementById('emailError').textContent = '';
    }

    // Validate Profile Image (check if it's an image file)
    const fileInput = document.getElementById('profileImage');
    const allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
    if (fileInput && !allowedExtensions.exec(profileImage)) {
        document.getElementById('profileImageError').textContent = 'Please upload an image file (jpg, jpeg, png, gif)';
        event.preventDefault();
    } else {
        document.getElementById('profileImageError').textContent = '';
    }

    // Validate Phone Number
    const phonePattern = /^(?!([\d])\1{9})\d{10}$/;
    if (!phonePattern.test(phoneNumber)) {
        document.getElementById('phoneNumberError').textContent = 'Phone Number should be 10 digits';
        event.preventDefault();
    } else {
        document.getElementById('phoneNumberError').textContent = '';
    }

    // Prevent form submission if any error messages exist
    const errorMessages = document.querySelectorAll('.text-danger');
    for (let i = 0; i < errorMessages.length; i++) {
        if (errorMessages[i].textContent !== '') {
            event.preventDefault();
            break;
        }
    }
});
