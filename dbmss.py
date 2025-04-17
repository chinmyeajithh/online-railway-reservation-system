import streamlit as st
import sqlite3
import base64

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('train_reservation.db')
    return conn

# Function to create necessary tables if they do not exist
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        user_name TEXT PRIMARY KEY,
        password TEXT,
        name TEXT,
        email_id TEXT,
        age INTEGER
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Passenger (
        passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT,
        seat_no INTEGER,
        reservation_status TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Station (
        station_code TEXT PRIMARY KEY,
        station_no INTEGER,
        source_station TEXT,
        dest_station TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Train (
        train_no TEXT PRIMARY KEY,
        train_name TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Route (
        route_id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_no TEXT,
        dept_time TEXT,
        arrival_time TEXT,
        FOREIGN KEY (train_no) REFERENCES Train(train_no)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TrainStatus (
        train_status_id INTEGER PRIMARY KEY AUTOINCREMENT,
        train_no TEXT,
        available_seats INTEGER,
        booked_seats INTEGER,
        available_date TEXT,
        FOREIGN KEY (train_no) REFERENCES Train(train_no)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT,
        train_status_id INTEGER,
        date TEXT,
        FOREIGN KEY (user_name) REFERENCES User(user_name),
        FOREIGN KEY (train_status_id) REFERENCES TrainStatus(train_status_id)
    )
    ''')

    conn.commit()

def set_background_image(image_file):
    try:
        with open(image_file, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{encoded}");
                background-size: cover;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning("Background image file not found.")

# Create tables
create_tables()
#st.image(r"C:\Users\Chinmye Ajith\OneDrive\Desktop\dbms\images.jpeg")
# Streamlit app
st.title('Train Reservation System')

# Set background image
set_background_image(r"C:\Users\Chinmye Ajith\OneDrive\Desktop\dbms\image.jpg")

# Custom CSS for background image
page_bg_img = '''
<style>
.stApp {
    background-image: url(r"C:\\Users\\Chinmye Ajith\\OneDrive\\Desktop\\dbms\\image.jpg");
    background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title('HOME')
option = st.sidebar.radio('GO TO:', [
    "User Registration", 
    "Book Train", 
    "View & Update Bookings", 
    "Manage Trains", 
    "Manage Stations", 
    "View Train Status", 
    "View Stations", 
    "View Routes"
])

# User Registration
if option == "User Registration":
    st.header("Register New User")
    user_name = st.text_input("Username", key="reg_user_name")
    password = st.text_input("Password", type='password', key="reg_password")
    name = st.text_input("Name", key="reg_name")
    email_id = st.text_input("Email", key="reg_email_id")
    age = st.number_input("Age", min_value=0, key="reg_age")
    
    if st.button("Register", key="reg_button"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO User (user_name, password, name, email_id, age) VALUES (?, ?, ?, ?, ?)', 
                       (user_name, password, name, email_id, age))
        conn.commit()
        st.success("User registered successfully")

    st.header("Update User Details")
    update_user_name = st.text_input("Enter Username to Update", key="upd_user_name")
    new_password = st.text_input("New Password", type='password', key="upd_password")
    new_name = st.text_input("New Name", key="upd_name")
    new_email_id = st.text_input("New Email", key="upd_email_id")
    new_age = st.number_input("New Age", min_value=0, key="upd_age")
    
    if st.button("Update User", key="upd_button"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE User 
            SET password = ?, name = ?, email_id = ?, age = ? 
            WHERE user_name = ?''',
            (new_password, new_name, new_email_id, new_age, update_user_name))
        conn.commit()
        st.success("User details updated successfully")

# Book Train
if option == "Book Train":
    st.header("Book a Train")
    user_name = st.text_input("Username for Booking", key="book_user_name")
    train_no = st.text_input("Train Number", key="book_train_no")
    date = st.date_input("Date of Travel", key="book_date")
    
    if st.button("Book", key="book_button"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Books (user_name, train_status_id, date) 
            VALUES (?, (SELECT train_status_id FROM TrainStatus WHERE train_no = ?), ?)''', 
            (user_name, train_no, date))
        conn.commit()
        st.success("Train booked successfully")

# View & Update Bookings
if option == "View & Update Bookings":
    st.header("View Bookings")
    user_name = st.text_input("Enter Username to View Bookings", key="view_user_name")
    
    if st.button("View", key="view_button"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Books WHERE user_name = ?', (user_name,))
        bookings = cursor.fetchall()
        
        if bookings:
            for booking in bookings:
                st.write(f"Booking ID: {booking[0]}, Train Status ID: {booking[2]}, Date: {booking[3]}")
        else:
            st.write("No bookings found for this user")

    st.header("Update Booking")
    booking_id = st.number_input("Enter Booking ID to Update", min_value=0, key="upd_booking_id")
    new_train_no = st.text_input("New Train Number", key="upd_train_no_booking")
    new_date = st.date_input("New Date of Travel", key="upd_date_booking")
    
    if st.button("Update Booking", key="upd_booking_button"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Books 
            SET train_status_id = (SELECT train_status_id FROM TrainStatus WHERE train_no = ?), date = ? 
            WHERE book_id = ?''', 
            (new_train_no, new_date, booking_id))
        conn.commit()
        st.success("Booking updated successfully")

# Manage Trains
if option == "Manage Trains":
    st.header("Add New Train")
    train_no = st.text_input("Train Number", key="add_train_no")
    train_name = st.text_input("Train Name", key="add_train_name")
    
    if st.button("Add Train", key="add_train_button"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Train (train_no, train_name) VALUES (?, ?)', 
                       (train_no, train_name))
        conn.commit()
        st.success("Train added successfully")

    st.header("Update Train Details")
    update_train_no = st.text_input("Enter Train Number to Update", key="upd_train_no")
    new_train_name = st.text_input("New Train Name", key="upd_train_name")
    
    if st.button("Update Train", key="upd_train_button"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Train 
            SET train_name = ? 
            WHERE train_no = ?''',
            (new_train_name, update_train_no))
        conn.commit()
        st.success("Train details updated successfully")

    st.header("Add Train Status")
    status_train_no = st.text_input("Train Number for Status", key="add_status_train_no")
    available_seats = st.number_input("Available Seats", min_value=0, key="add_available_seats")
    booked_seats = st.number_input("Booked Seats", min_value=0, key="add_booked_seats")
    available_date = st.date_input("Available Date", key="add_available_date")
    
    if st.button("Add Train Status", key="add_status_button"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO TrainStatus (train_no, available_seats, booked_seats, available_date) 
            VALUES (?, ?, ?, ?)''', 
            (status_train_no, available_seats, booked_seats, available_date))
        conn.commit()
        st.success("Train status added successfully")

# Manage Stations
if option == "Manage Stations":
    st.header("Add New Station")
    station_code = st.text_input("Station Code", key="add_station_code")
    station_no = st.number_input("Station Number", min_value=0, key="add_station_no")
    source_station = st.text_input("Source Station", key="add_source_station")
    dest_station = st.text_input("Destination Station", key="add_dest_station")
    
    if st.button("Add Station", key="add_station_button"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Station (station_code, station_no, source_station, dest_station) VALUES (?, ?, ?, ?)', 
                       (station_code, station_no, source_station, dest_station))
        conn.commit()
        st.success("Station added successfully")

    st.header("Update Station Details")
    update_station_code = st.text_input("Enter Station Code to Update", key="upd_station_code")
    new_station_no = st.number_input("New Station Number", min_value=0, key="upd_station_no")
    new_source_station = st.text_input("New Source Station", key="upd_source_station")
    new_dest_station = st.text_input("New Destination Station", key="upd_dest_station")
    
    if st.button("Update Station", key="upd_station_button"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Station 
            SET station_no = ?, source_station = ?, dest_station = ? 
            WHERE station_code = ?''',
            (new_station_no, new_source_station, new_dest_station, update_station_code))
        conn.commit()
        st.success("Station details updated successfully")

# View Train Status
if option == "View Train Status":
    st.header("View Train Status")
    train_no = st.text_input("Enter Train Number to View Status", key="view_status_train_no")
    
    if st.button("View Status", key="view_status_button"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM TrainStatus WHERE train_no = ?', (train_no,))
        status = cursor.fetchall()
        
        if status:
            for stat in status:
                st.write(f"Train Number: {stat[1]}, Available Seats: {stat[2]}, Booked Seats: {stat[3]}, Available Date: {stat[4]}")
        else:
            st.write("No status found for this train number")

# View Stations
if option == "View Stations":
    st.header("View Stations")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Station')
    stations = cursor.fetchall()
    
    if stations:
        for station in stations:
            st.write(f"Station Code: {station[0]}, Station Number: {station[1]}, Source Station: {station[2]}, Destination Station: {station[3]}")
    else:
        st.write("No stations found")

# View Routes
if option == "View Routes":
    st.header("View Routes")
    train_no = st.text_input("Enter Train Number to View Routes", key="view_route_train_no")
    
    if st.button("View Routes", key="view_route_button"):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Route WHERE train_no = ?', (train_no,))
        routes = cursor.fetchall()
        
        if routes:
            for route in routes:
                st.write(f"Route ID: {route[0]}, Train Number: {route[1]}, Departure Time: {route[2]}, Arrival Time: {route[3]}")
        else:
            st.write("No routes found for this train number")
