import { create } from 'zustand';
import { StateCreator } from 'zustand';
import { ScanEntry } from '@/services/graphqlTypes';

interface AppState {
    scanEntry: ScanEntry | null;
    setScanEntry: (entry: ScanEntry) => void;
}

const storeCreator: StateCreator<AppState> = (set) => ({
    scanEntry: null,
    setScanEntry: (entry) =>
        set(() => ({
            scanEntry: entry,
        })),
});

export const useAppStore = create<AppState>(storeCreator);
