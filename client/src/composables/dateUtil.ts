const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone

export function formattedDatePart(date: Date): string {
  return date.toLocaleString("fi-FI", {
    timeZone: timezone,
    day: "numeric",
    month: "numeric",
  })
}

export function formattedTimePart(date: Date): string {
  return date.toLocaleTimeString(undefined, {
    timeZone: timezone,
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  })
}
