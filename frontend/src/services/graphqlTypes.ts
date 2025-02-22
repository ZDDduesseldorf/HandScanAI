/**
 * This file contains the GraphQL type definitions for the HandScanAI project.
 * The interfaces defined herein are used for handling responses and inputs
 * GraphQL in queries and mutations.
 */

/**
 * Represents the result of the age and gender classification process.
 *
 * @property {string} id - A unique identifier for the scan result.
 * @property {number} minAge - The minimum age predicted.
 * @property {number} maxAge - The maximum age predicted.
 * @property {number} classifiedAge - The final age classification result.
 * @property {number} classifiedGender - The final gender classification result.
 * @property {number} confidenceAge - The confidence score for the age prediction.
 * @property {number} confidenceGender - The confidence score for the gender prediction.
 */
export interface ScanResult {
  id: string;
  minAge: number;
  maxAge: number;
  classifiedAge: number;
  classifiedGender: number;
  confidenceAge: number;
  confidenceGender: number;
}

/**
 * Represents a nearest neighbour record used for reference in the scan result.
 *
 * @property {string} id - A unique identifier for the neighbour record.
 * @property {number} gender - The gender value associated with the neighbour.
 * @property {number} age - The age value associated with the neighbour.
 * @property {string} region - The region information of the neighbour.
 */
export interface NearestNeighbour {
  id: string;
  gender: number;
  age: number;
  region: string;
}

/**
 * Represents the structure of the data returned by the GraphQL query for a scan result.
 *
 * @property {object} getScanResult - The response object containing the classifier result and nearest neighbour info.
 * @property {ScanResult} getScanResult.resultClassifier - The classification result for age and gender.
 * @property {NearestNeighbour[]} getScanResult.nearestNeighbourInfo - An array of nearest neighbour records.
 */
export interface GetScanResultData {
  getScanResult: {
    resultClassifier: ScanResult;
    nearestNeighbourInfo: NearestNeighbour[];
  };
}

/**
 * Represents a scan entry in the system.
 *
 * A scan entry holds the metadata associated with a user's hand scan, including whether
 * an image was provided, actual age and gender (if known), confirmation status, and timestamps.
 *
 * @property {string} id - A unique identifier for the scan entry.
 * @property {boolean} imageExists - Flag indicating whether an image is associated with the entry.
 * @property {number | null} realAge - The actual age of the user (if available).
 * @property {number | null} realGender - The actual gender of the user (if available).
 * @property {boolean} confirmed - Indicates if the scan entry has been confirmed.
 * @property {string} createdAt - Timestamp of when the scan entry was created.
 * @property {string} updatedAt - Timestamp of the last update to the scan entry.
 */
export interface ScanEntry {
  id: string;
  imageExists: boolean;
  realAge: number | null;
  realGender: number | null;
  confirmed: boolean;
  createdAt: string;
  updatedAt: string;
}

/**
 * Represents the data returned by a GraphQL mutation to create a new scan entry.
 *
 * @property {ScanEntry} createScanEntryModel - The newly created scan entry.
 */
export interface CreateScanEntryModelData {
  createScanEntryModel: ScanEntry;
}

/**
 * Represents the data returned by a GraphQL mutation to update an existing scan entry.
 *
 * @property {ScanEntry} updateScanEntryModel - The updated scan entry.
 */
export interface UpdateScanEntryModelData {
  updateScanEntryModel: ScanEntry;
}

/**
 * Represents the data returned by a GraphQL mutation to delete a scan entry.
 *
 * @property {boolean} deleteScanEntryModel - A boolean indicating whether the deletion was successful.
 */
export interface DeleteScanEntryModelData {
  deleteScanEntryModel: boolean;
}

/**
 * Defines the input structure for creating or updating a scan entry.
 *
 * @property {number | null} [realAge] - The actual age of the user.
 * @property {number | null} [realGender] - The actual gender of the user.
 * @property {boolean} [confirmed] - The confirmation status of the scan entry.
 */
export interface ScanEntryInput {
  realAge?: number | null;
  realGender?: number | null;
  confirmed?: boolean;
}

/**
 * Represents the data returned by a GraphQL query to retrieve multiple scan entries.
 *
 * @property {ScanEntry[]} getScanEntryModels - An array of scan entries.
 */
export interface GetScanEntryModelsData {
  getScanEntryModels: ScanEntry[];
}

/**
 * Represents the data returned by a GraphQL query to retrieve a single scan entry.
 *
 * @property {ScanEntry} getScanEntryModel - The requested scan entry.
 */
export interface GetScanEntryModelData {
  getScanEntryModel: ScanEntry;
}
