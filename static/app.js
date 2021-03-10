const BASE_URL = 'https://api.the-odds-api.com/'
const API_KEY = '0fdc02bed86bc36fe82801e9ef8b7a2e'



async function allOdds(){
    let res = await axios.get(`${BASE_URL}v3/odds/`, {params: 
        {apiKey: API_KEY,
        sport: 'upcoming',
        region: 'us'}})
        console.log(res.data.data)
    const games = res.data.data;
    for(let game in games){
        const gameTeams = games[game].teams;
        const homeTeam = games[game].home_team;
        console.log(gameTeams)
        console.log(homeTeam)

    }
}

$('#odds').on('click', allOdds)