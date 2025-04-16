let signup = document.querySelector("#login-form");
let signupType = 'guest';

const toggleSwitch = document.getElementById('toggleLogin');
        const loginTitle = document.getElementById('login-title');
        const usernameInput = document.getElementById('username');

        toggleSwitch.addEventListener('change', () => {
            if (toggleSwitch.checked) {
                loginTitle.textContent = 'Host Signup';
                usernameInput.placeholder = 'Host Username';
                signupType = 'host';
            } else {
                loginTitle.textContent = 'Guest Signup';
                usernameInput.placeholder = 'Guest Username';
                signupType = 'guest';
            }
        });

signup.addEventListener('submit', function (event) {
    event.preventDefault(); // keep the page from refreshing

    // Get the values input
    const username = document.getElementById("username").value;
    const f_name = document.getElementById("f_name").value;
    const l_name = document.getElementById("l_name").value;
    const password = document.getElementById("password").value;
    const email = document.getElementById("email").value;

    if (!validateEmail(email)) {
        let signupEmailErrorBox = document.querySelector("#signup-email-error-box");
        signupEmailErrorBox.style.display = "block";
        signupEmailErrorBox.innerHTML = "Invalid email. Check your email and try again.";
        return;
    }
    let [message, validPassword] = validatePassword(password);
    console.log(message);
    if (!validPassword) {
        let signupPasswordEmailBox = document.querySelector("#signup-password-error-box");
        signupPasswordEmailBox.style.display = "block";
        signupPasswordEmailBox.innerHTML = message;
        return;
    }


    if (signupType == "guest") {
        const guestData = {username, f_name, l_name, password, email};

        fetch('http://127.0.0.1:5000/addguest', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(guestData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status ${response.status}`);
            }
            return response.json();
        })
        .then(data => console.log("Server Response:", data))
        .catch(error => console.error('Error:', error));
        
    } else if (signupType == "host") {
        const hostData = {username, f_name, l_name, password, email};

        fetch('http://127.0.0.1:5000/addhost', {
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(hostData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Server Response:", data)
            window.location.href = "index.html";
        })
        .catch(error => console.error('Error:', error));
    }
})

function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (checkEmailUnique(email)) {
        return emailRegex.test(email);
    }
}

function validatePassword(password) {
    let length = false;
    let message = "";
    if (password.length > 15) {
        length = true;
    } else {
        let msg = "Password must contain at least 15 characters.\n"
        message += msg;
    }

    if (length) {
        return [message,true];
    } else {
        return [message, false];
    }

}

function checkEmailUnique(email) {
    fetch('http://127.0.0.1:5000/email', {
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(hostData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status ${response.status}`)
        }
        return response.json();
    })
    .then(data => {
        console.log("Server response : ", data);
    })
}