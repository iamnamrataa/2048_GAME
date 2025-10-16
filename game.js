class Game2048 {
    constructor() {
        this.size = 4;
        this.grid = [];
        this.score = 0;
        this.bestScore = localStorage.getItem('bestScore') || 0;
        this.gameOver = false;
        this.won = false;
        this.keepPlaying = false;
        
        this.init();
        this.setupEventListeners();
    }

    init() {
        this.createGrid();
        this.updateDisplay();
        this.addRandomTile();
        this.addRandomTile();
    }

    createGrid() {
        this.grid = Array(this.size).fill().map(() => Array(this.size).fill(0));
    }

    addRandomTile() {
        const emptyCells = [];
        
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                if (this.grid[i][j] === 0) {
                    emptyCells.push({i, j});
                }
            }
        }

        if (emptyCells.length > 0) {
            const {i, j} = emptyCells[Math.floor(Math.random() * emptyCells.length)];
            this.grid[i][j] = Math.random() < 0.9 ? 2 : 4;
        }
    }

    move(direction) {
        if (this.gameOver) return false;

        const oldGrid = this.grid.map(row => [...row]);
        let moved = false;

        switch (direction) {
            case 'left':
                moved = this.moveLeft();
                break;
            case 'right':
                moved = this.moveRight();
                break;
            case 'up':
                moved = this.moveUp();
                break;
            case 'down':
                moved = this.moveDown();
                break;
        }

        if (moved) {
            this.addRandomTile();
            this.updateDisplay();
            this.checkGameState();
            return true;
        }
        return false;
    }

    moveLeft() {
        let moved = false;
        
        for (let i = 0; i < this.size; i++) {
            const row = this.grid[i].filter(cell => cell !== 0);
            const newRow = [];
            let j = 0;

            while (j < row.length) {
                if (j + 1 < row.length && row[j] === row[j + 1]) {
                    const mergedValue = row[j] * 2;
                    newRow.push(mergedValue);
                    this.score += mergedValue;
                    j += 2;
                    moved = true;
                } else {
                    newRow.push(row[j]);
                    j += 1;
                }
            }

            while (newRow.length < this.size) {
                newRow.push(0);
            }

            if (JSON.stringify(this.grid[i]) !== JSON.stringify(newRow)) {
                moved = true;
            }
            
            this.grid[i] = newRow;
        }
        
        return moved;
    }

    moveRight() {
        this.reverseRows();
        const moved = this.moveLeft();
        this.reverseRows();
        return moved;
    }

    moveUp() {
        this.transpose();
        const moved = this.moveLeft();
        this.transpose();
        return moved;
    }

    moveDown() {
        this.transpose();
        const moved = this.moveRight();
        this.transpose();
        return moved;
    }

    reverseRows() {
        this.grid = this.grid.map(row => row.reverse());
    }

    transpose() {
        this.grid = this.grid[0].map((_, i) => this.grid.map(row => row[i]));
    }

    canMove() {
        // Check for empty cells
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                if (this.grid[i][j] === 0) return true;
            }
        }

        // Check for possible merges
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                const current = this.grid[i][j];
                
                // Check right neighbor
                if (j < this.size - 1 && this.grid[i][j + 1] === current) return true;
                // Check bottom neighbor
                if (i < this.size - 1 && this.grid[i + 1][j] === current) return true;
            }
        }

        return false;
    }

    checkGameState() {
        // Check for win
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                if (this.grid[i][j] === 2048 && !this.keepPlaying) {
                    this.won = true;
                    this.showMessage('You Win!', true);
                }
            }
        }

        // Update best score
        if (this.score > this.bestScore) {
            this.bestScore = this.score;
            localStorage.setItem('bestScore', this.bestScore);
        }

        // Check for game over
        if (!this.canMove()) {
            this.gameOver = true;
            this.showMessage('Game Over!', false);
        }
    }

    showMessage(message, isWin) {
        const messageEl = document.getElementById('message');
        const messageContainer = document.querySelector('.game-message');
        
        messageEl.textContent = message;
        messageContainer.classList.add(isWin ? 'game-won' : 'game-over');
    }

    hideMessage() {
        const messageContainer = document.querySelector('.game-message');
        messageContainer.classList.remove('game-won', 'game-over');
    }

    updateDisplay() {
        this.updateGrid();
        this.updateScores();
    }

    updateGrid() {
        const gridEl = document.querySelector('.grid');
        gridEl.innerHTML = '';

        // Create empty cells
        for (let i = 0; i < this.size * this.size; i++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            gridEl.appendChild(cell);
        }

        // Create tiles
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                const value = this.grid[i][j];
                if (value !== 0) {
                    const tile = document.createElement('div');
                    tile.className = `tile tile-${value}`;
                    tile.textContent = value;
                    tile.style.width = `calc(25% - 10px)`;
                    tile.style.height = `calc(25% - 10px)`;
                    tile.style.transform = `translate(${j * 100}%, ${i * 100}%)`;
                    gridEl.appendChild(tile);
                }
            }
        }
    }

    updateScores() {
        document.getElementById('score').textContent = this.score;
        document.getElementById('best-score').textContent = this.bestScore;
    }

    restart() {
        this.grid = Array(this.size).fill().map(() => Array(this.size).fill(0));
        this.score = 0;
        this.gameOver = false;
        this.won = false;
        this.keepPlaying = false;
        this.hideMessage();
        this.addRandomTile();
        this.addRandomTile();
        this.updateDisplay();
    }

    setupEventListeners() {
        // Keyboard controls
        document.addEventListener('keydown', (e) => {
            if (this.gameOver && !this.won) return;

            switch(e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    this.move('left');
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    this.move('right');
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    this.move('up');
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    this.move('down');
                    break;
            }
        });

        // Restart button
        document.getElementById('restart-btn').addEventListener('click', () => {
            this.restart();
        });

        // Message buttons
        document.getElementById('keep-playing').addEventListener('click', () => {
            this.keepPlaying = true;
            this.hideMessage();
        });

        document.getElementById('try-again').addEventListener('click', () => {
            this.restart();
        });
    }
}

// Initialize the game when page loads
document.addEventListener('DOMContentLoaded', () => {
    new Game2048();
});