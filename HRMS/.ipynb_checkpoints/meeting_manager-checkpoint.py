from typing import List, Dict
from collections import defaultdict
from datetime import datetime
from hrms.schemas import MeetingCreate, MeetingCancelRequest

class MeetingManager:
    def __init__(self):
        self.meetings: Dict[str, List[Dict[str, str]]] = defaultdict(list)

    def schedule_meeting(self, req: MeetingCreate) -> str:
        dt_str = req.meeting_dt.isoformat()
        try:
            datetime.fromisoformat(dt_str)
        except ValueError:
            raise ValueError("Invalid datetime format; use ISO format.")
        emp_id = req.emp_id
        if any(m["date"] == dt_str for m in self.meetings[emp_id]):
            raise ValueError(f"Conflict: {emp_id} already has a meeting at {dt_str}.")
        self.meetings[emp_id].append({"date": dt_str, "topic": req.topic})
        return f"Meeting scheduled for {emp_id} on {dt_str} about '{req.topic}'."

    def get_meetings(self, employee_id: str) -> List[Dict[str, str]]:
        return sorted(self.meetings.get(employee_id, []), key=lambda m: m["date"])

    def cancel_meeting(self, req: MeetingCancelRequest) -> str:
        emp_id = req.emp_id
        dt_str = req.meeting_dt.isoformat()
        original = list(self.meetings.get(emp_id, []))
        self.meetings[emp_id] = [m for m in original if not (
            m["date"] == dt_str and (req.topic is None or m["topic"] == req.topic)
        )]
        if len(self.meetings[emp_id]) == len(original):
            raise ValueError("No matching meeting to cancel.")
        return f"Canceled meeting for {emp_id} on {dt_str}{f' about {req.topic}' if req.topic else ''}."