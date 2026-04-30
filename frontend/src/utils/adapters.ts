export function adaptActivity(raw: any) {
  return {
    ...raw,
    id: String(raw.id),
    creatorId: String(raw.userId),
    tags: typeof raw.tags === 'string' ? raw.tags.split(',').filter(Boolean) : (raw.tags || []),
    fee: Number(raw.fee ?? 0),
    bonusValue: Number(raw.bonusValue ?? 0),
    registeredCount: Number(raw.registeredCount ?? 0),
    maxCount: Number(raw.maxCount ?? 0),
  };
}

export function adaptRegistration(raw: any) {
  return {
    ...raw,
    id: String(raw.id),
    userId: String(raw.userId),
    activityId: String(raw.activityId),
  };
}
