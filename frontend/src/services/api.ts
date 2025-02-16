import { ApolloClient, InMemoryCache, HttpLink, from } from '@apollo/client';
import { onError } from '@apollo/client/link/error';

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

const graphqlUri =
  import.meta.env.VITE_GRAPHQL_ENDPOINT || 'http://localhost:8000/graphql';

if (!import.meta.env.VITE_GRAPHQL_ENDPOINT) {
  console.warn(
    'VITE_GRAPHQL_ENDPOINT is not defined in the environment variables. Falling back to default: http://localhost:8000/graphql',
  );
}

const link = from([errorLink, new HttpLink({ uri: graphqlUri })]);

const client = new ApolloClient({
  cache: new InMemoryCache(),
  link,
});

export default client;
