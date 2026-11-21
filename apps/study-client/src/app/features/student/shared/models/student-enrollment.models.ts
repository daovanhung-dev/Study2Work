export interface StudentEnrollment {
  id: number;
  course_id: number;
  user_id: number;
  status: string;
  enrolled_at: string;
  completed_at?: string | null;
}
