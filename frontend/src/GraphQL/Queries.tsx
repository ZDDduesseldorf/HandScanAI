// import {gql} from '@apollo/client'

// export const LOAD_USERS = gql'
// query{
//     getAllUsers{
//         Id
//         firstName
//         email
//         password
//     }
// }
// '
// import { gql } from '@apollo/client';

// export const TEST_QUERY = gql`
//   query TestQuery {
//     exampleField
//   }
// `;
import { gql } from '@apollo/client';
export const TEST_QUERY = gql`
  query MyQuery {
    getTestModels {
      id
      createdAt
    }
  }
`;
