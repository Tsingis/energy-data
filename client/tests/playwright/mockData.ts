export const MOCK_NOW = new Date("2025-05-01T12:00:00Z")
const HOURS_RANGE = 2
const MINUTES_INTERVAL = 15

function generateTimestamps(
  hoursRange: number,
  minutesInterval: number
): string[] {
  const timestamps: string[] = []
  const totalIntervals = (hoursRange * 2 * 60) / minutesInterval

  for (let i = 0; i <= totalIntervals; i++) {
    const time = new Date(MOCK_NOW)
    const minutesOffset = (i - totalIntervals / 2) * minutesInterval
    time.setMinutes(time.getMinutes() + minutesOffset, 0, 0)
    timestamps.push(time.toISOString())
  }

  return timestamps
}

const timestamps = generateTimestamps(HOURS_RANGE, MINUTES_INTERVAL)

export const mockEnergyData = {
  "74": timestamps.map((timestamp) => ({
    timestamp,
    value:
      2800 + Math.sin((new Date(timestamp).getHours() / 12) * Math.PI) * 100,
  })),
  "241": timestamps.map((timestamp) => ({
    timestamp,
    value:
      2850 + Math.sin((new Date(timestamp).getHours() / 12) * Math.PI) * 50,
  })),
  "193": timestamps.map((timestamp) => ({
    timestamp,
    value:
      2600 + Math.sin((new Date(timestamp).getHours() / 12) * Math.PI) * 100,
  })),
  "165": timestamps.map((timestamp) => ({
    timestamp,
    value:
      2650 + Math.sin((new Date(timestamp).getHours() / 12) * Math.PI) * 50,
  })),
}

const hourlyTimestamps = generateTimestamps(HOURS_RANGE, 60)
export const mockPriceData = hourlyTimestamps.map((timestamp) => ({
  timestamp,
  value: 5 + Math.sin((new Date(timestamp).getHours() / 12) * Math.PI) * 1.5,
}))
