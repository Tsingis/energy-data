const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone

export function formattedDate(date: Date): string {
  return date.toLocaleString("en-US", {
    timeZone: timezone,
    day: "numeric",
    month: "short",
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

export function formattedDateTime(
  date: Date,
  newLine: boolean = false
): string {
  const datePart = formattedDate(date)
  const timePart = formattedTime(date)
  return newLine ? `${datePart} \n ${timePart}` : `${datePart} ${timePart}`
}
