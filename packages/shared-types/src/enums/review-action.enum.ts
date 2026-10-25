/** Hành động ghi vết của ItemReviewEvent (nhật ký kiểm toán lô/gói). */
export enum ReviewAction {
  APPROVE = 'APPROVE',
  REJECT = 'REJECT',
  CONFIRM = 'CONFIRM',
  REMOVE = 'REMOVE',
  CONFIRM_ALL = 'CONFIRM_ALL',
  IMPORT = 'IMPORT',
  REASSIGN = 'REASSIGN',
  EXTEND = 'EXTEND',
  FORCE_SEND = 'FORCE_SEND',
  ACCEPT_FLAG = 'ACCEPT_FLAG',
}
