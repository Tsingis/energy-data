export type EnergyModel = {
  timestamp: string
  value: number
}

export type EnergyData = {
  data: {
    [key: string]: EnergyModel[]
  }
}

export type PriceModel = {
  timestamp: string
  value: number
}

export type PriceData = {
  data: PriceModel[]
}

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
  minValue: number
}
