// Authorization token that must have been created previously. See : https://developer.spotify.com/documentation/web-api/concepts/authorization
const token = 'BQByBXH1kV8AVgGBwfp5g3Uq8C77KpuPWeMBbUuBwyVywKo1gnv7wQdwmsmUn7OHa5_8J4s-ucvuKoEizGN2PnF50i_ORehtBScRw_6GXxPy__ehFbR7itQCxgAtJp6-qMn4yAU_GNKwAs59SaL4f1Z657_8ZHIdUJVjarK1cMLdSyLv6PRlaiX2qV7sTZydBOYMHeYD_Kps1ORLxygTKz61DfQjB8VA9G0pefqecbVmzLvKmbftItrEe1iuedHhgQuDzn-eIu3srUOx17Y-VETKpFeYYvszIIHH3GrYc1I4xZhZNHJJ3z6zbkdufGqH';
async function fetchWebApi(endpoint, method, body) {
  const res = await fetch(`https://api.spotify.com/${endpoint}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    method,
    body:JSON.stringify(body)
  });
  return await res.json();
}

async function getTopTracks(){
  // Endpoint reference : https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
  return (await fetchWebApi(
    'v1/me/top/tracks?time_range=long_term&limit=20', 'GET'
  )).items;
}

const topTracks = await getTopTracks();
console.log(
  topTracks?.map(
    ({name, artists}) =>
      `${name} by ${artists.map(artist => artist.name).join(', ')}`
  )
);