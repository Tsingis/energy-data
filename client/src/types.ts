export type EnergyModel = {
  timestamp: string
  value: number
}

export type EnergyData = {
  data: {
    [key: string]: EnergyModel[]
  }
}
