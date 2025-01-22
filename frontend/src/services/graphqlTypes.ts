export interface HandData {
  classifiedAge: number;
  classifiedGender: number;
  confidenceAge: number;
  confidenceGender: number;
  id: string;
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
