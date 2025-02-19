import { create } from 'zustand';
import { StateCreator } from 'zustand';
import {
  ScanResult,
  ScanEntry,
  NearestNeighbour,
} from '@/services/graphqlTypes';

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

export const useAppStore = create<AppState>(storeCreator);
