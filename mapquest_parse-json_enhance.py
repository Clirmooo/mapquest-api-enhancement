import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "EGVIJZBu6OlzjazQolRueK1VFVfoi30D"

while True:
    print("\n=============================================")
    print("        MAPQUEST ROUTE APPLICATION")
    print("=============================================")

    orig = input("Starting Location (or 'q' to quit): ")

    if orig.lower() in ["quit", "q"]:
        print("Exiting application...")
        break

    dest = input("Destination (or 'q' to quit): ")

    if dest.lower() in ["quit", "q"]:
        print("Exiting application...")
        break

    # Choose distance unit
    print("\nChoose distance unit:")
    print("1. Kilometers")
    print("2. Miles")

    unit_choice = input("Enter choice (1 or 2): ")

    if unit_choice not in ["1", "2"]:
        print("Invalid choice. Using kilometers by default.")
        unit_choice = "1"

    # Create API URL
    url = main_api + urllib.parse.urlencode({
        "key": key,
        "from": orig,
        "to": dest
    })

    print("\nRequesting route information...")

    try:
        response = requests.get(url, timeout=10)
        json_data = response.json()

        json_status = json_data["info"]["statuscode"]

        if json_status == 0:

            print("\n=============================================")
            print("              ROUTE INFORMATION")
            print("=============================================")

            print("From:            " + orig)
            print("To:              " + dest)
            print("Trip Duration:   " + json_data["route"]["formattedTime"])

            # Original distance is in miles
            distance_miles = json_data["route"]["distance"]

            if unit_choice == "1":
                distance = distance_miles * 1.60934
                print("Distance:        " + "{:.2f}".format(distance) + " km")
            else:
                distance = distance_miles
                print("Distance:        " + "{:.2f}".format(distance) + " miles")

            # Fuel information
            if "fuelUsed" in json_data["route"]:
                fuel_gallons = json_data["route"]["fuelUsed"]
                fuel_liters = fuel_gallons * 3.78541

                print("Fuel Used:       " + "{:.2f}".format(fuel_liters) + " L")
            else:
                print("Fuel Used:       Not available")

            print("=============================================")
            print("                 DIRECTIONS")
            print("=============================================")

            # Display directions
            for number, each in enumerate(
                json_data["route"]["legs"][0]["maneuvers"], start=1
            ):

                maneuver_distance_miles = each["distance"]

                if unit_choice == "1":
                    maneuver_distance = maneuver_distance_miles * 1.60934
                    unit = "km"
                else:
                    maneuver_distance = maneuver_distance_miles
                    unit = "miles"

                print(
                    str(number) + ". " +
                    each["narrative"] +
                    " (" +
                    "{:.2f}".format(maneuver_distance) +
                    " " + unit + ")"
                )

            print("=============================================")
            print("API Status: 0 = Successful route call.")
            print("=============================================")

        else:
            print("\nRoute request failed.")
            print("API Status: " + str(json_status))

    except requests.exceptions.RequestException:
        print("\nError: Unable to connect to the MapQuest API.")
        print("Please check your internet connection.")

    except KeyError:
        print("\nError: Unexpected data received from the API.")

    except ValueError:
        print("\nError: Invalid response from the API.")

    # Ask if user wants another route
    again = input("\nDo you want to search another route? (y/n): ")

    if again.lower() != "y":
        print("\nThank you for using the MapQuest Route Application!")
        break