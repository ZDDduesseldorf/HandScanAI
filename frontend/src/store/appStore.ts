//external imports
import { create } from 'zustand';
import { StateCreator } from 'zustand';

//internal imports
import {
  ScanResult,
  ScanEntry,
  NearestNeighbour,
} from '@/services/graphqlTypes';

/**
 * Interface representing the state of HandScanAI.
 *
 * @property {ScanEntry | null} scanEntry - The current hand scan entry, or null if not set.
 * @property {ScanResult | null} scanResult - The result of the current hand scan, or null if not set.
 * @property {string | null} capturedImage - A URL pointing to the captured image, or null if not set.
 * @property {NearestNeighbour[] | null} nearestNeighbours - An array of nearest neighbour data, or null if not set.
 * @property {(entry: ScanEntry) => void} setScanEntry - Function to update the scan entry in the state.
 * @property {(data: ScanResult) => void} setScanResult - Function to update the scan result in the state.
 * @property {(image: string) => void} setCapturedImage - Function to update the captured image in the state.
 * @property {(data: NearestNeighbour[]) => void} setNearestNeighbours - Function to update the nearest neighbours in the state.
 */
interface AppState {
  scanEntry: ScanEntry | null;
  scanResult: ScanResult | null;
  capturedImage: string | null;
  nearestNeighbours: NearestNeighbour[] | null;
  setScanEntry: (entry: ScanEntry) => void;
  setScanResult: (data: ScanResult) => void;
  setCapturedImage: (image: string) => void;
  setNearestNeighbours: (data: NearestNeighbour[]) => void;
}

/**
 * Zustand store creator function.
 *
 * This function initializes the state with default values (null) for all properties and provides setter functions
 * that update the corresponding state values using Zustand's immutable update pattern.
 *
 * Each setter function calls the `set` method to replace the previous value with the new value passed as an argument.
 *
 * @param set - The function provided by Zustand to update state.
 * @returns The initial state of the application along with the state updater functions.
 */
const storeCreator: StateCreator<AppState> = (set) => ({
  scanEntry: null,
  setScanEntry: (entry) =>
    set(() => ({
      scanEntry: entry,
    })),
  scanResult: null,
  setScanResult: (data) =>
    set(() => ({
      scanResult: data,
    })),
  capturedImage: null,
  setCapturedImage: (image) =>
    set(() => ({
      capturedImage: image,
    })),
  nearestNeighbours: null,
  setNearestNeighbours: (data) =>
    set(() => ({
      nearestNeighbours: data,
    })),
});

/**
 * The application store hook.
 *
 * This Zustand store hook (`useAppStore`) can be imported and used within any component to access
 * and modify the state of HandScanAI.
 */
export const useAppStore = create<AppState>(storeCreator);
