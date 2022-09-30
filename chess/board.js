var game = new Chess()

function onDragStart (source, piece, position, orientation)
{
  // do not pick up pieces if the game is over
  if (game.game_over()) return false

  // only pick up pieces for the side to move
  if ((board.orientation() === "white" && piece.search(/^b/) !== -1) ||
      (board.orientation() === "black" && piece.search(/^w/) !== -1))
  {
    return false
  }
}

function makeRandomMove () {
  var possibleMoves = game.moves()

  // game over
  if (possibleMoves.length === 0) return

  var randomIdx = Math.floor(Math.random() * possibleMoves.length)
  game.move(possibleMoves[randomIdx])
  board.position(game.fen())
}

function onDrop (source, target)
{
  // see if the move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' // NOTE: always promote to a queen for example simplicity
  })

  // illegal move
  if (move === null) return 'snapback'

  window.setTimeout(makeRandomMove, 100)
}

// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd ()
{
  board.position(game.fen())
}

var config = {
  draggable: true,
  position: 'start',
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd
}

var board = Chessboard('myBoard', config)

function reset()
{
  game.reset()
  board.start()
}

function reverseBoard()
{
  game.reset()
  board.start(false)
  board.flip()
  if (board.orientation() === "black")
  {
    window.setTimeout(makeRandomMove, 100)
  }
}

$('#reset').on('click', reset)
$('#reverse_board').on('click', reverseBoard)