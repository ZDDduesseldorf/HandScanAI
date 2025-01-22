import { gql, useMutation } from '@apollo/client';

export interface HandData {
  classifiedAge: number;
  classifiedGender: number;
  confidenceAge: number;
  confidenceGender: number;
  id: string;
}

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
