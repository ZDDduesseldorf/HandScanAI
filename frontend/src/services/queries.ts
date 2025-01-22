import { gql } from '@apollo/client';


export const HandScanResultQuery = gql`
  query MyQuery {
    getScanResult(id: "5274cc1e-6413-4653-b14f-a4fcba138c99") {
      classifiedAge
      classifiedGender
      confidenceAge
      confidenceGender
      id
    }
  }
`;
