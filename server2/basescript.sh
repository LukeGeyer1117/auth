#!/bin/bash

# Remove existing database file if it exists
rm -f mydb.db

# Create a new database and apply schema
sqlite3 mydb.db < schema.sql && sleep 1

# Print success message
echo "Database setup complete!"

# test adding a guest
# CMD   addguest
# ARGS {username} {password} {email}
# python3 -m cli addguest "Guest" "luke" "geyer" "guest" "guest@mail.com"

# test adding a host
# CMD   addhost
# ARGS {username} {password} {email}
# python3 -m cli addhost "host" "gwynnan" "cartmel" "host" "host@mail.com"


# test adding a campground
# CMD   addCampground
# ARGS {name} {host_id} {street_address}
# python3 -m cli addCampground "Hailstone - Upper Fisher Campground" 1 "Jordanelle State Park" "Hailstone - Upper Fisher Campground, near Heber City, Utah, is a fantastic spot for those looking to enjoy the great outdoors with a touch of comfort. This campground offers a mix of tent sites, RV accommodations, and even cabins, making it a versatile choice for all types of campers."
# python3 -m cli addCampground "Granite Flat (utah)" 1 "Uinta National Forest" "Granite Flat, near Provo, Utah, is a scenic campground tucked away in the Uinta-Wasatch-Cache National Forest. This spot is surrounded by towering pine trees and offers a refreshing escape with clean, cool air, making it a favorite for those looking to unwind in nature."

# test adding a campsite
# CMD   addCampsite
# ARGS {campground_id}
# python3 -m cli addCampsite 1
# python3 -m cli addCampsite 1
# python3 -m cli addCampsite 2
# python3 -m cli addCampsite 2
# python3 -m cli addCampsite 2

# Test building a reservation
# CMD addReservation
# ARGS {guest_id} {campground_id} {campsite_id} {start_date} {end_date}

# python3 -m cli addReservation 1 1 1 "11/09/2025" "12/01/2025"
# python3 -m cli addReservation 1 2 2 "8/15/2025" "8/22/2025"
# python3 -m cli addReservation 1 1 2 "4/29/2025" "5/05/2025"

