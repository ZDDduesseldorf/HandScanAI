import { gql } from '@apollo/client';

export const GET_SCAN_RESULT = gql`
  query GetScanResult($id: ID!) {
    getScanResult(id: $id) {
      resultClassifier {
      classifiedAge
      classifiedGender
      confidenceAge
      confidenceGender
      id
      maxAge
      minAge
    }
    }
  }
`;

export const GET_SCAN_ENTRY_MODELS = gql`
  query GetScanEntryModels {
    getScanEntryModels {
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

export const GET_SCAN_ENTRY_MODEL = gql`
  query GetScanEntryModel($id: ID!) {
    getScanEntryModel(id: $id) {
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
