console.log('scrabble.js imported successfully.')

// Named DOM elements
const BOARD = document.querySelector('.board');
const USER_LETTERS = document.querySelector('#letters')
const FOUND_WORDS_LIST = document.querySelector('.found_words')
const ACROSS_BTN = document.querySelector('#across_btn')
const DOWN_BTN = document.querySelector('#down_btn')


// Generate 15*15 sqaures in board and assign unique id
for (let x = 0; x < 15; x++) {
    for (let y = 0; y < 15; y++) {
        let square = document.createElement('span');
        square.classList.add('square');
        square.id = `coord-${x + 1}-${y + 1}`;
        square.textContent = `.`; // hack to get spacing right 
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

function getBoardDict(){
    let board_dict = {}
    for (let x = 0; x < 225; x++){
        // console.log(BOARD.childNodes[x].textContent)
        board_dict[x] = BOARD.childNodes[x].textContent
    }
    return board_dict
}


// USER LETTERS
FOUND_WORDS_LIST.textContent = 'Enter your letters below to see what words you can make.'
function lettersChange(e) {
    board_dict = getBoardDict()     
    let userLetters = USER_LETTERS.value
    let json_body = {'userLetters': userLetters, 'board_dict': board_dict}
    // let allLetters = stringify(userLetters) + stringify(board_dict)
    // console.log(userLetters)
    fetch(`${window.origin}/`, {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify(json_body),
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

// Down & Across buttons
let play_down = false
let play_across = true
ACROSS_BTN.classList.add('clicked')
DOWN_BTN.addEventListener('click', (e) => {
    play_down = true;
    play_across = false;
    ACROSS_BTN.classList.remove('clicked')
    DOWN_BTN.classList.add('clicked')
})
ACROSS_BTN.addEventListener('click', (e) => {
    play_down = false;
    play_across = true;
    ACROSS_BTN.classList.add('clicked')
    DOWN_BTN.classList.remove('clicked')
})

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
            if (play_across && id[1] < 15) {
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
            if (play_across && id[1] > 1) {
                let new_coord = `#coord-${id[0]}-${parseInt(id[1]) - 1}`
                targetTile.classList.remove('selectedSquare')
                targetTile.classList.remove('typed_square')
                targetTile.textContent = '.'
                targetTile = document.querySelector(new_coord)
                targetTile.classList.add('selectedSquare')
            } if (play_across && id[1] == 1) { // if leftmost square
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

