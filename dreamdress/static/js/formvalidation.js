const usernameInput = document.getElementById("username");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const confirmPasswordInput = document.getElementById("confirmpassword")

document.addEventListener("DOMContentLoaded", function(){
    console.log("Reched");
    usernameInput.addEventListener("input", validateUsername);
    emailInput.addEventListener("input", validateEmail);
    passwordInput.addEventListener("input",validatePassword);
    confirmPasswordInput.addEventListener("input", validateConfirmPassword);
})

function validateUsername(){
    const regEx = /^[A-Za-z][A-Za-z0-9]*$/

    const usernameError = document.getElementById("usernameError");
    const username = usernameInput.value;

    if (!regEx.test(username)){
        usernameError.style.color="red";
        usernameError.textContent="Invalid Username";
    }else{
        usernameError.textContent = "";
    }
}

function validateEmail(){
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


    const emailError = document.getElementById("emailError");
    const email = emailInput.value;

    if (!emailPattern.test(email)){
        emailError.style.color="red";
        emailError.textContent="Invalid Email";
    }else{
        emailError.textContent = "";
    }
}

function validatePassword(){
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+{}[\]:;<>,.?/~]).{8,}$/;

    const passwordError = document.getElementById("passwordError");
    const password = passwordInput.value;

    if (!passwordPattern.test(password)){
        // passwordError.style.color="red";
        passwordError.textContent="Invalid Password";
    }else{
        console.log("Correct");
        passwordError.textContent = "";
    }
} 

function validateConfirmPassword(){
    const confrimPasswordError = document.getElementById("confrimPasswordError");
    const password = passwordInput.value;
    const confirmpassword = confirmPasswordInput.value;

    if (confirmpassword != password){
        confrimPasswordError.style.color="red";
        confrimPasswordError.textContent="Invalid Password";
    }else{
        confrimPasswordError.textContent='';
    }
}