// АВТОГЕНЕРАЦИЯ из team_lead/contracts/python (gen_ts.py). Не править вручную.

export type AccidentStatus = "new" | "assigned" | "inspection" | "completed";
export type TaskType = "pdf_protocol" | "policy_recheck" | "report" | "margin_calc" | "contract_reg" | "email_send";
export type DamageCategory = "minor" | "medium" | "total_loss";

/** implemented · владелец: Дима */
export interface ClaimCreateRequest {
  policy_number: string;
  region: string;
  description?: string;
}

/** implemented · владелец: Дима */
export interface StatusChangeRequest {
  status: AccidentStatus;
}

/** implemented · владелец: Дима */
export interface ClaimResponse {
  claim_id: string;
  number: string;
  policy_number: string;
  region: string;
  description: string;
  status: AccidentStatus;
  expert_id?: string | null;
  created_at: string;
}

/** implemented · владелец: Дима */
export interface InspectionCreateRequest {
  damage_found: boolean;
  notes?: string;
}

/** implemented · владелец: Дима */
export interface InspectionResponse {
  inspection_id: string;
  claim_id: string;
  expert_id: string;
  damage_found: boolean;
  notes: string;
  completed_at: string;
}

/** implemented · владелец: Дима */
export interface SignatureRequest {
  signed_by: string;
}

/** implemented · владелец: Дима */
export interface SignatureResponse {
  signature_id: string;
  claim_id: string;
  signed_by: string;
  verified: boolean;
}

/** implemented · владелец: Дима */
export interface PhotosResponse {
  photo_ids: string[];
}

/** proposed · владелец: Никита */
export interface DamageAssessmentDTO {
  category: DamageCategory;
  payout: number | string;
  requires_expert: boolean;
  requires_additional_photos: boolean;
}

/** proposed · владелец: Дима+Миша */
export interface StoredDocument {
  claim_id: string;
  kind: string;
  file_id: string;
  created_at: string;
}

/** proposed · владелец: Дима+Миша */
export interface OutboxTask {
  task_id: string;
  type: TaskType;
  claim_id?: string | null;
  created_at: string;
  status?: OutboxStatus;
  attempts?: number;
  error?: string | null;
}

/** proposed · владелец: Дима */
export interface CodeRequest {
  phone: string;
}

/** proposed · владелец: Дима */
export interface CodeVerifyRequest {
  phone: string;
  code: string;
}

/** proposed · владелец: Дима */
export interface TokenResponse {
  access_token: string;
  role: string;
  expires_at: string;
}

/** proposed · владелец: Дима */
export interface PaymentSessionRequest {
  policy_id: string;
  amount: number | string;
}

/** proposed · владелец: Дима */
export interface PaymentSessionResponse {
  session_id: string;
  pay_url: string;
}

/** proposed · владелец: Дима */
export interface PaymentWebhook {
  session_id: string;
  status: string;
  amount: number | string;
}

/** proposed · владелец: Дима+Амелия */
export interface UserDTO {
  user_id: string;
  full_name: string;
  role: string;
  active?: boolean;
}

/** proposed · владелец: Дима+Амелия */
export interface TariffDTO {
  tariff_id: string;
  region: string;
  base_rate: number | string;
  coefficient: number | string;
}

/** proposed · владелец: Дима+Амелия */
export interface PolicyDTO {
  policy_number: string;
  holder: string;
  status: string;
  expires_at: string;
}

/** proposed · владелец: Дима+Амелия */
export interface PaymentDTO {
  payment_id: string;
  policy_number: string;
  amount: number | string;
  status: string;
  paid_at?: string | null;
}

/** proposed · владелец: Дима+Амелия */
export interface AuditEventDTO {
  event_id: string;
  actor: string;
  action: string;
  entity_id: string;
  occurred_at: string;
}

/** proposed · владелец: Дима+Миша+Амелия */
export interface MarginReportDTO {
  period_start: string;
  period_end: string;
  revenue: number | string;
  commission: number | string;
  margin: number | string;
}

/** proposed · владелец: Дима+Амелия */
export interface InvoiceRequest {
  period_start: string;
  period_end: string;
}

/** proposed · владелец: Дима+Миша */
export interface TransactionRecord {
  transaction_id: string;
  policy_number: string;
  amount: number | string;
  status: string;
  created_at: string;
}

/** proposed · владелец: Дима+Амелия */
export interface TaskRestartRequest {
  reason?: string;
}
