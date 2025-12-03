import streamlit as st
from collections import defaultdict
import random
import pandas as pd
# falta optimizar fixture para omitir en lo posible single matches y descansos consecutivos
class AmericanoPadelTournament:
    """Mixed Americano Tournament - Men & Women pairs with helper logic"""
    def __init__(self, male_players, female_players, num_fields, points_per_match):
        if len(male_players) != len(female_players):
            raise ValueError(f"Must have equal numbers of men and women. Got {len(male_players)} men and {len(female_players)} women.")
        
        if len(male_players) < 2:
            raise ValueError("Need at least 2 players of each gender (4 total)")
        
        self.male_players = male_players
        self.female_players = female_players
        self.num_players = len(male_players)
        self.total_players = len(male_players) + len(female_players)
        self.num_fields = num_fields
        self.points_per_match = points_per_match
        
        self.player_stats = defaultdict(lambda: {
            'matches': 0,
            'partners': defaultdict(int),
            'opponents': defaultdict(int),
            'points_for': 0,
            'points_against': 0
        })
        
        self.rounds = []
        self.all_matches_played = set()
        
        # NEW: Track minimum matches (target for valid games)
        self.min_matches_reached = 0
    
    def get_match_signature(self, team1, team2):
        """Create unique signature for a match"""
        all_players = sorted([team1[0], team1[1], team2[0], team2[1]])
        return tuple(all_players)
    
    def calculate_match_score(self, team1, team2, current_round):
        """Calculate desirability score for a match (LOWER is better)"""
        players = [team1[0], team1[1], team2[0], team2[1]]
        
        # PRIORITY 1: Strongly favor players who are resting or rested recently
        rest_bonus = 0
        for p in players:
            rounds_since_last = current_round - self.player_stats[p].get('last_round_played', -1)
            if rounds_since_last > 1:
                # Player has been resting - HEAVILY favor them
                rest_bonus -= rounds_since_last * 5000
            elif rounds_since_last == 1:
                # Player just played - slight penalty to avoid consecutive play
                rest_bonus += 1000
        
        match_count_score = sum(self.player_stats[p]['matches'] for p in players)
        
        partnership_penalty = 0
        partnership_penalty += self.player_stats[team1[0]]['partners'][team1[1]] * 1000
        partnership_penalty += self.player_stats[team2[0]]['partners'][team2[1]] * 1000
        
        opponent_penalty = 0
        for p1 in [team1[0], team1[1]]:
            for p2 in [team2[0], team2[1]]:
                opponent_penalty += self.player_stats[p1]['opponents'][p2] * 100
        
        total_score = rest_bonus + match_count_score + partnership_penalty + opponent_penalty
        total_score += random.random() * 0.01
        
        return total_score
    
    def get_players_needing_matches(self):
        """Get players who haven't reached the minimum matches yet"""
        all_players = self.male_players + self.female_players
        if not all_players:
            return []
        
        min_matches = min(self.player_stats[p]['matches'] for p in all_players)
        return [p for p in all_players if self.player_stats[p]['matches'] == min_matches]
    
    def find_best_matches_for_round(self, num_matches_needed, current_round):
        """Find the best set of matches for a round"""
        selected_matches = []
        used_players = set()
        
        # Get players who need matches
        players_needing_matches = set(self.get_players_needing_matches())
        
        # PRIORITIZE players who have been resting
        resting_males = sorted(
            [m for m in self.male_players],
            key=lambda p: (
                -(current_round - self.player_stats[p].get('last_round_played', -1)),  # Longer rest = higher priority
                self.player_stats[p]['matches']  # Fewer matches = higher priority
            )
        )
        resting_females = sorted(
            [f for f in self.female_players],
            key=lambda f: (
                -(current_round - self.player_stats[f].get('last_round_played', -1)),
                self.player_stats[f]['matches']
            )
        )
        
        while len(selected_matches) < num_matches_needed:
            available_males = [m for m in resting_males if m not in used_players]
            available_females = [f for f in resting_females if f not in used_players]
            
            if len(available_males) < 2 or len(available_females) < 2:
                break
            
            # Check if we have at least ONE player who needs matches
            available_males_needing = [m for m in available_males if m in players_needing_matches]
            available_females_needing = [f for f in available_females if f in players_needing_matches]
            
            # STOP creating matches if no one available needs matches
            if not available_males_needing and not available_females_needing:
                break
            
            best_match = None
            best_score = float('inf')
            
            # Focus on players with longest rest first (already sorted)
            search_males = available_males[:min(8, len(available_males))]
            search_females = available_females[:min(8, len(available_females))]
            
            for i in range(len(search_males)):
                for j in range(i + 1, len(search_males)):
                    m1, m2 = search_males[i], search_males[j]
                    
                    for k in range(len(search_females)):
                        for l in range(k + 1, len(search_females)):
                            f1, f2 = search_females[k], search_females[l]
                            
                            configs = [
                                ((m1, f1), (m2, f2)),
                                ((m1, f2), (m2, f1))
                            ]
                            
                            for team1, team2 in configs:
                                signature = self.get_match_signature(team1, team2)
                                
                                if signature in self.all_matches_played:
                                    continue
                                
                                # Check if at least ONE player in this match needs games
                                all_match_players = [team1[0], team1[1], team2[0], team2[1]]
                                has_player_needing_match = any(p in players_needing_matches for p in all_match_players)
                                
                                if not has_player_needing_match:
                                    continue  # Skip this match, it would be all helpers
                                
                                score = self.calculate_match_score(team1, team2, current_round)
                                
                                if score < best_score:
                                    best_score = score
                                    best_match = (team1, team2)
            
            if best_match is None:
                break
            
            selected_matches.append(best_match)
            team1, team2 = best_match
            used_players.update([team1[0], team1[1], team2[0], team2[1]])
            
            signature = self.get_match_signature(team1, team2)
            self.all_matches_played.add(signature)
        
        return selected_matches, used_players
    
    def update_player_stats(self, match, round_num):
        """Update statistics after a match is scheduled"""
        team1, team2 = match
        
        for player in [team1[0], team1[1], team2[0], team2[1]]:
            self.player_stats[player]['matches'] += 1
            self.player_stats[player]['last_round_played'] = round_num  # Track last round played
        
        self.partner_count[team1[0]][team1[1]] += 1
        self.partner_count[team1[1]][team1[0]] += 1
        self.partner_count[team2[0]][team2[1]] += 1
        self.partner_count[team2[1]][team2[0]] += 1
        
        for p1 in [team1[0], team1[1]]:
            for p2 in [team2[0], team2[1]]:
                self.player_stats[p1]['opponents'][p2] += 1
                self.player_stats[p2]['opponents'][p1] += 1
    
    def calculate_target_matches(self):
        """
        Calculate target matches so each man plays with each woman at least once.
        In a perfect mixed Americano, each player should partner with all opposite gender players.
        """
        return self.num_players
    
    def get_current_min_matches(self):
        """Get the current minimum number of matches any player has played"""
        all_players = self.male_players + self.female_players
        if not all_players:
            return 0
        return min(self.player_stats[p]['matches'] for p in all_players)
    
    def can_generate_full_round(self):
        """Check if we can still generate a full round with all fields"""
        # Simulate finding matches without actually adding them
        temp_used = set()
        temp_matches = 0
        players_needing = set(self.get_players_needing_matches())
        
        # Try to find num_fields matches
        for _ in range(self.num_fields):
            available_males = [m for m in self.male_players if m not in temp_used]
            available_females = [f for f in self.female_players if f not in temp_used]
            
            if len(available_males) < 2 or len(available_females) < 2:
                break
            
            # Check if any available player needs matches
            has_player_needing = any(m in players_needing for m in available_males) or \
                                any(f in players_needing for f in available_females)
            
            if not has_player_needing:
                break
            
            # Just mark 2 males and 2 females as used (simplified check)
            if available_males and available_females and len(available_males) >= 2 and len(available_females) >= 2:
                temp_used.update([available_males[0], available_males[1], 
                                available_females[0], available_females[1]])
                temp_matches += 1
        
        return temp_matches >= self.num_fields
    
    def get_players_in_matches(self, matches):
        """Get set of all players in a list of matches"""
        players = set()
        for match in matches:
            players.update([match[0][0], match[0][1], match[1][0], match[1][1]])
        return players
    
    def matches_conflict(self, match, existing_matches):
        """Check if a match has any player already in existing matches"""
        existing_players = self.get_players_in_matches(existing_matches)
        match_players = set([match[0][0], match[0][1], match[1][0], match[1][1]])
        return bool(existing_players & match_players)
    
    def try_fill_round_from_pending(self, current_matches, pending_matches, max_size):
        """Try to fill current round with non-conflicting pending matches"""
        added_matches = []
        remaining_pending = []
        
        for pending_match in pending_matches:
            if len(current_matches) + len(added_matches) < max_size:
                if not self.matches_conflict(pending_match, current_matches + added_matches):
                    added_matches.append(pending_match)
                else:
                    remaining_pending.append(pending_match)
            else:
                remaining_pending.append(pending_match)
        
        return added_matches, remaining_pending
    
    def generate_schedule(self):
        """Generate the complete tournament schedule"""
        target_matches_per_player = self.calculate_target_matches()
        
        round_num = 0
        consecutive_empty_rounds = 0
        max_rounds = 50  # Safety limit
        pending_matches = []  # Store matches that couldn't fill a round
        
        while consecutive_empty_rounds < 3 and round_num < max_rounds:
            round_num += 1
            
            match_counts = [self.player_stats[p]['matches'] for p in 
                          self.male_players + self.female_players]
            min_matches = min(match_counts) if match_counts else 0
            max_matches = max(match_counts) if match_counts else 0
            
            # Update minimum matches reached
            self.min_matches_reached = min_matches
            
            # Check if everyone has reached target AND is balanced
            if min_matches >= target_matches_per_player and (max_matches - min_matches) <= 1:
                break
            
            round_matches, used_players = self.find_best_matches_for_round(self.num_fields, round_num)
            
            if not round_matches:
                consecutive_empty_rounds += 1
                continue
            
            # ALWAYS try to add non-conflicting pending matches first
            if pending_matches:
                added_from_pending, pending_matches = self.try_fill_round_from_pending(
                    round_matches, pending_matches, self.num_fields
                )
                round_matches = added_from_pending + round_matches
            
            # Check if this round is STILL incomplete after trying to add pending
            if len(round_matches) < self.num_fields:
                # Only hold matches if we can generate more full rounds in the future
                if self.can_generate_full_round():
                    # Store these matches and DON'T create this round yet
                    pending_matches.extend(round_matches)
                    
                    # Update stats for these matches
                    for match in round_matches:
                        self.update_player_stats(match, round_num)
                    
                    continue
                # else: we're near the end, so create the round even if incomplete
            
            consecutive_empty_rounds = 0
            
            # Determine who's resting
            all_players = set(self.male_players + self.female_players)
            playing_players = self.get_players_in_matches(round_matches)
            resting_players = list(all_players - playing_players)
            
            self.rounds.append({
                'matches': round_matches,
                'resting': resting_players
            })
            
            # Update stats only for matches not previously in pending
            # (pending matches were already updated when they were added to pending)
            updated_matches = set()
            for match in round_matches:
                # Create a simple signature to check if already updated
                match_sig = self.get_match_signature(match[0], match[1])
                if match_sig not in updated_matches:
                    # Check if this match was newly generated (not from pending)
                    match_was_pending = any(
                        self.get_match_signature(pm[0], pm[1]) == match_sig 
                        for pm in pending_matches
                    )
                    
                    # Count in previous rounds
                    already_in_previous = False
                    for prev_round in self.rounds[:-1]:
                        for prev_match in prev_round['matches']:
                            if self.get_match_signature(prev_match[0], prev_match[1]) == match_sig:
                                already_in_previous = True
                                break
                        if already_in_previous:
                            break
                    
                    if not match_was_pending and not already_in_previous:
                        self.update_player_stats(match, round_num)
                        updated_matches.add(match_sig)
        
        # Distribute remaining pending matches across final rounds
        while pending_matches:
            current_round = []
            remaining = []
            
            for match in pending_matches:
                if len(current_round) < self.num_fields:
                    if not self.matches_conflict(match, current_round):
                        current_round.append(match)
                    else:
                        remaining.append(match)
                else:
                    remaining.append(match)
            
            pending_matches = remaining
            
            if current_round:
                all_players = set(self.male_players + self.female_players)
                playing_players = self.get_players_in_matches(current_round)
                resting_players = list(all_players - playing_players)
                
                self.rounds.append({
                    'matches': current_round,
                    'resting': resting_players
                })
            else:
                # If we can't place any match without conflicts, force one and break
                if pending_matches:
                    match = pending_matches[0]
                    all_players = set(self.male_players + self.female_players)
                    playing_players = self.get_players_in_matches([match])
                    resting_players = list(all_players - playing_players)
                    
                    self.rounds.append({
                        'matches': [match],
                        'resting': resting_players
                    })
                    pending_matches = pending_matches[1:]
        
        return self.rounds
    
    def format_for_streamlit(self):
        """Format schedule for Streamlit visualization with helper logic"""
        formatted_rounds = []
        
        # Calculate the minimum matches (determines valid games)
        all_players = self.male_players + self.female_players
        final_min_matches = min(self.player_stats[p]['matches'] for p in all_players)
        
        for round_num, round_data in enumerate(self.rounds, 1):
            partidos = []
            
            for cancha_num, match in enumerate(round_data['matches'], 1):
                team1, team2 = match
                all_players_in_match = list(team1) + list(team2)
                
                # NEW: Determine helpers - players who exceed the minimum matches
                helpers = []
                valido_para = []
                
                for player in all_players_in_match:
                    player_matches_so_far = self.player_stats[player]['matches']
                    
                    # We need to count matches UP TO this round
                    # Count how many times this player appears in previous rounds + current
                    matches_before_this = 0
                    for prev_round_idx, prev_round in enumerate(self.rounds[:round_num]):
                        for prev_match in prev_round['matches']:
                            if player in prev_match[0] or player in prev_match[1]:
                                matches_before_this += 1
                    
                    # Check if this player has already reached minimum at time of this match
                    # They're a helper if they've already played >= final_min_matches
                    if matches_before_this > final_min_matches:
                        helpers.append(player)
                    else:
                        valido_para.append(player)
                
                partido = {
                    "cancha": cancha_num,
                    "pareja1": list(team1),
                    "pareja2": list(team2),
                    "ayudantes": helpers,
                    "valido_para": valido_para if valido_para else all_players_in_match
                }
                partidos.append(partido)
            
            formatted_rounds.append({
                "ronda": round_num,
                "partidos": partidos,
                "descansan": round_data['resting']
            })
        
        # Generate summary with valid vs helper games
        resumen_data = []
        for player in all_players:
            total_matches = self.player_stats[player]['matches']
            valid_matches = min(total_matches, final_min_matches)
            helper_matches = max(0, total_matches - final_min_matches)
            
            resumen_data.append({
                "Jugador": player,
                "Partidos": total_matches,
                "Partidos Válidos": valid_matches,
                "Partidos Ayudante": helper_matches,
                "Descansos": len(self.rounds) - total_matches
            })
        
        return {
            "rondas": formatted_rounds,
            "resumen": resumen_data,
            "min_matches": final_min_matches
        }


def generar_torneo_mixto(male_players, female_players, num_canchas, puntos_partido):
    """Generate mixed Americano tournament - each man plays with each woman"""
    tournament = AmericanoPadelTournament(male_players, female_players, 
                                          num_canchas, puntos_partido)
    tournament.generate_schedule()
    return tournament.format_for_streamlit()