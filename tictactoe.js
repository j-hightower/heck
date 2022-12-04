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
  constructor(grid /* this will be an array containg nine possible values nested into 3 arrays each containg 3 values. */) {
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
    const tic_tac_toe_board = document.createElement('div')
    const container = document.getElementById('testarea')
    tic_tac_toe_board.setAttribute('id', 'tictactoeboard')
    container.appendChild(tic_tac_toe_board)

    for (let row of this.grid) {
      const tic_tac_toe_row = document.createElement('div')
      tic_tac_toe_row.setAttribute('id', 'tictactoerow')
      tic_tac_toe_board.appendChild(tic_tac_toe_row)

      for (let column of row) {
        const tic_tac_toe_column = document.createElement('div')
        tic_tac_toe_column.setAttribute('id', 'tictactoecell')
        tic_tac_toe_row.appendChild(tic_tac_toe_cell)
      }
    }
  }
  /* defines a method for changing the state of a specific cell in our tic tac toe game.*/
  changestate(playtype, row, cell) {
  /* Defines the X state*/
    if (playtype === "x") {
      let state = 1
      this.grid[row][cell] = state
    }
  /* Defines the circle state*/
    else if (playtype === "o") {
      state = 2
      this.grid[row][cell] = state
  }
  /* Defines the blank state*/
    else {
      let state = 0
      this.grid[row][cell] = state
    }
  }
}

/* The gameplay function should handle reacting to when a user clicks somewhere on the grid, changing the value of the grid array to correspond to an 'x' or an 'o', and call the layout function to update the grid on the screen.*/
Gameplay = function() {
  return
}

Layout = function() {
  return
}

Test = function() {
  const game = new TicTacToeGame(0)
  const button = document.getElementById('testbutton').
  // game.changestate("o", 1, 1)
  // button.setAttribute('disabled')
  console.log(game)
  console.log(button)
}
