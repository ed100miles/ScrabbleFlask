console.log('scrabble.js imported successfully.')

const BOARD = document.querySelector('.board');
const USER_LETTERS = document.querySelector('#letters')
const FOUND_WORDS_LIST = document.querySelector('.found_words')

let play_down = true
let play_accross = false

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
    if (e.target.id != '') {
        targetTile.classList.remove('selectedSquare') // remove styling from old target
        targetTile = document.querySelector(`#${e.target.id}`)// update target
        targetTile.classList.add('selectedSquare') // add the styling
    }
}
BOARD.addEventListener('click', boardClick)

// USER LETTERS
FOUND_WORDS_LIST.textContent = 'Enter your letters below to see what words you can make.'
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
        .then(function (response) {
            response.json().then(function (data) {
                // console.log( new Date())
                FOUND_WORDS_LIST.textContent = `${Object.keys(data).length} possible words:`
                for (const [key, value] of Object.entries(data)) {
                    let word = document.createElement('div')
                    // word.classList.add('found_word')
                    word.textContent = `${key}`
                    FOUND_WORDS_LIST.appendChild(word)
                }
                if (Object.keys(data).length == 0) {
                    FOUND_WORDS_LIST.textContent = 'Enter your letters below to see what words you can make.'
                }
            })
        })
}

USER_LETTERS.addEventListener('keyup', lettersChange)

// Board typing:
// TODO: DRY this out!!!!!!!!!!!!!!!!!!!!!!!!!!!!

function boardType(e) {
    if (document.activeElement.id !== 'letters') {
        let id = targetTile.id.slice(6).split('-')
        let typed_letter = String.fromCharCode(e.which)
        if (/^[a-zA-Z]/.test(typed_letter)) {        // check is letter
            targetTile.textContent = typed_letter
            targetTile.classList.add('typed_square')
            targetTile.classList.remove('selectedSquare')
            // assign new target tile
            if (play_accross && id[1] < 15) {
                let new_coord = `#coord-${id[0]}-${parseInt(id[1]) + 1}`
                targetTile = document.querySelector(new_coord)
                targetTile.classList.add('selectedSquare')
            }
            if (play_down && id[0] < 15) {
                let new_coord = `#coord-${parseInt(id[0]) + 1}-${id[1]}`
                targetTile = document.querySelector(new_coord)
                targetTile.classList.add('selectedSquare')
            }
        }
        else if (e.which == 8) { // if backspace pressed
            if (play_accross && id[1] > 1) {
                let new_coord = `#coord-${id[0]}-${parseInt(id[1]) - 1}`
                targetTile.classList.remove('selectedSquare')
                targetTile.classList.remove('typed_square')
                targetTile.textContent = '.'
                targetTile = document.querySelector(new_coord)
                targetTile.classList.add('selectedSquare')
            } if (play_accross && id[1] == 1) { // if leftmost square
                targetTile.textContent = '.'
                targetTile.classList.remove('selectedSquare')
                targetTile.classList.remove('typed_square')
                targetTile = document.querySelector('#coord-8-8')
                targetTile.classList.add('selectedSquare')
            } if (play_down && id[0] > 1) {
                let new_coord = `#coord-${parseInt(id[0]) - 1}-${id[1]}`
                targetTile.classList.remove('selectedSquare')
                targetTile.classList.remove('typed_square')
                targetTile.textContent = '.'
                targetTile = document.querySelector(new_coord)
                targetTile.classList.add('selectedSquare')
            } if (play_down && id[0] == 1) { // if leftmost square
                targetTile.textContent = '.'
                targetTile.classList.remove('selectedSquare')
                targetTile.classList.remove('typed_square')
                targetTile = document.querySelector('#coord-8-8')
                targetTile.classList.add('selectedSquare')
            }
        }
    }
}
document.addEventListener('keyup', boardType)

