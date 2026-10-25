import { CEFRConfidence } from './enums/cefr-confidence.enum';
import { CEFRLevel } from './enums/cefr-level.enum';
import { ItemBatchSource } from './enums/item-batch-source.enum';
import { ItemStatus } from './enums/item-status.enum';
import { SessionStatus } from './enums/session-status.enum';
import { Skill } from './enums/skill.enum';
import { StoppingReason } from './enums/stopping-reason.enum';
import { UserRole } from './enums/user-role.enum';

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

export const USER_ROLES = Object.values(UserRole) as UserRoleValue[];
export const SESSION_STATUSES = Object.values(SessionStatus) as SessionStatusValue[];
export const STOPPING_REASONS = Object.values(StoppingReason) as StoppingReasonValue[];
export const CEFR_LEVELS = Object.values(CEFRLevel) as CefrLevelValue[];
export const CEFR_CONFIDENCES = Object.values(CEFRConfidence) as CefrConfidenceValue[];
export const SKILLS = Object.values(Skill) as SkillValue[];
export const ITEM_STATUSES = Object.values(ItemStatus) as ItemStatusValue[];
export const ITEM_BATCH_SOURCES = Object.values(ItemBatchSource) as ItemBatchSourceValue[];
