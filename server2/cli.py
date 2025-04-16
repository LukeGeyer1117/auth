#!/usr/bin/env python3

import click, os, sqlite3, sys
from datetime import datetime

DB_FILE = "mydb.db"

# getdb
def getdb(create=False):
    if os.path.exists(DB_FILE):
        if create:
            os.remove(DB_FILE)
    else:
        if not create:
            print("no database found")
            sys.exit(1)
    con = sqlite3.connect(DB_FILE)
    con.execute('PRAGMA foreign_keys = ON')
    return con

@click.group()
def cli():
    pass

# Create new guest
@click.command()
@click.argument('username')
@click.argument('first_name')
@click.argument('last_name')
@click.argument('password')
@click.argument('email')
def addguest(username: str, first_name: str, last_name: str, password: str, email: str):
    try:
        with getdb() as con:
            cursor = con.cursor()
            cursor.execute('''INSERT INTO guests (username, first_name, last_name, password, email) VALUES (?, ?, ?, ?, ?)''', (username, first_name, last_name, password, email))
            con.commit()
            # print(f'Created guest {username} with email {email}, password {"*"*len(password)}')
            return
    except sqlite3.Error as e:
        print(f'An error occured creating user : {e}')

# Create new host
@click.command()
@click.argument('username')
@click.argument('first_name')
@click.argument('last_name')
@click.argument('password')
@click.argument('email')
def addhost(username: str, first_name: str, last_name: str, password: str, email: str):
    try:
        with getdb() as con:
            cursor = con.cursor()
            cursor.execute('''INSERT INTO hosts (username, first_name, last_name, password, email) VALUES (?, ?, ?, ?, ?)''', (username, first_name, last_name, password, email))
            con.commit()
            return
    except sqlite3.Error as e:
        print(f'An error occured creating user : {e}')

# create a new campground
@click.command(name="addCampground")
@click.argument('name', type=str)
@click.argument('host_id', type=str)
@click.argument('street_address', type=str)
@click.argument('description', type=str)
def addCampground(name: str, host_id: str, street_address: str, description: str):
    try:
        with getdb() as con:
            cursor = con.cursor()
            cursor.execute('''INSERT INTO campground (name, host_id, street_address, description) VALUES (?, ?, ?, ?)''', (name, int(host_id), street_address, description))
            con.commit()
            # print(f'Created campground {name}, hosted by host {host_id}, created with id={row_id}')
            return True
    except sqlite3.Error as e:
        print(f'An error occured creating campground : {e}')
        return False
    
@click.command(name="deleteCampground")
@click.argument('c_id', type=str)
def deleteCampground(c_id: str):
    try:
        with getdb() as con:
            cursor = con.cursor()
            cursor.execute('''SELECT * from campground where id = ?''', (int(c_id),))
            record = cursor.fetchone()
            if record ==  None:
                print("no campground found to delete!")
                return False
            cursor.execute('''PRAGMA foreign_keys = ON;''')
            cursor.execute('''DELETE from campground where id=?''', (int(c_id),))
            con.commit()
            return 200
    except sqlite3.Error as e:
        print(f'An error occurred deleting a campgorund : {e}')
        return False
    
@click.command(name="editCampground")
@click.argument('c_id', type=str)
@click.argument('description', type=str)
def editCampground(c_id: str, description: str):
    try:
        with getdb() as con:
            cursor = con.cursor()
            print(f"Executing query: UPDATE campground SET description = {description} WHERE id = {c_id} with params: ({description})")
            cursor.execute('''UPDATE campground SET description = ? WHERE id = ?''', (description, int(c_id)))
            con.commit()
            return True
    except sqlite3.Error as e:
        print(f'An error occured editing a campground description : {e}')
        return False

# create a new campsite
@click.command(name="addCampsite")
@click.argument('campground_id')
def addCampsite(campground_id: int):
    try:
        with getdb() as con:
            cursor = con.cursor()
            # find out how many campsites are registered to the current campground
            cursor.execute('''SELECT * from campsite where c_id = ?''', (campground_id,))
            records = cursor.fetchall()
            # assign the campsite an id equal to current sites + 1
            campsite_id = len(records) + 1
            # insert the site into the sites table
            cursor.execute('''INSERT INTO campsite (id, c_id) VALUES (?, ?)''', (campsite_id, campground_id))
            con.commit()
            # print(f'Created campsite on campground with id={campground_id}, inserted with id={campsite_id}')
            return
    except sqlite3.Error as e:
        print(f'Error creating campsite : {e}')

