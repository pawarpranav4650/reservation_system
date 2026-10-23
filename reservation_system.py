import json
import os
from datetime import datetime

# -----------------------------
# DATA
# -----------------------------

buses = {
    "B101": {
        "route": "Pune -> Mumbai",
        "departure": "08:00 AM",
        "arrival": "12:00 PM",
        "total_seats": 10,
        "fare": 450,
        "available_seats": list(range(1, 11))
    },

    "B102": {
        "route": "Pune -> Nashik",
        "departure": "09:00 AM",
        "arrival": "01:00 PM",
        "total_seats": 12,
        "fare": 500,
        "available_seats": list(range(1, 13))
    },

    "B103": {
        "route": "Mumbai -> Pune",
        "departure": "02:00 PM",
        "arrival": "06:00 PM",
        "total_seats": 10,
        "fare": 450,
        "available_seats": list(range(1, 11))
    },

    "B104": {
        "route": "Pune -> Kolhapur",
        "departure": "07:00 AM",
        "arrival": "12:00 PM",
        "total_seats": 15,
        "fare": 650,
        "available_seats": list(range(1, 16))
    }
}

BOOKING_FILE = "bookings.json"


# -----------------------------
# LOAD BOOKINGS
# -----------------------------

def load_bookings():
    if os.path.exists(BOOKING_FILE):
        try:
            with open(BOOKING_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}

    return {}


# -----------------------------
# SAVE BOOKINGS
# -----------------------------

def save_bookings():
    with open(BOOKING_FILE, "w") as file:
        json.dump(bookings, file, indent=4)


bookings = load_bookings()


# -----------------------------
# GENERATE BOOKING ID
# -----------------------------

def generate_booking_id():
    number = 1001

    while f"BK{number}" in bookings:
        number += 1

    return f"BK{number}"


# -----------------------------
# DISPLAY BUSES
# -----------------------------

def view_buses():

    print("\n========== AVAILABLE BUSES ==========")

    for bus_id, bus in buses.items():

        print(f"\nBus ID       : {bus_id}")
        print(f"Route        : {bus['route']}")
        print(f"Departure    : {bus['departure']}")
        print(f"Arrival      : {bus['arrival']}")
        print(f"Total Seats  : {bus['total_seats']}")
        print(f"Available    : {len(bus['available_seats'])}")
        print(f"Fare         : Rs.{bus['fare']}")

    print("\n=====================================")


# -----------------------------
# VIEW AVAILABLE SEATS
# -----------------------------

def view_seats():

    view_buses()

    bus_id = input("\nEnter Bus ID: ").strip().upper()

    if bus_id not in buses:
        print("Invalid Bus ID.")
        return

    available = buses[bus_id]["available_seats"]

    print(f"\nAvailable seats for {bus_id}:")

    if available:
        print(available)
    else:
        print("No seats available.")


# -----------------------------
# BOOK TICKET
# -----------------------------

def book_ticket():

    view_buses()

    bus_id = input("\nEnter Bus ID: ").strip().upper()

    if bus_id not in buses:
        print("Invalid Bus ID.")
        return

    bus = buses[bus_id]

    if not bus["available_seats"]:
        print("Sorry! No seats available.")
        return

    print("\nAvailable Seats:")
    print(bus["available_seats"])

    try:
        seat_number = int(input("Enter seat number: "))
    except ValueError:
        print("Please enter a valid seat number.")
        return

    if seat_number not in bus["available_seats"]:
        print("Seat is not available.")
        return

    name = input("Enter passenger name: ").strip()

    if not name:
        print("Passenger name cannot be empty.")
        return

    phone = input("Enter phone number: ").strip()

    if not phone.isdigit() or len(phone) != 10:
        print("Please enter a valid 10-digit phone number.")
        return

    booking_id = generate_booking_id()

    booking = {
        "booking_id": booking_id,
        "passenger_name": name,
        "phone": phone,
        "bus_id": bus_id,
        "route": bus["route"],
        "seat_number": seat_number,
        "fare": bus["fare"],
        "booking_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Confirmed"
    }

    bookings[booking_id] = booking

    # Remove booked seat
    bus["available_seats"].remove(seat_number)

    save_bookings()

    print("\n========== BOOKING SUCCESSFUL ==========")
    print(f"Booking ID    : {booking_id}")
    print(f"Passenger     : {name}")
    print(f"Phone         : {phone}")
    print(f"Bus ID        : {bus_id}")
    print(f"Route         : {bus['route']}")
    print(f"Seat Number   : {seat_number}")
    print(f"Fare          : Rs.{bus['fare']}")
    print("Status        : Confirmed")
    print("========================================")


