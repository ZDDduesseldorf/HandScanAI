//external imports
import { gql } from '@apollo/client';

/**
 * This file defines the GraphQL mutations used in the HandScanAI project.
 */


/**
 * GraphQL mutation to create a new scan entry.
 *
 * This mutation does not require any input parameters and returns the newly created scan entry model.
 *
 * The returned scan entry includes:
 * - id: Unique identifier for the scan entry.
 * - imageExists: Boolean indicating whether an image is associated with the entry.
 * - realAge: The actual age provided (if any).
 * - realGender: The actual gender provided (if any).
 * - confirmed: Confirmation status of the scan entry.
 * - createdAt: Timestamp when the scan entry was created.
 * - updatedAt: Timestamp when the scan entry was last updated.
 */
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

/**
 * GraphQL mutation to update an existing scan entry.
 *
 * This mutation requires the ID of the scan entry to update and an input object containing
 * the fields to be updated (of type ScanEntryInput).
 *
 * The returned scan entry includes updated values for:
 * - id: Unique identifier for the scan entry.
 * - imageExists: Boolean indicating image presence.
 * - realAge: Updated real age value.
 * - realGender: Updated real gender value.
 * - confirmed: Updated confirmation status.
 * - createdAt: Creation timestamp (unchanged).
 * - updatedAt: Updated timestamp for the scan entry.
 *
 * @param {ID!} id - The unique identifier of the scan entry.
 * @param {ScanEntryInput!} input - The input object containing fields to update.
 */
export const UPDATE_SCAN_ENTRY = gql`
  mutation UpdateScanEntry($id: ID!, $input: ScanEntryInput!) {
    updateScanEntryModel(id: $id, input: $input) {
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
 * GraphQL mutation to delete an existing scan entry.
 *
 * This mutation requires the ID of the scan entry to be deleted and returns a boolean value
 * indicating whether the deletion was successful.
 *
 * @param {ID!} id - The unique identifier of the scan entry to delete.
 */
export const DELETE_SCAN_ENTRY = gql`
  mutation DeleteScanEntry($id: ID!) {
    deleteScanEntryModel(id: $id)
  }
`;
