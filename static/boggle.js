const $board = $('#game');
const words = new Set();
const $msg = $('.msg')
let score = 0;

// Handler for word submission
async function handleWordSubmit(e) {
    e.preventDefault();

    //input
    const $word = $('.word', $board);

    //input value
    let word = $word.val();

    //if input is blank do nothing
    if (!word) {
        return;
    }

    //if word already submitted do nothing
    if (words.has(word)) {
        showMessage(`${word} already submitted`, "err");
        $word.val('').focus();
        return;
    }

    //Axios request to check word against dictionary of words
    const res = await axios.get('/check-word', {params: {word: word}});

    //check word and respond with message about word status
    if (res.data.result === 'not-word') {
        showMessage(`${word} is not a word`, "err");
    } else if (res.data.result === 'not-on-board') {
        showMessage(`${word} is not on this game board`, "err");
    } else {
        showWord(word);
        score += word.length;
        showScore();
        words.add(word);
        showMessage(`Added: ${word} | Worth ${word.length} points!`, 'ok');
    }

    $word.val('').focus();
}

$('.add-word', $board).on('submit', handleWordSubmit);

function showMessage(msg, cls) {
    $($msg, $board).text(msg).removeClass().addClass(`msg-${cls}`);

}

function showWord(word) {
    $('.words', $board).append($('<li>', {text: word}));
}

function showScore() {
    $('.score', $board).text(score);
}

async function scoreGame() {
    $('.add-word', $board).hide();
    const res = await axios.post('/game-over', {score: score});
    if (res.data.newRecord) {
        showMessage(`New Highscore: ${score}`, 'ok');
        // $('.highscore').text(score);
    } else {
        showMessage(`Final Score: ${score}`, 'ok');
    }

    $('.reset').removeAttr("hidden");
    $('body').addClass('ender');
    $('table').addClass("hide");
    $('ul').addClass("hide");
}

const timer = setInterval(countDown, 1000);
let time = 60;

function Timer() {
    $('.timer', $board).text(time);
}

async function countDown() {
    time -= 1;
    Timer();

    if (time === 0) {
        clearInterval(timer);
        await scoreGame();
    }
}