export interface HandData {
  classifiedGender: number;
  confidenceAge: number;
  confidenceGender: number;
  id: string;
}
import { gql } from '@apollo/client';
// export const TEST_QUERY = gql`
//   query MyQuery {
//     getTestModels {
//       id
//       createdAt
//     }
//   }
// `;

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
