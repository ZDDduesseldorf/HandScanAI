import { create } from 'zustand';
import { StateCreator } from 'zustand';
import { HandData, ScanEntry } from '@/services/graphqlTypes';

interface AppState {
  scanEntry: ScanEntry | null;
  handData: HandData | null;
  setScanEntry: (entry: ScanEntry) => void;
  setHandData: (data: HandData) => void;
}

const storeCreator: StateCreator<AppState> = (set) => ({
  scanEntry: null,
  setScanEntry: (entry) =>
    set(() => ({
      scanEntry: entry,
    })),
  handData: null,
  setHandData: (data) =>
    set(() => ({
      handData: data,
    })),
});

export const useAppStore = create<AppState>(storeCreator);
