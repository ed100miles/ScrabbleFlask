console.log('scrabble.js imported successfully.')

const BOARD = document.querySelector('.board');
const USER_LETTERS = document.querySelector('#letters')
const FOUND_WORDS_LIST = document.querySelector('.found_words')

// Generate 15*15 sqaures in board and assign unique id
for (let x = 0; x < 15; x++) {
    for (let y = 0; y < 15; y++) {
        let square = document.createElement('span');
        square.classList.add('square');
        square.id = `coord-${x + 1}-${y + 1}`;
        square.textContent = `.`; //${x+1}
        BOARD.appendChild(square);
    }
}

// Initialize targetTile to centre of board
let targetTile = document.querySelector('#coord-8-8')
targetTile.classList.add('selectedSquare')

// Function to add selectedSquare class to clicked tile and remove from old
function boardClick(e) {
    targetTile.classList.remove('selectedSquare') // remove styling from old target
    targetTile = document.querySelector(`#${e.target.id}`)// update target
    targetTile.classList.add('selectedSquare') // add the styling
}
BOARD.addEventListener('click', boardClick)

// USER LETTERS
function lettersChange(e) {
    let userLetters = USER_LETTERS.value
    fetch(`${window.origin}/`, {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify(userLetters),
        cache: 'no-cache',
        headers: new Headers({
            'content-type': 'application/json'
        })
    })
    .then(function(response){
        response.json().then(function(data){
            // console.log( new Date())
            FOUND_WORDS_LIST.textContent = ''
            for (const [key, value] of Object.entries(data)) {
                let word = document.createElement('div')
                // word.classList.add('found_word')
                word.textContent = `${key}` 
                FOUND_WORDS_LIST.appendChild(word)
                // console.log(key, value);
              }
        })
    })
}

USER_LETTERS.addEventListener('keyup', lettersChange)

