import React, { createContext, useContext, useState, ReactNode } from 'react';
import { HandData } from '../GraphQL/Queries';

// Define the structure of the context's value.
// It includes:
// - `handData`: the stored data or null if nothing is set.
// - `setHandData`: a function to update the `handData`.
interface DataContextType {
  handData: HandData | null;
  setHandData: React.Dispatch<React.SetStateAction<HandData | null>>;
}

// Create the context to store the data.
// Initial value is `undefined` to ensure proper error handling when the context is not provided.
const DataContext = createContext<DataContextType | undefined>(undefined);

// Create a provider component to wrap the parts of your app that need access to the context.
export const DataProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  // Use React's `useState` to manage the `handData` state within the provider.
  const [handData, setHandData] = useState<HandData | null>(null);

  return (
    <DataContext.Provider value={{ handData, setHandData }}>
      {children}
    </DataContext.Provider>
  );
};

// Hook for accessing the context.
export const useDataContext = () => {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error('useDataContext must be used within a DataProvider');
  }
  return context;
};
