const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone

export function formattedDate(date: Date): string {
  return date.toLocaleString("fi-FI", {
    timeZone: timezone,
    day: "numeric",
    month: "numeric",
  })
}

export function formattedTime(date: Date): string {
  return date.toLocaleTimeString(undefined, {
    timeZone: timezone,
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  })
}

export function formattedDateTime(date: Date): string {
  const datePart = formattedDate(date)
  const timePart = formattedTime(date)
  return `${datePart} ${timePart}`
}
