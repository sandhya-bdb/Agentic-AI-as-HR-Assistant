from collections import defaultdict
from typing import Dict

from hrms.schemas import LeaveApplyRequest


class LeaveManager:
    def __init__(self):
        self.employee_leaves: Dict[str, Dict] = defaultdict(
            lambda: {"balance": 20, "history": []}
        )

    def get_leave_balance(self, employee_id: str) -> str:
        data = self.employee_leaves.get(employee_id)
        if data:
            return f"{employee_id} has {data['balance']} leave days remaining."
        return "Employee ID not found."

    def apply_leave(self, req: LeaveApplyRequest) -> str:
        employee_id = req.emp_id
        leave_dates = [d.isoformat() for d in req.leave_dates]
        if employee_id not in self.employee_leaves:
            return "Employee ID not found."
        requested = len(leave_dates)
        available = self.employee_leaves[employee_id]["balance"]
        if available < requested:
            return f"Insufficient leave balance: requested {requested}, available {available}."
        self.employee_leaves[employee_id]["balance"] -= requested
        self.employee_leaves[employee_id]["history"].extend(leave_dates)
        return (f"Leave applied for {requested} day(s). Remaining balance: "
                f"{self.employee_leaves[employee_id]['balance']}")

    def get_leave_history(self, employee_id: str) -> str:
        data = self.employee_leaves.get(employee_id)
        if data:
            hist = data['history']
            dates = [record['leave_date'].strftime("%B %d, %Y") for record in hist]
            return f"Leave history for {employee_id}: {', '.join(dates)}."
        return "Employee ID not found."

if __name__ == "__main__":
    lm = LeaveManager()
    print(lm.get_leave_history("E004"))