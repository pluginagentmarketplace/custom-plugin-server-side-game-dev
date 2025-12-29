# Matchmaking Systems Guide

## ELO Rating System

### Rating Formula
```
New Rating = Old Rating + K * (Actual - Expected)

Where:
  K = Volatility (32 for standard, 16 for established players)
  Actual = 1 (win), 0.5 (draw), 0 (loss)
  Expected = 1 / (1 + 10^((opponent_elo - your_elo) / 400))
```

### Rating Interpretation
```
< 1200:  Beginner
1200-1600:  Intermediate
1600-2000:  Advanced
2000+:  Professional
```

### K-Factor Strategies
```
New Player:       K = 64  (rapid rating change)
Established:      K = 32  (moderate change)
Master:           K = 16  (slow change)

Result: Faster convergence for new players
```

## Skill-Based Matchmaking

### Queue Expansion Bracket Strategy
```
Time in Queue | Skill Window
    5 sec    |  ±50 ELO
   10 sec    |  ±100 ELO
   15 sec    |  ±150 ELO
   20 sec    |  ±200 ELO
   30 sec    |  Unlimited

Result: Find match within 30 sec, maintaining fairness
```

### Implementation Algorithm
```python
def find_match(player, wait_time):
    if wait_time < 5:
        skill_window = 50
    elif wait_time < 10:
        skill_window = 100
    elif wait_time < 15:
        skill_window = 150
    else:
        skill_window = 200

    candidates = queue.filter(
        abs(candidate.elo - player.elo) <= skill_window
    )
    return random.choice(candidates)
```

## Match Balance Metrics

### Balance Calculation
```
Balance = 1 / (1 + abs(elo_diff) / 400)

ELO Diff | Balance | Win Probability
    0   |  1.00   |  50-50
  100   |  0.80   |  64-36
  200   |  0.62   |  76-24
  400   |  0.27   |  91-9 (very unbalanced)
```

### Quality Score
```
Perfect Match:      Balance >= 0.95
Good Match:         Balance >= 0.85
Acceptable:         Balance >= 0.70
Poor Match:         Balance < 0.70
```

## Glicko-2 System (Advanced)

### Advantages over ELO
```
✅ Accounts for rating deviation (uncertainty)
✅ Accounts for volatility
✅ Better for inactive players
✅ Faster convergence
```

### Components
```
μ (mu):             Rating value
φ (phi):            Rating deviation (uncertainty)
σ (sigma):          Volatility (consistency)

Higher uncertainty → Larger rating swings
```

## Trueskill System (Microsoft)

### Advantages
```
✅ Designed for team games
✅ Factors in team synergy
✅ Bayesian approach (probabilistic)
✅ Handles draws/upsets well
```

### Rating Components
```
Skill (μ):          Player skill
Uncertainty (σ):    Confidence in rating
Better for:         Competitive ranked systems
```

## Queue Management

### Queue Types
```
Quick Play:    Any skill, instant match
Ranked:        Matched by rating
Casual:        No rating impact
Placement:     Determine initial rating
```

### Queue Health Metrics
```
Wait Time P95:      < 30 seconds
Match Balance:      > 85%
Queue Depth:        10+ players
Dodge Rate:         < 5%
```

## Anti-Gaming Measures

### Prevent Smurfing
```
New accounts:       Placement matches (10 games)
Rapid rating climb: Increase K-factor monitor
Account analysis:   Detect unusual patterns

Detection signals:
  - New account winning 90%+
  - Skill gap too large from previous
  - Hardware/region changes
```

### Prevent Boosting
```
Account sharing:    IP/device fingerprint
Win trading:        Detect coordinated wins
Account sales:      Detect rating drops

Penalties:
  - Rating reset
  - Account suspension
  - Ban (severe cases)
```

## Role-Based Matchmaking

### Example: 5v5 Team Game
```
Role Distribution:
  Tank:       1 per team (lowest avg elo)
  Damage:     2 per team
  Support:    1 per team
  Flex:       1 per team

Result: Balanced teams, all roles played
```

### Soft Constraints
```
Minimize team ELO difference
Minimize skill variance (all similar OR all different)
Maximize role fill satisfaction
Avoid toxic player groupings (if tracked)
```

## Matchmaking Algorithms

### Brute Force (for small queues)
```
O(n²) complexity - Try all pairs
Acceptable for < 100 players
```

### Hungarian Algorithm (for balanced teams)
```
O(n³) complexity - Optimal assignment
Best for: Tournament, lobby, small queues
```

### Greedy Selection
```
O(n log n) complexity - Fast
Select best available match
Good for: Large queues, real-time
```

### Machine Learning
```
Train on historical match data
Predict match quality
Minimize queue time + balance trade-off
```

## Seasonal Ranking

### Seasonal Reset Pattern
```
Season 1:     All players start at 1600
Season 2:     Reset to 1500 + 75% of (rating - 1500)
Effect:       Strong players still rated high
              Weak players get fresh start
```

### Placement Matches
```
10 placement matches to seed initial rating
Based on previous season (if exists)
Faster convergence in new season
```

## Incentive Structures

### Ranking Rewards
```
Bronze:       0-1000 ELO (cosmetics)
Silver:       1000-1500 ELO (cosmetics)
Gold:         1500-1800 ELO (cosmetics)
Platinum:     1800-2000 ELO (exclusive skins)
Diamond:      2000+ ELO (exclusive cosmetics)

Effect: Motivation to climb ranks
```

### Win Streaks
```
Win streak bonus:    +5 ELO per consecutive win
Loss streak penalty: -2 ELO per consecutive loss

Effect: Rewards momentum, punishes consistency
```

## Monitoring & Adjustments

### Quality Metrics Dashboard
```
Match Fairness:     Average balance score
Wait Times:         P50, P95, P99
Queue Health:       Active players by skill
Popular Roles:      What's being filled
Dodge/Leave Rate:   Player satisfaction
```

### Dynamic Adjustment
```
If average wait time > 45 sec:
  → Expand skill windows 20%

If match balance < 70%:
  → Restrict skill windows 10%

If dodge rate > 10%:
  → Queue penalties (cooldown)

If tank queue > 2x dps queue:
  → Tank queue bonus rewards
```

## Anti-patterns

❌ **Pure ELO, no skill window**: Unfair for new players
✅ **Do**: Expand bracket over time

❌ **Fixed queue time**: Some players wait 30s, some 5m
✅ **Do**: Expand bracket dynamically

❌ **Ignore region/latency**: High ping is unfair
✅ **Do**: Prefer regional matches

❌ **No placement system**: Wild rating swings
✅ **Do**: Placement matches for new accounts
