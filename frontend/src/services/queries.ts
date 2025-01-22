import { gql } from '@apollo/client';


export const GET_SCAN_RESULT = gql`
  query GetScanResult($id: ID!) {
    getScanResult(id: $id) {
      classifiedAge
      classifiedGender
      confidenceAge
      confidenceGender
      minAge
      maxAge
      id
    }
  }
`;
