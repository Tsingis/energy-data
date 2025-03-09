export enum DatasetKeys {
  Production = "74",
  ProductionPrediction = "241",
  Consumption = "193",
  ConsumptionPrediction = "165",
}

// Step 2: Map the dataset keys to their respective labels and colors
export const DATASET_LABELS: Record<DatasetKeys, string> = {
  [DatasetKeys.Production]: "Production",
  [DatasetKeys.ProductionPrediction]: "Production - prediction",
  [DatasetKeys.Consumption]: "Consumption",
  [DatasetKeys.ConsumptionPrediction]: "Consumption - prediction",
}

export const DATASET_COLORS: Record<DatasetKeys, string> = {
  [DatasetKeys.Production]: "rgb(0, 86, 179)",
  [DatasetKeys.ProductionPrediction]: "rgb(102, 179, 255)",
  [DatasetKeys.Consumption]: "rgb(179, 0, 0)",
  [DatasetKeys.ConsumptionPrediction]: "rgb(216, 82, 82)",
}
