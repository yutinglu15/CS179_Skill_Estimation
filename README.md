# CS179_Skill_Estimation

This is an in-class project from cs 179.

This is a skill estimation from starcraft data. 


## Potential Ideas 

1. Compare the ability of your model to predict the winner of new (unseen) games to simple approaches, such as fraction of games won, number of games played, etc.
    - figure out ways to evaluate model performance: 
        (a) predict the winner of games in validation
        (b) predict the fraction of games won
        (c) predict game result: [? - ?]
    
2. Try evaluating how many games are required to accurately predict the players' skill levels / win probability by decreasing the amount of training data available and observing the performance. 
    - when processing data...may do pruning
        (a) vary # most recent games for each player --> look at distribution of date in train and valid first
        (b) vary max # opponents for each player to count
        (c) vary max # games with each oppo for each player to count 
    
3. Try evaluating how quickly you can determine a new players' skill by either random game choices or carefully chosen games (matched based on estimated skill level).  You can leave a player out of the inference process entirely, then slowly add their games in and see how quickly you are able to learn their relative position.
    - may need to build a new model: 
        * input with skill levels for old players, games that new player(s) involved.
        * output the estimated skill level for new player(s). 
    
4. Experiment with learning a more complex model, for example taking into account game features (player's selected character) or additional latent scores (such as offensive and defensive skill) along with a correspondingly more elaborate probability of win function.
        - Add weights for match date (the more recent one the more importance) -> related to Idea 2. 
        - # plays
        - race
        - addon
        - tournament-type
        * For those new features, may need to do hypothesis test later to verify their significance to the results.  
