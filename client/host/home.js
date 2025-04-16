// Get the div that holds all managed campgrounds
let managedCampground = document.querySelector("#managed-campgrounds");
let newCampgroundForm = document.querySelector("#new-campground-form");

// Execute a click command to locate all campgrounds managed by the current user.
const host = JSON.parse(localStorage.getItem("host"));
if (host && host.id) {
    fetch(`http://127.0.0.1:5000/campgrounds/${host.id}`, {
        method: 'GET',
        headers: {'Content-Type': 'application/json'},
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status ${response.status}`);
        }
        return response.json(); // convert response to JSON
    })
    .then(data => {
        if (data.campgrounds && data.campgrounds.length > 0) {
            managedCampground.innerHTML = ""; // Clear previous content
            
            data.campgrounds.forEach(campground => {
                let id = campground[0];
                let cg = document.createElement("div");
                cg.classList.add("campground-item");

                // Add the name, address, and description to the campground
                let cgname = document.createElement("h2");
                cgname.innerHTML = campground[1];
                cg.appendChild(cgname);

                let cgaddr = document.createElement("h3");
                cgaddr.innerHTML = campground[3];
                cg.appendChild(cgaddr);

                let cgdesc = document.createElement("p");
                cgdesc.innerHTML = campground[4];
                cg.appendChild(cgdesc);

                // Footer - Holds buttons
                let footer = document.createElement("footer");
                cg.appendChild(footer);

                // Edit button
                let editButton = document.createElement("button");
                editButton.className = "campground-edit-button"
                editButton.textContent = "Edit";
                editButton.addEventListener('click', () => editCampground(id, cg));

                // Delete button
                let deleteButton = document.createElement("button");
                deleteButton.className = "campground-delete-button";
                deleteButton.textContent = "Delete";
                deleteButton.addEventListener('click', () => deleteCampground(id));

                // Edit Desccription Textarea
                let descriptionEdit = document.createElement("textarea");
                descriptionEdit.className = "campground-description-edit-textarea";

                footer.appendChild(editButton);
                footer.appendChild(deleteButton);
                cg.appendChild(descriptionEdit);
                managedCampground.appendChild(cg);
            });
        } else {
            managedCampground.innerHTML = "<p>No matching campgrounds found</p>";
        }
    })
    .catch(error => {
        console.error("Fetch error:", error);
    });

    fetch('http://127.0.0.1:5000/getmreservations', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(host)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status ${response.status}`);
        }
        return response.json(); // Convert response to json
    })
    .then(data => {
        let managedReservations = document.querySelector("#managed-reservations");
        if (data.reservations && data.reservations.length > 0) {
            (data.reservations);
            managedReservations.innerHTML = ""; // Clear the content of the reservations box

            // Create the divs for reservations and populate the screen.
            data.reservations.forEach(reservation => {
                let startDate = reservation[0];
                let endDate = reservation[1];
                let guestEmail = reservation[2];
                let cgName = reservation[3];

                let reservationItem = document.createElement("div");
                reservationItem.className = "reservation-item";
                let resDates = document.createElement("h2");
                resDates.innerHTML = startDate + " - " + endDate;
                reservationItem.appendChild(resDates);

                let guestName = document.createElement("h3");
                guestName.innerHTML = guestEmail;
                reservationItem.appendChild(guestName);

                let campgroundName = document.createElement("h3");
                campgroundName.innerHTML = cgName;
                reservationItem.appendChild(campgroundName)

                managedReservations.appendChild(reservationItem);
            })
        }
    })
    .catch(error => {
        console.error("Fetch error:", error);
    })
}

newCampgroundForm.addEventListener("submit", function (event) {
    event.preventDefault();

    // Get form data
    let name = document.getElementById("name").value;
    let address = document.getElementById("address").value;
    let description = document.getElementById("description").value;

    let formData = {
        "name": name,
        "address": address,
        "description": description,
        "host_id": host.id
    };

    // Apply fetch request
    fetch("http://127.0.0.1:5000/campgrounds", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Optional: do something with `data`
        console.log("Campground created:", data);
        // Refresh the page after everything completes
        location.reload();
    })
    .catch(error => {
        console.error("Error submitting campground:", error);
        // Optional: show user an error message here
    });
});


function editCampground(id, cg_item) {
    let cg_edit_textarea = cg_item.querySelector(".campground-description-edit-textarea");
    cg_edit_textarea.style.display = "block";
    cg_edit_textarea.value = cg_item.querySelector('p').innerHTML;
    
    let confirmationButton = document.createElement('button');
    confirmationButton.className = "confirmation-button";
    confirmationButton.innerText = "Confirm";
    cg_item.appendChild(confirmationButton);

    confirmationButton.addEventListener('click', () => finalizeCGEdit(id, cg_edit_textarea, confirmationButton));
}

function finalizeCGEdit(cg_id, textArea, confirmationButton) {
    fetch(`http://127.0.0.1:5000/campgrounds/${cg_id}`, {
        method : 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({description : textArea.value})
    })
    .then(response => response.json())
    .then(data => {        
        // Hide the text area
        textArea.style.display = "none";
        confirmationButton.remove()
    })
    .catch(error => console.error("Error: ", error));
}

function deleteCampground(id) {
    // Ask the user for confirmation
    const confirmation = window.confirm("Are you sure you want to delete this campground? This action cannot be undone.");
    
    // If the user confirms, proceed with the deletion
    if (confirmation) {
        fetch(`http://127.0.0.1:5000/campgrounds/${id}`, {
            method: 'DELETE',
            headers: {'Content-Type' : 'application/json'},
        })
        .then(response => response.json())
        .then(data => console.log("Deletion success:", data))  // Log success message
        .catch(error => console.error('Error:', error));  // Log error if occurs
    } else {
        console.log("Deletion cancelled.");
    }
}
