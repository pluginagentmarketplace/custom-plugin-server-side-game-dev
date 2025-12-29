#!/usr/bin/env python3
"""
ELO and Skill-Based Matchmaking Simulator
Demonstrates ranking systems and queue matching algorithms
"""

import random
import math
from typing import List, Tuple

class Player:
    """Player with ELO rating"""
    def __init__(self, player_id: int, elo: int = 1600):
        self.player_id = player_id
        self.elo = elo
        self.matches_played = 0
        self.wins = 0
        self.losses = 0

    def win_rate(self) -> float:
        """Calculate win rate"""
        if self.matches_played == 0:
            return 0.0
        return self.wins / self.matches_played

    def __repr__(self):
        return f"Player#{self.player_id} (ELO: {self.elo}, WR: {self.win_rate():.1%})"

class ELOSystem:
    """Standard ELO rating system"""

    K_FACTOR = 32  # ELO volatility (higher = faster rating change)

    @staticmethod
    def expected_score(rating1: int, rating2: int) -> float:
        """Calculate expected score (probability of winning)"""
        return 1 / (1 + 10 ** ((rating2 - rating1) / 400))

    def update_rating(self, player: Player, opponent: Player, result: float) -> int:
        """
        Update player rating after match
        result: 1.0 = win, 0.5 = draw, 0.0 = loss
        """
        expected = self.expected_score(player.elo, opponent.elo)
        delta = self.K_FACTOR * (result - expected)
        new_elo = int(player.elo + delta)
        return new_elo

class MatchmakingQueue:
    """Skill-based matchmaking queue"""

    def __init__(self, max_queue_time: float = 30.0):
        self.queue: List[Player] = []
        self.max_queue_time = max_queue_time

    def add_player(self, player: Player):
        """Add player to queue"""
        self.queue.append(player)

    def find_match(self, player: Player, skill_window: int = 100) -> Player:
        """Find opponent within skill window"""
        candidates = [
            p for p in self.queue
            if abs(p.elo - player.elo) <= skill_window and p.player_id != player.player_id
        ]

        if candidates:
            return random.choice(candidates)
        return None

    def create_matches(self, skill_window: int = 100) -> List[Tuple[Player, Player]]:
        """Create matches from current queue"""
        matches = []
        matched_ids = set()

        # Sort by ELO
        sorted_queue = sorted(self.queue, key=lambda p: p.elo)

        for player in sorted_queue:
            if player.player_id in matched_ids:
                continue

            opponent = self.find_match(player, skill_window)
            if opponent and opponent.player_id not in matched_ids:
                matches.append((player, opponent))
                matched_ids.add(player.player_id)
                matched_ids.add(opponent.player_id)

        # Remove matched players
        self.queue = [p for p in self.queue if p.player_id not in matched_ids]

        return matches

class TournamentSimulator:
    """Simulate tournament matches"""

    def __init__(self):
        self.elo_system = ELOSystem()

    def simulate_match(self, player1: Player, player2: Player) -> Tuple[Player, Player]:
        """Simulate a match outcome"""
        expected_p1 = self.elo_system.expected_score(player1.elo, player2.elo)

        # Random match outcome weighted by ELO difference
        if random.random() < expected_p1:
            winner, loser = player1, player2
            p1_result, p2_result = 1.0, 0.0
        else:
            winner, loser = player2, player1
            p1_result, p2_result = 0.0, 1.0

        # Update ratings
        delta1 = self.elo_system.update_rating(player1, player2, p1_result)
        delta2 = self.elo_system.update_rating(player2, player1, p2_result)

        player1.elo = delta1
        player2.elo = delta2
        player1.matches_played += 1
        player2.matches_played += 1

        if p1_result == 1.0:
            player1.wins += 1
            player2.losses += 1
        else:
            player1.losses += 1
            player2.wins += 1

        return winner, loser

    def run_tournament(self, num_players: int = 100, num_rounds: int = 10):
        """Run complete tournament"""
        # Create players
        players = [Player(i, random.randint(1200, 2000)) for i in range(num_players)]

        print("=" * 70)
        print("MATCHMAKING TOURNAMENT SIMULATION")
        print("=" * 70)
        print(f"Players: {num_players}, Rounds: {num_rounds}")
        print()

        # Run rounds
        for round_num in range(num_rounds):
            print(f"Round {round_num + 1}:")

            # Shuffle for matches
            random.shuffle(players)

            # Create matches
            matches_created = 0
            for i in range(0, len(players) - 1, 2):
                winner, loser = self.simulate_match(players[i], players[i + 1])
                matches_created += 1

            print(f"  Matches: {matches_created}")
            print()

        # Final statistics
        print("=" * 70)
        print("FINAL STANDINGS (Top 10)")
        print("=" * 70)

        # Sort by ELO
        players.sort(key=lambda p: p.elo, reverse=True)

        for rank, player in enumerate(players[:10], 1):
            print(f"{rank:2}. {player} | W/L: {player.wins}/{player.losses}")

        print()
        print(f"Average ELO: {sum(p.elo for p in players) / len(players):.0f}")
        print(f"ELO Range: {min(p.elo for p in players)} - {max(p.elo for p in players)}")

class MatchmakingMetrics:
    """Analyze matchmaking quality"""

    @staticmethod
    def skill_balance(player1: Player, player2: Player) -> float:
        """Calculate match balance (0 = perfect, 1 = completely unbalanced)"""
        elo_diff = abs(player1.elo - player2.elo)
        # Normalize to 0-1 range (0 diff = 0 unbalance, 400 diff = 1 unbalance)
        return min(elo_diff / 400, 1.0)

    @staticmethod
    def calculate_quality_score(matches: List[Tuple[Player, Player]]) -> float:
        """Calculate overall matchmaking quality"""
        if not matches:
            return 0.0

        balances = [
            MatchmakingMetrics.skill_balance(p1, p2)
            for p1, p2 in matches
        ]

        # Lower is better (0 = perfect)
        average_unbalance = sum(balances) / len(balances)
        quality_score = 1.0 - average_unbalance  # Invert to 0-1 quality

        return quality_score

if __name__ == "__main__":
    # Run tournament
    simulator = TournamentSimulator()
    simulator.run_tournament(num_players=100, num_rounds=20)
