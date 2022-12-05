/*
  Design a program that allows a user to play tic tac toe.

  Beginner level: The user is both X(O) and O(X), respectively.

  Intermediate Level: The user plays against something else.

  Expert Level: The user plays against an AI.

*/

/* We'll define a class that handles all changes to our grid. I think this is going to grow as we move along, but the bare minimum should define methods that save states to cells, and
define properties for each row. defining a class defines ways we can easily create new objects. We'll want one object to contain the grid. the grid will be an array containing the
states of each cell. we'll need a method for changing the state of the cell.... that's all I can think about for now. Lets make sure we think about arguments that will need to be passed
into the methods!*/
class TicTacToeGame {
  constructor() {
    /* We'll arbitrarily set our grid as an array. each 'line' in our array is a row, and each value in the set is a cell. We'll say that when the value is 0 it's blank, if the value is 1
    it's an 'x', and if the value is 2 it's an 'o'. */
    this.grid = [
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0]
    ]
  }
  /* Defines the method for populating the grid.*/
  placegrid() {
    /* creates the container for the tic tac toe board. It's just a flex container. */
    const tic_tac_toe_board = document.createElement('div')
    const container = document.getElementById('testarea')
    let row_number = 0
    let column = 0
    tic_tac_toe_board.setAttribute('id', 'tictactoeboard')
    container.appendChild(tic_tac_toe_board)
    /* Loops through the rows of the grid of the tic tac toe board and creates a div for each of them. */
    for (let row of this.grid) {
      row_number ++
      const tic_tac_toe_row = document.createElement('div')
      tic_tac_toe_row.setAttribute('id', 'tictactoerow')
      tic_tac_toe_board.appendChild(tic_tac_toe_row)
      /* Loops through each column in each row and creates a button */
      for (let cell of row) {
        column ++
        if (column === 4) {
          column = 0
          column ++
        }
        const tic_tac_toe_column = document.createElement('button')
        tic_tac_toe_column.setAttribute('class', 'tictactoecell')
        tic_tac_toe_column.setAttribute('id', 'row' + (row_number - 1) + 'column' + (column - 1))
        tic_tac_toe_column.setAttribute('onClick', 'Test2(' + (row_number - 1) + ', ' + (column - 1) + ')')
        tic_tac_toe_row.appendChild(tic_tac_toe_column)
      }
    }
    const reset_button = document.createElement('button')
    reset_button.setAttribute('id', 'tictactoereset')
    reset_button.setAttribute('onClick', 'Test3()')
    reset_button.innerHTML = 'reset'
    tic_tac_toe_board.appendChild(reset_button)
  }
  /* defines a method for changing the state of a specific cell in our tic tac toe game.*/
  changestate(player, row, column) {
    /* Defines the X state*/
    if (player === "x") {
      let state = 1
      this.grid[row][column] = state
    }
    /* Defines the circle state*/
    else if (player === "o") {
      let state = 2
      this.grid[row][column] = state
  }
    /* Defines the blank state*/
    else {
      let state = 0
      this.grid[row][column] = state
    }
  }
  /* displays the normal gameplay for tic-tac-toe by adding a div inside of each button, containing text corresponding to 'x' or 'o'.*/
  play(row, column) {
    let container = document.getElementById('row' + row + 'column' + column)
    container.removeAttribute('onClick')
    let play_display = document.createElement('div')
    if (this.grid[row][column] === 1) {
      play_display.setAttribute('class', 'tictactoeplayed')
      play_display.setAttribute('style', 'color:#0080ff')
      play_display.innerText = 'X'
      container.appendChild(play_display)
    }
    else if (this.grid[row][column] === 2) {
      play_display.setAttribute('class', 'tictactoeplayed')
      play_display.setAttribute('style', 'color:#ff3300')
      play_display.innerText = 'O'
      container.appendChild(play_display)
    }
  }

  reset() {
    const played_game = document.getElementById('tictactoeboard')
    played_game.remove()
    player = 0
    game = new TicTacToeGame
    game.placegrid()
  }

  check() {
    /* Check horizontally. */
    for (let array of game.grid) {
      if (WonGameHorizontally(array)) {
        game.won()
      }
    }
    /* won vertically block. We want to check if the same number is present in the same column of all rows. How would we do this? */
    if (WonGameVertically(game.grid)) {
      game.won()
    }
    if (WonGameDiagonally(game.grid)) {
      game.won()
    }
  }

  won() {
    let played_game = document.getElementsByClassName('tictactoecell')
    for (let element of played_game) {
      element.removeAttribute('onClick')
    }
    console.log('You won!')
  }
}

/* The gameplay function should handle reacting to when a user clicks somewhere on the grid, changing the value of the grid array to correspond to an 'x' or an 'o', and call the layout function to update the grid on the screen.*/
let game = 0
let player = 0

WonGameHorizontally = function(array) {
  return (array[0] == 1 & array[1] == 1 & array[2] == 1) | (array[0] == 2 & array[1] == 2 & array[2] == 2)
}

WonGameVertically = function(grid) {
  return (
    (grid[0][0] == 1 & grid[1][0] == 1 & grid[2][0] == 1) |
    (grid[0][1] == 1 & grid[1][1] == 1 & grid[2][1] == 1) |
    (grid[0][2] == 1 & grid[1][2] == 1 & grid[2][2] == 1) |
    (grid[0][0] == 2 & grid[1][0] == 2 & grid[2][0] == 2) |
    (grid[0][1] == 2 & grid[1][1] == 2 & grid[2][1] == 2) |
    (grid[0][2] == 2 & grid[1][2] == 2 & grid[2][2] == 2)
  )
}

WonGameDiagonally = function(grid) {
  return (
    (grid[0][0] == 1 & grid[1][1] == 1 & grid[2][2] == 1) |
    (grid[0][2] == 1 & grid[1][1] == 1 & grid[2][0] == 1) |
    (grid[0][0] == 2 & grid[1][1] == 2 & grid[2][2] == 2) |
    (grid[0][2] == 2 & grid[1][1] == 2 & grid[2][0] == 2)
  )
}

Layout = function() {
  return
}

Test = function() {
  game = new TicTacToeGame()
  const button = document.getElementById('testbutton')
  game.placegrid()
  button.removeAttribute('onClick')
}

Test2 = function(row, column) {
  if (player % 2) {
    let playtype = "o"
    game.changestate(playtype, row, column)
  }
  else {
    let playtype = "x"
    game.changestate(playtype, row, column)
  }
  player ++
  game.play(row, column)
  game.check()
}

Test3 = function() {
  game.reset(game.grid)
}
