console.log('scrabble.js imported successfully.')

// Named DOM elements
const BOARD = document.querySelector('.board');
const USER_LETTERS = document.querySelector('#letters')
const FOUND_WORDS_LIST = document.querySelector('.found_words_list')
const FOUND_WORDS_HEADER = document.querySelector('.found_words_header')
const ACROSS_BTN = document.querySelector('#across_btn')
const DOWN_BTN = document.querySelector('#down_btn')
const DEFINITION_CONTAINER = document.querySelector('.definition_container')

// Get words fetch request:
function lettersChange(e) {
    controller.abort()
    controller = new AbortController()

    function getBoardDict() {
        let board_dict = {}
        for (let x = 0; x < 225; x++) {
            // console.log(BOARD.childNodes[x].textContent)
            board_dict[x] = BOARD.childNodes[x].textContent
        }
        return board_dict
    }
    board_dict = getBoardDict()
    let userLetters = USER_LETTERS.value
    let json_body = { 'userLetters': userLetters, 'board_dict': board_dict }
    // let allLetters = stringify(userLetters) + stringify(board_dict)
    // console.log(userLetters)
    
    fetch(`${window.origin}/`, {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify(json_body),
        cache: 'no-cache',
        signal: controller.signal,
        headers: new Headers({
            'content-type': 'application/json'
        })
    })
        .then(function (response) {
            response.json().then(function (data) {
                word_count = 0
                FOUND_WORDS_LIST.textContent = ''
                possible_words_dict = {}
                for (const [key, value] of Object.entries(data)) {
                    let score = key
                    // value is a list of (word, definition) tuples so iterates through this list
                    for (let item of value) {
                        let word = document.createElement('div')
                        word.textContent = `${item[0]}: ${score} points`
                        word.classList.add('found_word')
                        FOUND_WORDS_LIST.prepend(word)
                        word_count += 1
                        possible_words_dict[item[0]] = item[1]
                    }
                }
                FOUND_WORDS_HEADER.textContent = `${word_count} possible words:`
                if (Object.keys(data).length == 0) {
                    FOUND_WORDS_HEADER.textContent = 'Enter your letters below to see what words you can make.'
                }
            })
        })
        .catch(function(e){
            if(e.name == 'AbortError'){
                console.log('User abored fetch')
            }
            else{
                throw e;
            }
        })
}

// Debouncer for lettersChange - https://davidwalsh.name/javascript-debounce-function
function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		var later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		var callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
	};
};

let debounce_letters_changed = debounce(function(e) {
	lettersChange(e)
}, 500);

// Board typing:
function boardType(e) {
    function board_type_update_end() {
        targetTile.textContent = '.'
        targetTile.classList.remove('selectedSquare')
        targetTile.classList.remove('typed_square')
        targetTile = document.querySelector('#coord-8-8')
        targetTile.classList.add('selectedSquare')
    }
    function board_type_update_mid(new_coord) {
        targetTile.textContent = '.'
        targetTile.classList.remove('selectedSquare')
        targetTile.classList.remove('typed_square')
        targetTile = document.querySelector(new_coord)
        targetTile.classList.add('selectedSquare')
    }
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
                board_type_update_mid(new_coord)
            } if (play_across && id[1] == 1) { // if leftmost square
                board_type_update_end()
            } if (play_down && id[0] > 1) {
                let new_coord = `#coord-${parseInt(id[0]) - 1}-${id[1]}`
                board_type_update_mid(new_coord)
            } if (play_down && id[0] == 1) { // if leftmost square
                board_type_update_end()
            }
        }
    }
}

// Initializations:

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

let targetTile = document.querySelector('#coord-8-8') // Initialize targetTile to centre of board:
targetTile.classList.add('selectedSquare') // and style
let play_across = true
let play_down = false
let possible_words_dict = null
FOUND_WORDS_HEADER.textContent = 'Enter your letters below to see what words you can make.'
let controller = new AbortController() // to abort previous fetch if new one called
ACROSS_BTN.classList.add('clicked')

// Event listners:

document.addEventListener('keyup', (e) => {
    boardType(e);
    debounce_letters_changed(e);
})

USER_LETTERS.addEventListener('keyup', debounce_letters_changed)

FOUND_WORDS_LIST.addEventListener('mouseover', function(e){
    let found_word = e.toElement.textContent.split(':')[0]
    DEFINITION_CONTAINER.textContent = possible_words_dict[found_word]
})

BOARD.addEventListener('click', (e) => {
    //  Add selectedSquare class to clicked tile and remove from old
    if (e.target.id != '') {
        targetTile.classList.remove('selectedSquare') // remove styling from old target
        targetTile = document.querySelector(`#${e.target.id}`)// update target
        targetTile.classList.add('selectedSquare') // add the styling
    }
})

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

