import { gql } from '@apollo/client';

export const CREATE_SCAN_ENTRY = gql`
  mutation CreateScanEntry {
    createScanEntryModel {
      id
      imageExists
      realAge
      realGender
      confirmed
      createdAt
      updatedAt
    }
  }
`;
