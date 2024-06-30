const canvas = document.getElementById("pong");
const context = canvas.getContext("2d");

// Create the paddle
const paddleWidth = 10, paddleHeight = 100, paddleMargin = 10;
const player = {
    x: paddleMargin,
    y: (canvas.height - paddleHeight) / 2,
    width: paddleWidth,
    height: paddleHeight,
    color: "WHITE",
    score: 0
};

const ai = {
    x: canvas.width - paddleWidth - paddleMargin,
    y: (canvas.height - paddleHeight) / 2,
    width: paddleWidth,
    height: paddleHeight,
    color: "WHITE",
    score: 0
};

// Create the ball
const ball = {
    x: canvas.width / 2,
    y: canvas.height / 2,
    radius: 10,
    speed: 5,
    velocityX: 5,
    velocityY: 5,
    color: "WHITE"
};

// Draw the net
function drawNet() {
    for (let i = 0; i <= canvas.height; i += 15) {
        drawRect(canvas.width / 2 - 1, i, 2, 10, "WHITE");
    }
}

// Draw a rectangle (paddle, net, etc.)
function drawRect(x, y, w, h, color) {
    context.fillStyle = color;
    context.fillRect(x, y, w, h);
}

// Draw a circle (ball)
function drawCircle(x, y, r, color) {
    context.fillStyle = color;
    context.beginPath();
    context.arc(x, y, r, 0, Math.PI * 2, false);
    context.closePath();
    context.fill();
}

// Draw text (score)
function drawText(text, x, y, color) {
    context.fillStyle = color;
    context.font = "45px Arial";
    context.fillText(text, x, y);
}

// Reset the ball after scoring
function resetBall() {
    ball.x = canvas.width / 2;
    ball.y = canvas.height / 2;
    ball.speed = 5;
    ball.velocityX = -ball.velocityX;
    ball.velocityY = 5 * (Math.random() * 2 - 1);
}

// Update the paddle positions and ball position
function update() {
    // Move the ball
    ball.x += ball.velocityX;
    ball.y += ball.velocityY;

    // AI paddle movement
    let targetY = ball.y - (ai.height / 2);
    ai.y += (targetY - ai.y) * 0.1;

    // Ball collision with top and bottom walls
    if (ball.y + ball.radius > canvas.height || ball.y - ball.radius < 0) {
        ball.velocityY = -ball.velocityY;
    }

    // Check for collision with paddles
    let playerPaddle = (ball.x < canvas.width / 2) ? player : ai;
    if (ball.x + ball.radius > playerPaddle.x && ball.x - ball.radius < playerPaddle.x + playerPaddle.width &&
        ball.y + ball.radius > playerPaddle.y && ball.y - ball.radius < playerPaddle.y + playerPaddle.height) {
        ball.velocityX = -ball.velocityX;
        ball.speed += 0.5;
    }

    // Check for scoring
    if (ball.x + ball.radius > canvas.width) {
        player.score++;
        resetBall();
    } else if (ball.x - ball.radius < 0) {
        ai.score++;
        resetBall();
    }
}

// Render the game
function render() {
    // Clear the canvas
    drawRect(0, 0, canvas.width, canvas.height, "#000");

    // Draw the net
    drawNet();

    // Draw the paddles and ball
    drawRect(player.x, player.y, player.width, player.height, player.color);
    drawRect(ai.x, ai.y, ai.width, ai.height, ai.color);
    drawCircle(ball.x, ball.y, ball.radius, ball.color);

    // Draw the scores
    drawText(player.score, canvas.width / 4, canvas.height / 5, "WHITE");
    drawText(ai.score, 3 * canvas.width / 4, canvas.height / 5, "WHITE");
}

// Game loop
function gameLoop() {
    update();
    render();
}

setInterval(gameLoop, 1000 / 60);

// Player paddle movement
canvas.addEventListener("mousemove", evt => {
    let rect = canvas.getBoundingClientRect();
    player.y = evt.clientY - rect.top - player.height / 2;
});
