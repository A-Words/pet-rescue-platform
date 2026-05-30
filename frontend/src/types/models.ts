export interface User {
  id: string
  username: string
  email: string
  phone?: string
  avatar_url?: string
  role: 'user' | 'admin'
  is_active: boolean
  created_at: string
}

export interface LostPet {
  id: string
  user_id: string
  user?: User
  pet_name: string
  pet_type: 'dog' | 'cat' | 'bird' | 'other'
  breed?: string
  color?: string
  gender?: 'male' | 'female' | 'unknown'
  age_description?: string
  photo_urls: string[]
  description: string
  lost_date: string
  lost_location: string
  rescue_station?: string
  latitude?: number
  longitude?: number
  contact_info: string
  reward_amount: number
  status: 'active' | 'found' | 'closed'
  clue_count?: number
  created_at: string
  updated_at: string
}

export interface FoundClue {
  id: string
  lost_pet_id: string
  reporter_id: string
  reporter?: User
  photo_urls: string[]
  description: string
  found_location: string
  found_date: string
  contact_info: string
  status: 'pending' | 'confirmed' | 'rejected'
  admin_notes?: string
  created_at: string
}

export interface AdoptablePet {
  id: string
  pet_name: string
  pet_type: 'dog' | 'cat' | 'bird' | 'other'
  breed?: string
  color?: string
  gender?: 'male' | 'female' | 'unknown'
  age_months?: number
  photo_urls: string[]
  description?: string
  health_status: 'healthy' | 'treating' | 'chronic'
  is_vaccinated: boolean
  is_dewormed: boolean
  is_sterilized: boolean
  adoption_status: 'available' | 'reserved' | 'adopted'
  rescue_station?: string
  intake_date: string
  application_count?: number
}

export interface AdoptionApplication {
  id: string
  pet_id: string
  pet?: AdoptablePet
  applicant_id: string
  applicant?: User
  applicant_name: string
  applicant_phone: string
  applicant_address: string
  applicant_id_number: string
  housing_type?: string
  has_other_pets: boolean
  adoption_reason: string
  experience_description?: string
  status: 'pending' | 'approved' | 'rejected' | 'cancelled'
  review_records?: ReviewRecord[]
  created_at: string
  updated_at: string
}

export interface ReviewRecord {
  id: string
  application_id: string
  reviewer_id: string
  decision: 'approved' | 'rejected'
  review_notes?: string
  reviewed_at: string
}

export interface VisitReminder {
  id: string
  application_id: string
  adopter_id: string
  pet_id: string
  reminder_date: string
  visit_date?: string
  status: 'pending' | 'completed' | 'overdue'
  visit_notes?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export interface MonthlyStatistics {
  total_lost_reports: number
  successful_recoveries: number
  recovery_rate: number
  total_adoption_applications: number
  approved_adoptions: number
  adoption_success_rate: number
  total_found_clues: number
  confirmed_clues: number
}

export interface DashboardOverview {
  active_lost_pets: number
  available_adoptable: number
  pending_applications: number
  pending_clues: number
  overdue_reminders: number
}
