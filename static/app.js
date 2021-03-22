const BASE_URL = 'https://api.the-odds-api.com/'
const API_KEY = '0fdc02bed86bc36fe82801e9ef8b7a2e'
const COMMENT_URL = '/'

async function processCommentForm(e) {
    e.preventDefault();
  
    let text = $("#Comment").val();
    
    const commentData = await axios.post(COMMENT_URL, {
      text
    });
    
    handleResponse(commentData)
}

function handleCommentResponse(commentData){

}


// $('comment_form').on('submit', processCommentForm)