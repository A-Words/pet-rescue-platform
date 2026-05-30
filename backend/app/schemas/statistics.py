from decimal import Decimal

from pydantic import BaseModel


class MonthlyStatistics(BaseModel):
    total_lost_reports: int
    successful_recoveries: int
    recovery_rate: Decimal
    total_adoption_applications: int
    approved_adoptions: int
    adoption_success_rate: Decimal
    total_found_clues: int
    confirmed_clues: int


class DashboardOverview(BaseModel):
    active_lost_pets: int
    available_adoptable: int
    pending_applications: int
    pending_clues: int
    overdue_reminders: int
