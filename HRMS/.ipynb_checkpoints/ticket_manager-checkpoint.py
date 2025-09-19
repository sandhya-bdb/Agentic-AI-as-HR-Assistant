from typing import List, Dict, Optional
from datetime import datetime
from hrms.schemas import TicketCreate, TicketStatusUpdate


class TicketManager:
    def __init__(self):
        self.tickets: List[Dict[str, str]] = []
        self._next_id: int = 1

    def create_ticket(self, req: TicketCreate) -> str:
        ticket_id = f"T{self._next_id:04d}"
        ticket = {
            "ticket_id": ticket_id,
            "emp_id": req.emp_id,
            "item": req.item,
            "reason": req.reason,
            "status": "Open",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        self.tickets.append(ticket)
        self._next_id += 1
        return f"Ticket {ticket_id} created for {req.emp_id}."

    def update_ticket_status(self, req: TicketStatusUpdate, ticket_id: str) -> str:
        for t in self.tickets:
            if t["ticket_id"] == ticket_id:
                t["status"] = req.status
                t["updated_at"] = datetime.utcnow().isoformat()
                return f"Ticket {ticket_id} status updated to {req.status}."
        raise ValueError(f"Ticket '{ticket_id}' not found.")

    def list_tickets(
            self,
            employee_id: Optional[str] = None,
            status: Optional[str] = None
    ) -> List[Dict[str, str]]:
        results = self.tickets
        if employee_id:
            results = [t for t in results if t["emp_id"] == employee_id]
        if status:
            results = [t for t in results if t["status"].lower() == status.lower()]
        return results