# -----------------------------
# VIEW BOOKING DETAILS
# -----------------------------

def view_booking():

    booking_id = input("\nEnter Booking ID: ").strip().upper()

    if booking_id not in bookings:
        print("Booking not found.")
        return

    booking = bookings[booking_id]

    print("\n========== BOOKING DETAILS ==========")
    print(f"Booking ID    : {booking['booking_id']}")
    print(f"Passenger     : {booking['passenger_name']}")
    print(f"Phone         : {booking['phone']}")
    print(f"Bus ID        : {booking['bus_id']}")
    print(f"Route         : {booking['route']}")
    print(f"Seat Number   : {booking['seat_number']}")
    print(f"Fare          : Rs.{booking['fare']}")
    print(f"Booking Date  : {booking['booking_date']}")
    print(f"Status        : {booking['status']}")
    print("=====================================")


# -----------------------------
# CANCEL BOOKING
# -----------------------------

def cancel_booking():

    booking_id = input("\nEnter Booking ID: ").strip().upper()

    if booking_id not in bookings:
        print("Booking not found.")
        return

    booking = bookings[booking_id]

    if booking["status"] == "Cancelled":
        print("This booking is already cancelled.")
        return

    bus_id = booking["bus_id"]
    seat_number = booking["seat_number"]

    # Release the seat
    buses[bus_id]["available_seats"].append(seat_number)
    buses[bus_id]["available_seats"].sort()

    booking["status"] = "Cancelled"

    save_bookings()

    print("\nBooking cancelled successfully.")
    print(f"Booking ID : {booking_id}")
    print(f"Seat {seat_number} has been released.")


# -----------------------------
# SEARCH BOOKING
# -----------------------------

def search_booking():

    search = input(
        "\nEnter Booking ID or Passenger Name: "
    ).strip().lower()

    found = False

    for booking in bookings.values():

        if (
            search == booking["booking_id"].lower()
            or search in booking["passenger_name"].lower()
        ):

            print("\n---------- BOOKING ----------")
            print(f"Booking ID  : {booking['booking_id']}")
            print(f"Passenger   : {booking['passenger_name']}")
            print(f"Bus ID      : {booking['bus_id']}")
            print(f"Route       : {booking['route']}")
            print(f"Seat        : {booking['seat_number']}")
            print(f"Fare        : Rs.{booking['fare']}")
            print(f"Status      : {booking['status']}")
            print("-----------------------------")

            found = True

    if not found:
        print("No booking found.")


# -----------------------------
# VIEW ALL BOOKINGS
# -----------------------------

def view_all_bookings():

    if not bookings:
        print("\nNo bookings available.")
        return

    print("\n========== ALL BOOKINGS ==========")

    for booking in bookings.values():

        print(
            f"{booking['booking_id']} | "
            f"{booking['passenger_name']} | "
            f"{booking['bus_id']} | "
            f"Seat {booking['seat_number']} | "
            f"Rs.{booking['fare']} | "
            f"{booking['status']}"
        )

    print("==================================")


# -----------------------------
# MAIN MENU
# -----------------------------

def main():

    while True:

        print("\n")
        print("==========================================")
        print("     RAILWAY / BUS RESERVATION SYSTEM")
        print("==========================================")

        print("1. View Available Buses")
        print("2. View Available Seats")
        print("3. Book Ticket")
        print("4. View Booking Details")
        print("5. Cancel Booking")
        print("6. Search Passenger / Booking")
        print("7. View All Bookings")
        print("8. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            view_buses()

        elif choice == "2":
            view_seats()

        elif choice == "3":
            book_ticket()

        elif choice == "4":
            view_booking()

        elif choice == "5":
            cancel_booking()

        elif choice == "6":
            search_booking()

        elif choice == "7":
            view_all_bookings()

        elif choice == "8":
            print("\nThank you for using the Reservation System!")
            break

        else:
            print("\nInvalid choice. Please try again.")


# -----------------------------
# PROGRAM START
# -----------------------------

print("TEST:python file is running")

if __name__ == "__main__":
    main()