import datetime

class Flashcard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.interval = 0  # Days until next review
        self.ease_factor = 2.5 # How easily the interval increases
        self.last_reviewed = None
        self.next_review = datetime.date.today() # Initially due today

    def __repr__(self):
        return f"Card('{self.question}', due: {self.next_review})"

    def review(self, quality, current_date):
        """
        Updates card's interval and ease factor based on review quality.
        Quality: 0-5 (0-2: incorrect, 3: hard, 4: good, 5: easy)
        This implements a simplified SuperMemo 2 (SM-2) algorithm, a science-backed method.
        """
        self.last_reviewed = current_date

        if quality >= 3: # Correct answer
            if self.interval == 0: # First correct answer
                self.interval = 1
            elif self.interval == 1: # Second correct answer
                self.interval = 6
            else:
                self.interval = round(self.interval * self.ease_factor)
            
            self.ease_factor += (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        else: # Incorrect answer
            self.interval = 1 # Reset interval to 1 day for immediate re-learning
            self.ease_factor -= 0.2
        
        # Ensure ease factor doesn't drop too low
        if self.ease_factor < 1.3:
            self.ease_factor = 1.3
        
        # Ensure interval is at least 1 if correct (prevents 0-day intervals)
        if self.interval < 1 and quality >= 3:
            self.interval = 1

        # Schedule the next review based on the calculated interval
        self.next_review = current_date + datetime.timedelta(days=self.interval)

def main():
    cards = [
        Flashcard("What is the capital of France?", "Paris"),
        Flashcard("What is 7 times 8?", "56"),
        Flashcard("Who painted the Mona Lisa?", "Leonardo da Vinci"),
        Flashcard("What is the chemical symbol for water?", "H2O"),
        Flashcard("What is the largest ocean on Earth?", "Pacific Ocean"),
        Flashcard("What is the square root of 81?", "9"),
    ]

    print("Welcome to the Active Learning Spaced Repetition Simulator!")
    print("This tool demonstrates science-backed learning strategies: active recall and spaced repetition.")
    print("Try to answer the questions. After each answer, rate your recall (0-5).")
    print("0-2: Incorrect, 3: Hard, 4: Good, 5: Easy")
    print("-" * 60)

    current_date = datetime.date.today()
    session_count = 0

    while True:
        session_count += 1
        print(f"\n--- Learning Session {session_count} (Simulated Date: {current_date}) ---")
        
        # Filter cards due for review on the current simulated date
        # This is the core "spaced repetition" mechanism, scheduling items based on memory decay.
        due_cards = [card for card in cards if card.next_review <= current_date]
        
        if not due_cards:
            print(f"No cards due for review on {current_date}. All cards are learned for now or scheduled for later!")
            
            # Find the earliest next review date to suggest advancing
            earliest_next_review = None
            for card in cards:
                # Only consider cards scheduled for *after* the current date
                if card.next_review > current_date:
                    if earliest_next_review is None or card.next_review < earliest_next_review:
                        earliest_next_review = card.next_review
            
            if earliest_next_review:
                print(f"The next card(s) will be due on {earliest_next_review}.")
                advance_choice = input(f"Advance simulated date to {earliest_next_review} (y/n)? (or 'q' to quit): ").lower()
                if advance_choice == 'y':
                    current_date = earliest_next_review
                    continue # Start new session with advanced date
                elif advance_choice == 'q':
                    break
                else:
                    print("Quitting simulator.")
                    break
            else:
                print("All cards are fully learned and scheduled far into the future. Exiting.")
                break

        print(f"{len(due_cards)} card(s) due for review:")
        for card in due_cards:
            print(f"\nQuestion: {card.question}")
            # This input prompts the user to actively recall the answer before revealing it.
            # This is the "active recall" strategy, crucial for strengthening memory.
            input("Press Enter to reveal answer...") 
            print(f"Answer: {card.answer}")
            
            while True:
                try:
                    quality = int(input("How well did you recall? (0-5): "))
                    if 0 <= quality <= 5:
                        break
                    else:
                        print("Please enter a number between 0 and 5.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            
            card.review(quality, current_date) # Pass current_date to ensure consistent simulation
            print(f"  -> Next review for '{card.question}' in {card.interval} days (on {card.next_review}).")
        
        # After reviewing all due cards for the current_date, prompt to advance the date.
        cont = input("\nSession complete. Press Enter to advance simulated date by 1 day, or 'q' to quit: ")
        if cont.lower() == 'q':
            break
        current_date += datetime.timedelta(days=1)

if __name__ == "__main__":
    main()
