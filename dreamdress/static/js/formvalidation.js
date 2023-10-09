const usernameInput = document.getElementById("username");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const confirmPasswordInput = document.getElementById("confirmpassword")

document.addEventListener("DOMContentLoaded", function(){
    console.log("Reched");
    const usernameInput = document.getElementById("username");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirmpassword");

    usernameInput.addEventListener("input", validateUsername);
    emailInput.addEventListener("input", validateEmail);
    passwordInput.addEventListener("input",validatePassword);
    confirmPasswordInput.addEventListener("input", validateConfirmPassword);
});

function validateUsername(){
    const regEx = /^[A-Za-z][A-Za-z0-9]*$/

    const usernameError = document.getElementById("usernameError");
    const username = usernameInput.value;

    if (!regEx.test(username)){
        usernameError.style.color="red";
        usernameError.textContent="Invalid Username";
    }else{
        //send ajax request
        fetch(`/check_username/?username=${username}`)
            .then(response => response.json())
            .then(data=> {
                if (data.exists){
                    usernameError.textContent = 'Username is already Taken';
                    usernameError.style.color = 'red';
                }
                else{
                    usernameError.textContent='';
                }
            })
            .catch(error => {
                console.error('Error:',error);
                //Handle the error here, e,g ,. show the error 
            });
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
        //send an ajax request
        fetch(`/check_email/?email=${email}`)
            .then(response => response.json())
            .then(data=> {
                if (data.exists){
                    emailError.textContent = 'Email is already Taken';
                    emailError.style.color = 'red';
                }
                else{
                    emailError.textContent='';
                }
            })
            .catch(error => {
                console.error('Error:',error);
                //Handle the error here, e,g ,. show the error 
            });
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
