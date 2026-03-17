export interface URLCreate {
  original_url: string;
  expiry_days?: number;
}

export interface URLRead {
  short_url_id: string;
  original_url: string;
  created_at: string;
  expires_at: string;
  is_expired: boolean;
}

export interface APIError {
  detail: string;
}
