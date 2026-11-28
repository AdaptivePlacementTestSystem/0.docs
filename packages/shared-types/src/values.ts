import { CandidateRejectionReason } from './enums/candidate-rejection-reason.enum';
import { CEFRConfidence } from './enums/cefr-confidence.enum';
import { CEFRLevel } from './enums/cefr-level.enum';
import { CheckLevel } from './enums/check-level.enum';
import { CheckPoint } from './enums/check-point.enum';
import { ExamRoundStatus } from './enums/exam-round-status.enum';
import { ItemBatchSource } from './enums/item-batch-source.enum';
import { ItemBatchStatus } from './enums/item-batch-status.enum';
import { ItemCheckReasonCode } from './enums/item-check-reason-code.enum';
import { ItemStatus } from './enums/item-status.enum';
import { ReviewAction } from './enums/review-action.enum';
import { SessionStatus } from './enums/session-status.enum';
import { Skill } from './enums/skill.enum';
import { StoppingReason } from './enums/stopping-reason.enum';
import { UserRole } from './enums/user-role.enum';
import { ErrorCode } from './errors/error-code';

/**
 * Dạng "literal union" và danh sách giá trị của enum — cho nơi không muốn import enum (FE: zod, select, mock).
 * `${E}` biến enum thành union chuỗi, nên `'TEACHER'` gán được cho `UserRoleValue`.
 */
export type UserRoleValue = `${UserRole}`;
export type SessionStatusValue = `${SessionStatus}`;
export type StoppingReasonValue = `${StoppingReason}`;
export type CefrLevelValue = `${CEFRLevel}`;
export type CefrConfidenceValue = `${CEFRConfidence}`;
export type SkillValue = `${Skill}`;
export type ItemStatusValue = `${ItemStatus}`;
export type ItemBatchSourceValue = `${ItemBatchSource}`;
export type ItemBatchStatusValue = `${ItemBatchStatus}`;
export type ReviewActionValue = `${ReviewAction}`;
export type CheckLevelValue = `${CheckLevel}`;
export type CheckPointValue = `${CheckPoint}`;
export type ExamRoundStatusValue = `${ExamRoundStatus}`;
export type ItemCheckReasonCodeValue = `${ItemCheckReasonCode}`;
export type CandidateRejectionReasonValue = `${CandidateRejectionReason}`;
export type ErrorCodeValue = `${ErrorCode}`;

export const USER_ROLES = Object.values(UserRole) as UserRoleValue[];
export const SESSION_STATUSES = Object.values(SessionStatus) as SessionStatusValue[];
export const STOPPING_REASONS = Object.values(StoppingReason) as StoppingReasonValue[];
export const CEFR_LEVELS = Object.values(CEFRLevel) as CefrLevelValue[];
export const CEFR_CONFIDENCES = Object.values(CEFRConfidence) as CefrConfidenceValue[];
export const SKILLS = Object.values(Skill) as SkillValue[];
export const ITEM_STATUSES = Object.values(ItemStatus) as ItemStatusValue[];
export const ITEM_BATCH_SOURCES = Object.values(ItemBatchSource) as ItemBatchSourceValue[];
export const ITEM_BATCH_STATUSES = Object.values(ItemBatchStatus) as ItemBatchStatusValue[];
export const REVIEW_ACTIONS = Object.values(ReviewAction) as ReviewActionValue[];
export const CHECK_LEVELS = Object.values(CheckLevel) as CheckLevelValue[];
export const CHECK_POINTS = Object.values(CheckPoint) as CheckPointValue[];
export const EXAM_ROUND_STATUSES = Object.values(ExamRoundStatus) as ExamRoundStatusValue[];
export const ITEM_CHECK_REASON_CODES = Object.values(ItemCheckReasonCode) as ItemCheckReasonCodeValue[];
export const CANDIDATE_REJECTION_REASONS = Object.values(CandidateRejectionReason) as CandidateRejectionReasonValue[];
export const ERROR_CODES = Object.values(ErrorCode) as ErrorCodeValue[];
