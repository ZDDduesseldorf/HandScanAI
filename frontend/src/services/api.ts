//external imports
import { ApolloClient, InMemoryCache, HttpLink, from } from '@apollo/client';
import { onError } from '@apollo/client/link/error';

/**
 * Error link to handle and log GraphQL and network errors.
 * @see https://www.apollographql.com/docs/react/api/link/apollo-link-error/
 */
const errorLink = onError(({ graphQLErrors, networkError }) => {
  if (graphQLErrors) {
    graphQLErrors.forEach(({ message, locations, path }) => {
      console.error(`[GraphQL error]: Message: ${message}`);
      if (locations) {
        console.error(
          `[GraphQL error]: Locations: ${locations.map((loc) => JSON.stringify(loc)).join(', ')}`,
        );
      }
      if (path) {
        console.error(`[GraphQL error]: Path: ${path.join(' -> ')}`);
      }
    });
  }
  if (networkError && networkError instanceof Error) {
    console.error(`[Network error]: ${networkError.message}`);
  }
});

/**
 * GraphQL endpoint URI.
 *
 * Retrieves the GraphQL endpoint from the environment variable VITE_GRAPHQL_ENDPOINT.
 * If the environment variable is not defined, it falls back to the default URI: 'http://localhost:8000/graphql'.
 */
const graphqlUri =
  import.meta.env.VITE_GRAPHQL_ENDPOINT || 'http://localhost:8000/graphql';

// Warn the developer if the VITE_GRAPHQL_ENDPOINT environment variable is missing.
if (!import.meta.env.VITE_GRAPHQL_ENDPOINT) {
  console.warn(
    'VITE_GRAPHQL_ENDPOINT is not defined in the environment variables. Falling back to default: http://localhost:8000/graphql',
  );
}

/**
 * Combined Apollo Link chain.
 *
 * The `from` function composes multiple links into a single link chain.
 * Here, it first applies the errorLink to handle errors before using the HttpLink to send requests.
 */
const link = from([errorLink, new HttpLink({ uri: graphqlUri })]);

/**
 * Apollo Client instance for interacting with the GraphQL API.
 *
 * Configured with:
 * - An in-memory cache for efficient data caching.
 * - A link chain that includes error handling and HTTP communication.
 *
 * @see https://www.apollographql.com/docs/react/api/core/ApolloClient/
 */
const client = new ApolloClient({
  cache: new InMemoryCache(),
  link,
});

export default client;
