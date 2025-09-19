from typing import List, Dict, Optional
from difflib import get_close_matches
from hrms.schemas import EmployeeCreate


class EmployeeManager:
    def __init__(self):
        self.employees: Dict[str, Dict[str, str]] = {}
        self.manager_map: Dict[str, Optional[str]] = {}

    def get_next_emp_id(self) -> str:
        """
        Generate the next employee ID based on the existing IDs.
        """
        if not self.employees:
            return "E001"
        max_id = max(int(eid[1:]) for eid in self.employees.keys())
        return f"E{max_id + 1:03}"

    def add_employee(self, emp: EmployeeCreate) -> None:
        """
        Add a new employee via Pydantic model.
        Raises ValueError if emp_id exists or manager_id is invalid.
        """
        name, manager_id = emp.name, emp.manager_id
        if emp.emp_id in self.employees:
            raise ValueError(f"Employee ID '{emp.emp_id}' already exists.")
        if manager_id and manager_id not in self.employees:
            raise ValueError(f"Manager ID '{manager_id}' does not exist.")
        self.employees[emp.emp_id] = emp.model_dump()
        self.manager_map[emp.emp_id] = manager_id

    def get_manager(self, emp_id: str) -> str:
        """
        Return manager's ID and name, or a message if none.
        """
        if emp_id not in self.employees:
            raise ValueError(f"Employee ID '{emp_id}' not found.")
        mgr_id = self.manager_map.get(emp_id)
        if not mgr_id:
            return "No manager assigned."
        mgr = self.employees[mgr_id]
        return f"{mgr_id}: {mgr['name']}"

    def search_employee_by_name(self, name_query: str, n: int = 5, cutoff: float = 0.6) -> List[str]:
        matches = get_close_matches(name_query, [e["name"] for e in self.employees.values()], n=n, cutoff=cutoff)
        return [eid for eid, data in self.employees.items() if data["name"] in matches]

    def get_employee_details(self, emp_id: str) -> Dict[str, str]:
        if emp_id not in self.employees:
            raise ValueError(f"Employee ID '{emp_id}' not found.")
        return self.employees[emp_id]

    def get_direct_reports(self, manager_id: str) -> List[str]:
        if manager_id not in self.employees:
            raise ValueError(f"Manager ID '{manager_id}' not found.")
        return [eid for eid, mgr in self.manager_map.items() if mgr == manager_id]


if __name__ == "__main__":
    em = EmployeeManager()
    em.add_employee(EmployeeCreate(name="John Doe", manager_id=None))
    em.add_employee(EmployeeCreate(name="Mama Doe", manager_id="E001"))
    print(em.get_next_emp_id())