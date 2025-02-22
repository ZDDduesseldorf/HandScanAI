//external imports
import { gql } from '@apollo/client';

/**
 * This file contains the GraphQL queries for the HandScanAI project.
 */

/**
 * GraphQL query to retrieve the scan result for a specific scan entry.
 *
 * The query expects an ID as input and returns:
 * - resultClassifier: The classification details, including classified age, classified gender,
 *   confidence scores, and age boundaries.
 * - nearestNeighbourInfo: An array of nearest neighbour records used for reference.
 *
 * @param {ID!} id - The unique identifier of the scan entry.
 */
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
      nearestNeighbourInfo {
        id
        gender
        age
        region
      }
    }
  }
`;

/**
 * GraphQL query to retrieve all scan entry models.
 *
 * This query does not require any parameters and returns an array of scan entries.
 * Each scan entry includes details such as image existence, real age, real gender, confirmation status, and timestamps.
 */
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

/**
 * GraphQL query to retrieve a single scan entry model by its ID.
 *
 * The query expects an ID as input and returns the scan entry model with corresponding details:
 * - id, imageExists, realAge, realGender, confirmed, createdAt, and updatedAt.
 *
 * @param {ID!} id - The unique identifier of the scan entry.
 */
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
