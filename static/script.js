function validateInput(inputElement) {
    if (inputElement.value === '' || inputElement.value === null) {
        inputElement.style.backgroundColor = '#ffb3b3';
        inputElement.style.border = '1px solid red';
        return false;
    }
    return true;
}

var emailreg = /^([a-zA-Z0-9\._]+)@([a-zA-Z0-9])+.([a-z]+)(.[a-z]+)?$/

function validateSign() {
    var username = document.getElementById('username');
    var email = document.getElementById('email');
    var pass = document.getElementById('pass');
    var cpass = document.getElementById('cpass');
    var checkbox = document.getElementById('agreement');

    if (!validateInput(username)) return false;
    if (!validateInput(email) || !emailreg.test(email.value)) return false;
    if (!validateInput(pass)) return false;
    if (!validateInput(cpass) || cpass.value !== pass.value) return false;

    if (!checkbox.checked) {
        alert("Please agree to the terms and conditions.");
        return false;
    }

    return true;
}

function validateLogin() {
    var email = document.getElementById('email');
    var password = document.getElementById('password');

    if(!validateInput(email) || !emailreg.test(email.value)) return false;
    if(!validateInput(password)) return false;

    return true;
}