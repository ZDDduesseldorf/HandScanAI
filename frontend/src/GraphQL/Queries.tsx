export interface HandData {
  id: string;
  createdAt: string;
}
import { gql } from '@apollo/client';
export const TEST_QUERY = gql`
  query MyQuery {
    getTestModels {
      id
      createdAt
    }
  }
`;
