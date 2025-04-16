# Campsite Reservation App

## Resources

**guests**

Attributes:

* id (integer)
* username (string)
* password (string)
* email (string)

  ## Schema
  ```sql
  CREATE TABLE guests (
    id INTEGER PRIMARY KEY UNIQUE,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
  );```

**hosts**

Attributes:

* id (integer)
* username (string)
* password (string)
* email (string)

  ## Schema
  ```sql
  CREATE TABLE hosts (
    id INTEGER PRIMARY KEY UNIQUE,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
  );```

**reservation**

Attributes:

* id (integer)
* guest_id (integer)
* campground_id (integer)
* campsite_id (integer)
* start_date (string)
* end_date (string)

## Schema

```sql
CREATE TABLE reservation (
    id INTEGER PRIMARY KEY UNIQUE,
    guest_id INTEGER NOT NULL,
    campground_id INTEGER NOT NULL,
    campsite_id INTEGER NOT NULL,
    start_date TEXT,
    end_date TEXT, 

    FOREIGN KEY (guest_id) REFERENCES guests(id),
    FOREIGN KEY (campsite_id, campground_id) REFERENCES campsite(id, c_id) ON DELETE CASCADE,
    FOREIGN KEY (campground_id) REFERENCES campground(id) ON DELETE CASCADE
);
```
**campground**

* id (integer)
* name (text)
* host_id (integer)
* street_address (text)
* description (text)

## Schema
```sql
CREATE TABLE campground (
    id INTEGER PRIMARY KEY,
    name TEXT,
    host_id INTEGER,
    street_address TEXT,
    description TEXT,

    FOREIGN KEY (host_id) REFERENCES hosts(id)
);
```

**campsite**

* id (integer)
* c_id (integer)

## Schema
```sql
CREATE TABLE campsite (
    id INTEGER,
    c_id INTEGER,

    PRIMARY KEY (id, c_id),
    FOREIGN KEY (c_id) REFERENCES campground(id) ON DELETE CASCADE
);
```

## REST Endpoints

Name                           | Method | Path
-------------------------------|--------|------------------
Add a new guest member         | POST   | /addguest
Add a new host member          | POST   | /addhost
Login a guest member           | POST   | /loginguest
Login a host member            | POST   | /loginhost
Add a new campground           | POST   | /campgrounds
Get an existing campground     | GET    | /campgrounds/<int: c_id>
Edit a campground description  | PUT    | /campgrounds/<int: c_id>
Delete an existing campground  | DELETE | /campgrounds/<int: c_id>
Add a campsite to a campground | POST   | /campsites




# auth_project
# auth
# auth
# auth
# auth
# auth
