import { create } from 'zustand';
import { StateCreator } from 'zustand';

interface AppState {
  count: number; // Example state
  increment: () => void; // Example action
}

const storeCreator: StateCreator<AppState> = (set) => ({
  count: 0,
  increment: () =>
    set((state) => ({
      count: state.count + 1,
    })),
});

export const useAppStore = create<AppState>(storeCreator);
