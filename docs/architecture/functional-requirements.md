# Requirments JSTB

## Overview
JSTB is a trading system that analysez patterns in historic data using Machine Learning and translates these patterns into logic (rules) for trading bots.    

## Technical requirements
- Runs in the cloud
- Simple as possible technology
- Historic stock data is stored in a database
- Keep cost in mind
- Version control
- DevOps pipelines

## Platform use cases
- Ingest market data
- Describe and test high level ideas (with AI)
- Specify ideas that may give an edge into a strategy
- Backtest stategy
- Develop trading algo for sucesfully backtested startegies
- Implement and run startegies in trading bot
- Evaluate and improve or discontinue strategies
 


## Functional requirements
- Build up history and then update daily 
- Think of specific financial instruments, timeframe minute, dating back to 2000 (if possible) 
- Examples: Nasdaq, S&P 500, Gold, BTC, Tesla, VIX, DIXY - Add instruments over time, begin with a single instrument 
- Define high level ideas - Examples: "find the probability of an index closing higher on a Monday after a Friday with a big loss" or "the probability of an index going down after going up for 10 straight days " 
- So it is not so much about classic candle sticks, moving averages etc., but more about finding niche patterns in the data 
- An LLM should translate the high level idea in an ML model 
- The ideas should be very high level, the LLM should try different variations and variables 
- Then if found a pattern must be translated in a trading pattern 
- The pattern including risk management is then implemented in a trading bot that interacts with the trading platform

## Links
[Markdown guide](https://www.markdownguide.org/cheat-sheet/)
[Azure DevOps] (https://aex.dev.azure.com/)
[Azure Portal] (https://portal.azure.com/)