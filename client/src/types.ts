export type EnergyModel = {
  timestamp: string
  value: number
}

export type EnergyData = {
  [key: string]: EnergyModel[]
}

export type PriceModel = {
  timestamp: string
  value: number
}

export type PriceData = PriceModel[]

export type Dataset = {
  label: string
  data: { x: number; y: number }[]
  borderColor: string
  backgroundColor: string
  borderWidth: number
  fill: boolean
  borderDash?: number[]
  yAxisID?: string
}

export type ChartData = {
  labels: string[]
  datasets: Dataset[]
  minTimestamp: Date | null
  maxTimestamp: Date | null
}
