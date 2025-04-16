CREATE TABLE guests (
    id INTEGER PRIMARY KEY UNIQUE,
    username TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE hosts (
    id INTEGER PRIMARY KEY UNIQUE,
    username TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
);

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

CREATE TABLE campground (
    id INTEGER PRIMARY KEY,
    name TEXT,
    host_id INTEGER,
    street_address TEXT,
    description TEXT,

    FOREIGN KEY (host_id) REFERENCES hosts(id)
);

CREATE TABLE campsite (
    id INTEGER,
    c_id INTEGER,

    PRIMARY KEY (id, c_id),
    FOREIGN KEY (c_id) REFERENCES campground(id) ON DELETE CASCADE
);