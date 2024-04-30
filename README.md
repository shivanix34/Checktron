<div align="center">
  <h1 style="font-size: 24px; font-weight: bold;">Checktron</h1>
</div><p align="justify">


## Overview

This project focuses on developing a sophisticated AI opponent capable of engaging in 1vs1 battles with human players. Leveraging the Minimax algorithm, tailored to the zero-sum dynamics of draughts, our AI agent strategically evaluates potential moves while anticipating human responses. To enhance efficiency, we integrate α-β pruning techniques, allowing the agent to focus on the most promising paths by eliminating irrelevant branches of the game tree. Moreover, we refine and optimize evaluation functions to provide nuanced assessments of game states, facilitating adaptive gameplay. Through iterative refinement, our project aims to push the boundaries of AI performance in strategic decision-making, showcasing the potential of computational intelligence in mastering complex board games. ”Checktron” contributes to the discourse on AI’s capabilities in adversarial environments, demonstrating its role in strategic gaming and computational intelligence research.

![Screenshot 2024-04-29 042327](https://github.com/shivanix34/Checktron/assets/137218848/935e46ca-8664-4d48-8714-bdf37225e978)
![Screenshot 2024-04-29 042625](https://github.com/shivanix34/Checktron/assets/137218848/da781a68-d556-4f86-b31a-780346006c14)


## Evaluation


The Minimax Algorithm with α-β Pruning:

- The Minimax algorithm is a fundamental technique in game theory for decision-making in adversarial environments. It aims to determine the best move for a player by exploring the game tree to a certain depth.

- The core idea behind Minimax is to maximize the minimum possible outcome for the player, assuming that the opponent plays optimally.

- It works recursively, evaluating all possible moves up to a certain depth and assigning scores to each move based on the expected outcome of the game.

- α-β pruning is an optimization technique that reduces the number of nodes evaluated by the Minimax algorithm by eliminating branches that are guaranteed to be worse than previously examined branches.

- By maintaining two values, α (the minimum score that the maximizing player is assured of) and β (the maximum score that the minimizing player is assured of), α-β pruning can prune branches that fall outside this range.

- The efficiency of α-β pruning lies in its ability to eliminate portions of the game tree that cannot influence the final decision, thus significantly reducing the computational overhead.
</p>
<div style="display: flex; justify-content: center;">
  <img src="https://github.com/shivanix34/Checktron/assets/137218848/33f7f1c5-ce4d-48b8-aa78-6b968cabe8d3" alt="Activity Drawio">
</div>
