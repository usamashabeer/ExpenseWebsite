var usernameField = document.querySelector('#UnameField');
var feedbackArea = document.querySelector('.invalid-feedback');
var emailFeedbackArea = document.querySelector('.email-invalid-feedback');
var usernameSuccessOutput = document.querySelector('.usernameSuccessOutput');
var emailField = document.querySelector('#emailField');
var passordField = document.querySelector('#passwordField');
var showPWD = document.querySelector('.showPWD');
var submitBtn = document.querySelector('.submit-btn');



const handleToggleInput = (e) => {

    if (showPWD.textContent === 'Show') {
        showPWD.textContent = 'Hide';
        passordField.setAttribute('type', 'text');
    } else {
        passordField.setAttribute('type', 'password');

        showPWD.textContent = 'Show';
    }
};
showPWD.addEventListener('click', handleToggleInput);

// this add eventlistner show the event occur on the field
usernameField.addEventListener('keyup', (e) => {

    // usernameval contain the value which enter in field of #UnameFiel
    const usernameval = e.target.value;

    usernameSuccessOutput.textContent = 'Checking'
    usernameField.classList.remove('is-valid');
    if (usernameval.length > 0) {
        usernameField.classList.remove('is-invalid');
        feedbackArea.style.display = 'none';
        fetch('/authentication/username-validate', {
                body: JSON.stringify({ username: usernameval }),
                method: 'POST',
            })
            .then((res) => res.json())
            .then((data) => {
                usernameSuccessOutput.style.display = 'none';
                console.log('data', data.username_valid);
                if (data.username_error) {
                    console.log('usernmae wrong');
                    // submitBtn.setAttribute('disabled', 'disabled');
                    submitBtn.disabled = true;
                    usernameField.classList.add('is-invalid');

                } else {
                    submitBtn.removeAttribute('disabled');
                    usernameField.classList.add('is-valid');
                }
            });
    }
});
emailField.addEventListener('keyup', (e) => {
    const emailval = e.target.value;
    emailField.classList.remove('is-valid');
    if (emailval.length > 0) {
        feedbackArea.style.display = 'none';
        emailField.classList.remove('is-invalid');
        fetch('/authentication/email-validate', {
                body: JSON.stringify({
                    email: emailval
                }),
                method: 'POST'
            }).then((res) => res.json())
            .then((data) => {
                if (data.email_error) {
                    submitBtn.disabled = true;
                    emailField.classList.add('is-invalid');

                } else {
                    submitBtn.removeAttribute('disabled');
                    emailField.classList.add('is-valid');
                }
            });
    }
});