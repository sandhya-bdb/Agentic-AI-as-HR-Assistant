from typing import Dict, List, Optional
from collections import defaultdict
from datetime import date, timedelta
import random
from hrms import *

def seed_services(employee_manager, leave_manager, meeting_manager, ticket_manager):
    """
    Seeds all service classes with coherent dummy data.

    Args:
        employee_manager: Instance of EmployeeManager
        leave_manager: Instance of LeaveManager
        meeting_manager: Instance of MeetingManager
        ticket_manager: Instance of TicketManager

    Returns:
        None - services are modified in-place
    """

    employees_data = [
        # Leadership
        {"emp_id": "E001", "name": "Sarah Johnson", "manager_id": None, "email": "sarah.johnson@atliq.com"},
        {"emp_id": "E002", "name": "Michael Chen", "manager_id": None, "email": "michael.chen@atliq.com"},

        # Engineering team under Sarah
        {"emp_id": "E003", "name": "David Wilson", "manager_id": "E001", "email": "david.wilson@atliq.com"},
        {"emp_id": "E004", "name": "Tony Sharma", "manager_id": "E003", "email": "tony.sharma@atliq.com"},
        {"emp_id": "E005", "name": "James Rodriguez", "manager_id": "E003", "email": "james.rodriguez@atliq.com"},

        # Product team under Michael
        {"emp_id": "E006", "name": "Emily Kim", "manager_id": "E002", "email": "emily.kim@atliq.com"},
        {"emp_id": "E007", "name": "Carlos Mendez", "manager_id": "E006", "email": "carlos.mendez@atliq.com"},
        {"emp_id": "E008", "name": "Lisa Wong", "manager_id": "E006", "email": "lisa.wong@atliq.com"},
    ]

    # Populate employee manager
    for employee in employees_data:
        emp_id = employee["emp_id"]
        employee_manager.employees[emp_id] = employee
        employee_manager.manager_map[emp_id] = employee["manager_id"]

    # Create leave data
    # Set up some leave history for each employee
    current_date = date.today()
    request_id_counter = 1

    for employee in employees_data:
        emp_id = employee["emp_id"]

        # Set a random leave balance between 5 and 20 days
        leave_manager.employee_leaves[emp_id]["balance"] = random.randint(5, 20)

        # Create some leave history entries
        num_leaves = random.randint(1, 5)  # Random number of leave entries

        for i in range(num_leaves):
            # Generate a leave date in the past (1-90 days ago)
            days_ago = random.randint(1, 90)
            leave_date = current_date - timedelta(days=days_ago)

            # Add to leave history
            history_entry = {
                "history_id": len(leave_manager.employee_leaves[emp_id]["history"]) + 1,
                "emp_id": emp_id,
                "leave_date": leave_date,
                "request_id": request_id_counter
            }
            leave_manager.employee_leaves[emp_id]["history"].append(history_entry)

            # Sometimes add consecutive days for the same request
            if random.random() > 0.7:  # 30% chance of multi-day leave
                for j in range(1, random.randint(2, 5)):  # 1-4 additional days
                    consecutive_date = leave_date + timedelta(days=j)
                    consecutive_entry = {
                        "history_id": len(leave_manager.employee_leaves[emp_id]["history"]) + 1,
                        "emp_id": emp_id,
                        "leave_date": consecutive_date,
                        "request_id": request_id_counter
                    }
                    leave_manager.employee_leaves[emp_id]["history"].append(consecutive_entry)

            request_id_counter += 1

    # Create meeting data
    meeting_types = ["Team Sync", "Project Review", "Client Meeting", "1:1", "Planning"]
    meeting_locations = ["Conference Room A", "Conference Room B", "Zoom", "MS Teams", "Cafeteria"]

    # Generate meetings for each employee
    for employee in employees_data:
        emp_id = employee["emp_id"]
        num_meetings = random.randint(2, 6)

        for i in range(num_meetings):
            # Create a meeting in the next 10 days
            meeting_date = current_date + timedelta(days=random.randint(0, 10))
            meeting_hour = random.randint(9, 16)  # 9 AM to 4 PM

            meeting = {
                "title": random.choice(meeting_types),
                "date": meeting_date.strftime("%Y-%m-%d"),
                "time": f"{meeting_hour:02d}:00",
                "location": random.choice(meeting_locations),
                "attendees": []
            }

            # Add some attendees (1-3 other employees)
            potential_attendees = [e["emp_id"] for e in employees_data if e["emp_id"] != emp_id]
            num_attendees = min(random.randint(1, 3), len(potential_attendees))
            attendees = random.sample(potential_attendees, num_attendees)

            meeting["attendees"] = attendees
            meeting_manager.meetings[emp_id].append(meeting)

    # Create ticket data
    ticket_items = ["Laptop", "Monitor", "Keyboard", "Mouse", "Headset", "Office Chair", "Software License"]
    ticket_reasons = ["New hire setup", "Replacement for broken item", "Upgrade request", "Project requirement",
                      "Ergonomic needs"]

    # Generate some tickets
    num_tickets = random.randint(8, 15)
    for _ in range(num_tickets):
        employee = random.choice(employees_data)

        ticket = {
            "ticket_id": str(ticket_manager._next_id),
            "emp_id": employee["emp_id"],
            "item": random.choice(ticket_items),
            "reason": random.choice(ticket_reasons),
            "status": random.choice(["Open", "In Progress", "Closed"])
        }

        ticket_manager.tickets.append(ticket)
        ticket_manager._next_id += 1

    return {
        "employees": len(employee_manager.employees),
        "leave_records": sum(len(data["history"]) for data in leave_manager.employee_leaves.values()),
        "meetings": sum(len(meetings) for meetings in meeting_manager.meetings.values()),
        "tickets": len(ticket_manager.tickets)
    }

if __name__ == "__main__":
    # Initialize services
    employee_manager = EmployeeManager()
    leave_manager = LeaveManager()
    meeting_manager = MeetingManager()
    ticket_manager = TicketManager()

    # Seed the services with data
    result = seed_services(employee_manager, leave_manager, meeting_manager, ticket_manager)

    print(f"Seeded {result['employees']} employees")
    print(f"Seeded {result['leave_records']} leave records")
    print(f"Seeded {result['meetings']} meetings")
    print(f"Seeded {result['tickets']} tickets")

    # employee_manager.add_employee(EmployeeCreate(name="John Doe", manager_id="E001"))
    # print(f"Manager of E004 {employee_manager.get_manager('E004')}")
    # print(f"Direct reports of E004 {employee_manager.get_direct_reports('E001')}")

    print(leave_manager.get_leave_history("E004"))
