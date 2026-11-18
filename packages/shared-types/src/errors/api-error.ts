import { ErrorCode } from './error-code';

/** Thân lỗi chuẩn của API: `{ code, message, details? }`. `details` tùy mã (ví dụ SESSION_IN_PROGRESS kèm `sessionId`). */
export interface ApiError<TDetails = unknown> {
  code: ErrorCode;
  message: string;
  details?: TDetails;
}

/** Chi tiết đi kèm `SESSION_IN_PROGRESS` (HTTP 409): phiên đang mở để SV vào lại. */
export interface SessionInProgressDetails {
  sessionId: string;
}
