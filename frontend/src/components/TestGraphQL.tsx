import React, { useEffect, useState } from 'react';
import { useQuery, gql } from '@apollo/client';
import { TEST_QUERY } from '../GraphQL/Queries';

function GetModels() {
  const { error, loading, data } = useQuery(TEST_QUERY);
  const [models, setModels] = useState([]);
  useEffect(() => {
    console.log(data);
    if (data) {
      setModels(data.getTestModels);
    }
  }, [data]);

  return (
    <div>
      {/* {" "}
      {users.map((val) => {
        return <h1> {val.firstName}</h1>;
      })} */}
    </div>
  );
}

export default GetModels;