# create a reservation
@click.command(name="addReservation")
@click.argument('guest_id')
@click.argument('campground_id')
@click.argument('campsite_id')
@click.argument('start_date')
@click.argument('end_date')
def addReservation(guest_id: int, campground_id: int, campsite_id: int, start_date: str, end_date: str):
    # create date objects for given start and end dates
    start_date_object, end_date_object = datetime.strptime(start_date, '%m/%d/%Y'), datetime.strptime(end_date, '%m/%d/%Y')
    start_date_only, end_date_only = start_date_object.date(), end_date_object.date()
    try:
        with getdb() as con:
            cursor = con.cursor()
            # Find all reservations to the same site
            cursor.execute('''SELECT * FROM reservation where campground_id = ? AND campsite_id = ?''', (campground_id, campsite_id))
            record = cursor.fetchall()
            # make sure there is no overlap in dates
            for r in record:
                r_start, r_end = r[-2], r[-1]
                r_start_date_object, r_end_date_object = datetime.strptime(r_start, '%m/%d/%Y'), datetime.strptime(r_end, '%m/%d/%Y')
                r_start_date_only, r_end_date_only = r_start_date_object.date(), r_end_date_object.date()
                if check_overlap(start_date_only, end_date_only, r_start_date_only, r_end_date_only):
                    print(f'Guest {guest_id} reservation for cg {campground_id} sn {campsite_id} could not be completed due to reservation overlap.')
                    return False
            cursor.execute('''
                    INSERT INTO reservation (guest_id, campground_id, campsite_id, start_date, end_date) VALUES (?, ?, ?, ?, ?)
                    ''', (guest_id, campsite_id, campground_id, start_date, end_date))
            con.commit()
            # print(f'Created reservation for guest {guest_id} at campground {campground_id} site {campsite_id}, dates : {start_date} - {end_date}')
            return True
    except sqlite3.Error as e:
        print(f'Error creating reservation : {e}')


def check_overlap(start1, end1, start2, end2):
    return start1 <= end2 and start2 <= end1

@click.command(name="findHost")
@click.argument('email')
def findHost(email: str):
    try:
        with getdb() as con:
            cursor = con.cursor()
            # Find the host with the given email and password
            cursor.execute('''SELECT * from hosts where email = ?''', (email,))
            try:
                record = cursor.fetchone()
                return record
            except:
                print(f'Cannot find account, username/password combination is not associated with a user.')
                return False
    except Exception as e:
        print(f'Error finding guest : {e}')

@click.command(name="findGuest")
@click.argument('email')
def findGuest(email: str):
    try:
        with getdb() as con:
            cursor = con.cursor()
            # Find the guest with the given email and password
            cursor.execute('''SELECT * from guests where email = ?''', (email,))
            try:
                record = cursor.fetchone()
                return record
            except:
                print(f'Cannot find account, username/password combination is not associated with a user.')
                return False
    except Exception as e:
        print(f'Error finding guest : {e}')

@click.command(name="getcampgrounds")
@click.argument('id')
def getcampgrounds(id : int):
    try:
        with getdb() as con:
            cursor = con.cursor()
            # Find the campgrounds with host id
            cursor.execute('''SELECT * from campground where host_id = ?''', (id,))
            records = cursor.fetchall()
            return records
    except Exception as e:
        print(f'Error finding campgrounds : {e}')

@click.command(name="getmreservations")
@click.argument("id")
def getmreservations(id : str):
    try:
        with getdb() as con:
            cursor = con.cursor()
            # Find all reservations owned by the host id
            cursor.execute('''select r.start_date, r.end_date, g.email, c.name 
                            from reservation r join campground c on r.campground_id = c.id 
                           JOIN guests g on r.guest_id = g.id WHERE c.host_id = ?''', (int(id),))
            records = cursor.fetchall()
            return records
    except Exception as e:
        print(f'Error finding reservations : {e}')

@click.command(name="checkEmail")
@click.argument("email")
def checkEmail(email : str):
    try:
        with getdb() as con:
            cursor = con.cursor()
            # Find all accounts with email = email
            cursor.execute('''select * from hosts where email = ?''', (email,))
            records_hosts = cursor.fetchall()
            cursor.execute('''select * from guests where email = ?''', (email,))
            records_guests = cursor.fetchall()
            if records_hosts or records_guests:
                return False
            return True
    except Exception as e:
        print(f'Error checking email : {e}')

# add commands
cli.add_command(addguest)
cli.add_command(addhost)
cli.add_command(addCampground)
cli.add_command(deleteCampground)
cli.add_command(editCampground)
cli.add_command(addCampsite)
cli.add_command(addReservation)
cli.add_command(findHost)
cli.add_command(findGuest)
cli.add_command(getcampgrounds)
cli.add_command(getmreservations)
cli.add_command(checkEmail)

if __name__ == "__main__":
    cli()   