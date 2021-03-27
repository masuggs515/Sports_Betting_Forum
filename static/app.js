async function processCommentForm(e) {
  e.preventDefault();

  let text = $("#Comment").val();
  const url = window.location.href;
  const game_id = url.split('game')[1];
  const commentData = await axios.post(`/game${game_id}`, {
    text
  });
  $('#comment-form').trigger("reset")
  handleCommentResponse(commentData);
}

function handleCommentResponse(commentData) {
  if (commentData.data.error) {
    const errorHtml = `<p class="text-center m-2 alert alert-danger">${commentData.data.error}</p>`
    $('#comment-error').html(errorHtml)
  } else {
    const comment = commentData.data.text;
    const time = commentData.data.timestamp;
    const username = commentData.data.username;
    const user_image = commentData.data.user_image;
    const comment_id = commentData.data.comment_id;
    let commentHtml = `
                <div id="${comment_id}" class="bg-dark-blue border-green mt-4 px-3 pt-2 text-justify float-left">
                    <img src=${user_image} alt="" class="rounded-circle" width="35" height="35">
                    <h4 class="d-inline mx-2">${username}</h4>
                    <span class="float-end"><small>${time}</small></span>
                            <span class="pt-2"><i class="likes d-inline bg-dark-blue text-light-grey float-end far fa-thumbs-up me-2"></i></span>
                            <button type="submit" id="delete-comment" class="float-end btn btn-sm bg-dark-blue text-light-grey border border-light rounded-3 me-2">
                            Delete comment <i class="fa fa-trash"></i></button>
                    <br>
                    <p class="mx-4 mt-2">${comment}</p>
                </div>
                `
    $('#comment-section').prepend(commentHtml)
    $('#no-comments').remove()
  }
}


$('#comment-form').on('submit', processCommentForm);

$('body').on("click", deleteComment)

async function deleteComment(e) {
  if (e.target.id == "delete-comment") {
    comment_id = $(e.target).parent().attr('id');
    $(e.target).parent().remove();
    await axios.delete(`/comment/${comment_id}/delete`)
  }
}

$('body').on("click", async function (e) {
  if ($(e.target).hasClass('likes')) {
    const comment_id = $(e.target).parent().parent().attr('id');
    if ($(e.target).hasClass('far')) {

      await axios.post('/comment/add_like', {
        comment_id
      })

      $(e.target).addClass('fas').removeClass('far')

    } else {
      $(e.target).addClass('far').removeClass('fas')

      await axios.post('/comment/remove_like', {
        "comment_id": comment_id
      })
    }
  }
})