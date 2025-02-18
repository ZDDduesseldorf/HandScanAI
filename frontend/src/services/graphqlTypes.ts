export interface ScanResult {
  id: string;
  minAge: number;
  maxAge: number;
  classifiedAge: number;
  classifiedGender: number;
  confidenceAge: number;
  confidenceGender: number;
}

export interface GetScanResultData {
  getScanResult: {
    resultClassifier: ScanResult;
  }
}

export interface ScanEntry {
  id: string;
  imageExists: boolean;
  realAge: number | null;
  realGender: number | null;
  confirmed: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface CreateScanEntryModelData {
  createScanEntryModel: ScanEntry;
}

export interface UpdateScanEntryModelData {
  updateScanEntryModel: ScanEntry;
}

export interface DeleteScanEntryModelData {
  deleteScanEntryModel: boolean;
}

export interface ScanEntryInput {
  realAge?: number | null;
  realGender?: number | null;
  confirmed?: boolean;
}

export interface GetScanEntryModelsData {
  getScanEntryModels: ScanEntry[];
}

export interface GetScanEntryModelData {
  getScanEntryModel: ScanEntry;
}
