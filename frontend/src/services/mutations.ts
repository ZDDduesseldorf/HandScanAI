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

export const UPDATE_SCAN_ENTRY = gql`
  mutation UpdateScanEntry($id: ID!, $input: ScanEntryInput!, $confirmed: Boolean!) {
    updateScanEntryModel(id: $id, input: $input, confirmed: $confirmed) {
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

export const DELETE_SCAN_ENTRY = gql`
  mutation DeleteScanEntry($id: ID!) {
    deleteScanEntryModel(id: $id)
  }
`;
