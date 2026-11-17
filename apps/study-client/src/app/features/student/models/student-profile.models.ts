/** API #04: app/modules/guest/api_04_users_me/models.py */
export interface StudentAccountProfileDto {
  id: number;
  full_name: string;
  email: string;
  role: string;
  avatar_url: string | null;
  phone: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}
