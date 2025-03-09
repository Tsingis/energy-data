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
