let login = document.querySelector("#login-form");
let loginType = 'guest';

// const toggleSwitch = document.getElementById('toggleLogin');
        // const loginTitle = document.getElementById('login-title');

        toggleSwitch.addEventListener('change', () => {
            if (toggleSwitch.checked) {
                loginTitle.textContent = 'Host Login';
                loginType = 'host';
            } else {
                loginTitle.textContent = 'Guest Login';
                loginType = 'guest';
            }
        });

login.addEventListener('submit', function (event) {
    event.preventDefault(); // keep the page from refreshing

    // Get the values input
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (loginType == "guest") {
        const guestData = {email, password};

        fetch('http://127.0.0.1:5000/loginguest', {
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(guestData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status ${response.status}`);
            }
            // console.log(response.json(), response.status)
            return response.json();
        })
        .then(data => {

            if (data.guest) {
                // Store local info and redirect
                localStorage.setItem("guest", JSON.stringify(data.guest));
                window.location.href = "../guest/index.html";
            } else {
                console.error("Login failed:", data.error);
            }
        })
        .catch(error => {
            let errorBox = document.querySelector("#error-box");
            errorBox.innerHTML = "Invalid credentials! Email and password were incorrect.";
            errorBox.style.display = "block";
            console.error('Error:', error)
        });
        
    } else if (loginType == "host") {
        const hostData = {email, password};

        fetch('http://127.0.0.1:5000/loginhost', {
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(hostData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status ${response.status}`);
            }
            // console.log(response.json(), response.status)
            return response.json();
        })
        .then(data => {

            if (data.host) {
                // Store local info and redirect
                localStorage.setItem("host", JSON.stringify(data.host));
                window.location.href = "../host/index.html";
            } else {
                console.error("Login failed:", data.error);
                alert("Error : email or password could not be found!");
            }
        })
        .catch(error => console.error('Error:', error));
    }
})