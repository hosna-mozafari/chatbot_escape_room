from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

puzzle_hints = {
    "son_puzzle": ["You can have it if you are married (You have used 1/3 hints for the current puzzle)", "When they grow up they can become super annoying (You have used 2/3 hints for the current puzzle)", "It starts with the letter S and ends with the letters ON (You have used 3/3 hints for the current puzzle)"],
    "math_puzzle": ["There is a relation between the actual sum of the numbers! (You have used 1/3 hints for the current puzzle)", "It is easier than you think! The multiplication grows sequentially! (You have used 2/3 hints for the current puzzle)", "It is a digit of 3 numbers and starts with the number 2. (You have used 3/3 hints for the current puzzle)"],
    "east_puzzle": ["I suggest to look around (You have used 1/2 hints for the current puzzle)", "Look for something related to the answer of the previous puzzle in another direction! (You have used 2/2 hints for the current puzzle)"],
    "north_puzzle": ["I suggest to look around (You have used 1/2 hints for the current puzzle)", "You can figure it out from the answer of the previous puzzle! (You have used 2/2 hints for the current puzzle)"],
    "chess_puzzle": ["Pay attention to the activities of other people! They may need another one to accomplish their job! (You have used 1/3 hints for the current puzzle)", "Maybe he is involved with another one! (You have used 2/3 hints for the current puzzle)", "There is a Person who cannot do their job/activity without another person (You have used 3/3 hints for the current puzzle)"],
    "activate_puzzle": ["The spaceship's power is down. Look around to find more clues. (You have used 1/3 hints for the current puzzle)", "Take a closer look at the captain's chair (You have used 2/3 hints for the current puzzle)", "Try to turn on the power switch! (You have used 3/3 hints for the current puzzle)"],
    "direction_puzzle": ["I suggest you to choose a direction to go! (You have used 1/1 hints for the current puzzle)"],
    "wires_puzzle": ["Try taking a closer look to the navigation screen (You have used 1/3 hints for the current puzzle)", "Maybe there is someting wrong with the wires (You have used 2/3 hints for the current puzzle)", "Check the wires and if you haved already done that then try reconnecting one of the cables with the smallest current! (You have used 3/3 hints for the current puzzle)"],
    "signal_puzzle": ["Try taking a closer look to the communication console (You have used 1/3 hints for the current puzzle)", "Press the left or the right button to position the satellite and improve the amplifier signal (You have used 2/3 hints for the current puzzle)", "The strongest signal is related to the current time (You have used 3/3 hints for the current puzzle)"]
}

class ActionSayName(Action):

    def name(self) -> Text:
        return "action_say_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        current_room = tracker.get_slot("current_room")
        is_game_over = tracker.get_slot("is_game_over")
        
        if is_game_over:
            dispatcher.utter_message("The game is over. Please refresh the page to start a new session.")
            return[]

        if not name:
            dispatcher.utter_message(text="I don't know your name.")
            return[]

        if current_room:
            if current_room != "hosna_room":
                dispatcher.utter_message(f"Hey, please focus on the game!")
                return[]
        else:
            if tracker.get_slot("current_puzzle_to_solve") is None:
                dispatcher.utter_message(text=f"Hi {name}, Delwan is a young programmer who was working on a Chabot game when she suddenly fell asleep. In her dream, she heard a voice and woke up, but to her surprise, she found herself trapped in her own nightmare. As you begin playing the game in this room, you become stuck with her. Delwan is confused and unable to figure out how to escape. Your help is crucial, or both of you will remain trapped forever! First and foremost, you should know that you need a password to open the door.")
                dispatcher.utter_message(text="Be careful and pay attention to all the objects you come across. To obtain the password, you must solve three puzzles. The answer of the first puzzle will be a clue for the second one, and the answer of the second puzzle will be a clue for the last one. By solving the final puzzle, you will receive the password!")
                dispatcher.utter_message(text="You can always ask for help anytime!")
                dispatcher.utter_message(text="Are you ready to start?")

                return [SlotSet("name", name), SlotSet("current_puzzle_to_solve", "direction_puzzle"), SlotSet("lives", 5), SlotSet("current_room", "hosna_room"), SlotSet("signal_position", 5)]
            else:
                dispatcher.utter_message(text=f"Sorry I don't understand. Can you rephrase it?")
                return []

class ActionAffirmStartGame(Action):

    def name(self) -> Text:
        return "action_handle_affirmation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        is_game_over = tracker.get_slot("is_game_over")
        if is_game_over:
            dispatcher.utter_message("The game is over. Please refresh the page to start a new session.")
            return[]

        is_already_started = tracker.get_slot("is_already_started")
        if is_already_started:
            name = tracker.get_slot("name")
            if name:
                dispatcher.utter_message(f"Hey Focus on the game!")
                return[]
            dispatcher.utter_message("Hey Focus on the game!")
            return[]
        intent = tracker.get_intent_of_latest_message()

        name = tracker.get_slot("name")
        if name is None:
            dispatcher.utter_message("Hey you must tell me your name first!")
            return[]
        

        if intent == "affirm_to_play":
            dispatcher.utter_message("You woke up in the center of the room!")
            dispatcher.utter_message("In the north you see a window overlooking the ocean (yes that's weird because she is living in the jungle where polar bears are living!). You can enjoy a beautiful sunset there!")
            dispatcher.utter_message("On the east you see a table with some objects on it.")
            dispatcher.utter_message("On the south there is door which seems to be the exit door!")
            dispatcher.utter_message("On the west you see a board with some lines written on it and also a broken chair")
            dispatcher.utter_message("Which direction do you want to go?")
        elif intent == "deny_to_play":
            dispatcher.utter_message("I was just being nice! You have no choice! Play or die!")
            dispatcher.utter_message("In the north you see a window overlooking the ocean (yes that's weird because she is living in the jungle where polar bears are living!). You can enjoy a beautiful sunset there!")
            dispatcher.utter_message("On the east you see a table with some objects on it.")
            dispatcher.utter_message("On the south there is door which seems to be the exit door!")
            dispatcher.utter_message("On the west you see a board with some lines written on it and also a broken chair")
            dispatcher.utter_message("Which direction do you want to go?")
        else:
            dispatcher.utter_message("I'm sorry, I didn't understand. Can you please clarify?")

        return [SlotSet("is_already_started", True)]

class ActionGiveDirection(Action):

    def name(self) -> Text:
        return "action_handle_direction"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        is_game_over = tracker.get_slot("is_game_over")
        if is_game_over:
            dispatcher.utter_message("The game is over. Please refresh the page to start a new session.")
            return[]

        direction = tracker.get_slot("direction")
        current_room = tracker.get_slot("current_room")

        name = tracker.get_slot("name")


        if current_room:
            if current_room != "hosna_room":
                dispatcher.utter_message(f"Hey, please focus on the game!")
                return[]

        if direction:
            if direction == "west":
                is_puzzle_already_solved = tracker.get_slot("is_son_puzzle_solved")
                if is_puzzle_already_solved:
                    dispatcher.utter_message(text=f"You have already solved this riddle. Look around for more clues.")
                    return []

                dispatcher.utter_message("There is a puzzle on the board")
                dispatcher.utter_message("Brothers and sisters have I none, but the father of the man is the father of my son. What is man's relationship with me?")
                return [SlotSet("current_puzzle_to_solve", "son_puzzle")]

            if direction == "east":
                son_puzzle_solved = tracker.get_slot("is_son_puzzle_solved")

                if not son_puzzle_solved:
                    dispatcher.utter_message(text=f"You can't go there yet. You have to explore other directions first!")
                    return[]

                is_puzzle_already_solved = tracker.get_slot("is_math_puzzle_solved")
                if is_puzzle_already_solved:
                    dispatcher.utter_message(text=f"You have already solved this riddle. Look around for more clues.")
                    return []
                dispatcher.utter_message("There are two laptops on the table. You are able to select one of them. Be careful! If you choose the wrong one you will lose a life! One of them works with IOS operating system and the other one with windows! Which one do you want?")
                return [SlotSet("current_puzzle_to_solve", "east_puzzle")]
            if direction == "north":
                dispatcher.utter_message("You are enjoying a beautiful sunset from the window or maybe windows. Remeber this for the east puzzle!")
                return [SlotSet("current_puzzle_to_solve", "north_puzzle")]
            if direction == "south":
                # dispatcher.utter_message("The bear next to the door seems to be a doll but it is not!! It has a tiny little red hat with a flower on it! His hand is in his pocket which has a picture of a fish on it!")
                # dispatcher.utter_message("What do you want to do?")

                last_two_puzzles_solved = tracker.get_slot("is_son_puzzle_solved") and tracker.get_slot("is_math_puzzle_solved")

                if not last_two_puzzles_solved:
                    dispatcher.utter_message("Sorry, you can't go to the south yet. Explore other directions first!")
                    return []

                dispatcher.utter_message("There is a safe box. Solve the following puzzle to open it and get the key for the exit door!")
                dispatcher.utter_message("There are 4 people in a room, Sam is reading, Mahsa is watching TV, Rayan is playing chess. What is Sepehr doing?")
                return [SlotSet("current_puzzle_to_solve", "chess_puzzle")]
        else:
            dispatcher.utter_message("Sorry try again!")
        return []


class ActionSonPuzzle(Action):
    def __init__(self):
        self.puzzle_name = "son_puzzle"

    def name(self) -> Text:
        return "action_son_puzzle"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        is_game_over = tracker.get_slot("is_game_over")
        if is_game_over:
            dispatcher.utter_message("The game is over. Please refresh the page to start a new session.")
            return[]

        name = tracker.get_slot("name")

        current_room = tracker.get_slot("current_room")
        if current_room:
            if current_room != "hosna_room":
                dispatcher.utter_message(f"Hey, please focus on the game!")
                return[]


        is_puzzle_already_solved = tracker.get_slot("is_son_puzzle_solved")
        if is_puzzle_already_solved:
            dispatcher.utter_message(text=f"You are talking nonsenses")
            return []

        current_puzzle_to_be_solved = tracker.get_slot("current_puzzle_to_solve")

        if current_puzzle_to_be_solved:
            if current_puzzle_to_be_solved != self.puzzle_name:
                dispatcher.utter_message(text=f"Sorry I don't understand. Can you rephrase it?")
                return []

        son_answer = tracker.get_slot("son_answer")

        if son_answer:
            if son_answer.lower() == "son":
                dispatcher.utter_message(text=f'Correct! Remember this answer for the next puzzle')
                dispatcher.utter_message(text=f"Now where do you want to go?")
                return[SlotSet("is_son_puzzle_solved", True)]
            else:
                dispatcher.utter_message(text=f"Wrong answer! Try again!")
        return []

class ActionMathPuzzle(Action):
    def __init__(self):
        self.puzzle_name = "math_puzzle"

    def name(self) -> Text:
        return "action_math_puzzle"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        is_game_over = tracker.get_slot("is_game_over")
        if is_game_over:
            dispatcher.utter_message("The game is over. Please refresh the page to start a new session.")
            return[]

        current_room = tracker.get_slot("current_room")
        if current_room:
            if current_room == "tareq_room":
                lock_answer = tracker.get_slot("math_answer")
                is_easter_egg_solved = tracker.get_slot("is_easter_egg_solved")
                if is_easter_egg_solved:
                    dispatcher.utter_message("You have already solved the combination lock for the compartment.")
                    return[]
                if lock_answer == "39104":
                    current_lives = tracker.get_slot("lives")
                    dispatcher.utter_message("Yes! You have opened the compartment and found a medal with the inscription 'I <3 M'")
                    dispatcher.utter_message(f"You also unlocked the achievement 'True Explorer' and gain an extra life. You have {current_lives+1} lives left.")
                    dispatcher.utter_message("Keep exploring and to find more achivements to brag about!")
                    return[SlotSet("lives", current_lives+1), SlotSet("is_easter_egg_solved", True)]
                else:
                    dispatcher.utter_message(f"The code {lock_answer} is wrong. Please try again.")
                return[]


        is_puzzle_already_solved = tracker.get_slot("is_math_puzzle_solved")
        if is_puzzle_already_solved:
            dispatcher.utter_message(text=f"You are talking nonsenses")
            return []

        current_puzzle_to_be_solved = tracker.get_slot("current_puzzle_to_solve")

        if current_puzzle_to_be_solved:
            if current_puzzle_to_be_solved != self.puzzle_name:
                dispatcher.utter_message(text=f"Sorry I don't understand. Can you rephrase it?")
                return []

        math_answer = tracker.get_slot("math_answer")

        if math_answer:
            if math_answer.lower() == "two hundred ninety six" or math_answer == "296":
                
                dispatcher.utter_message(text=f"Right! You are doing well!")
                dispatcher.utter_message(text=f"You see a picture of a safe box. Look around to find the misterious safe box!")
                dispatcher.utter_message(text=f"Where do you want to explore now?")
                return[SlotSet("is_math_puzzle_solved", True)]
                # return[]

            else:
                dispatcher.utter_message(text=f"Wrong answer! Try again!")
        return []


class DefaultFallbackAction(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        is_game_over = tracker.get_slot("is_game_over")
        if is_game_over:
            dispatcher.utter_message("The game is over. Please refresh the page to start a new session.")
            return[]

        # Custom fallback response message
        fallback_message = "I'm sorry, I didn't understand. Can you please rephrase your message?"

        # Send the fallback message
        dispatcher.utter_message(text=fallback_message)

        return []



class GetHints(Action):
    def name(self) -> Text:
        return "action_get_hints"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        is_game_over = tracker.get_slot("is_game_over")
        if is_game_over:
            dispatcher.utter_message("The game is over. Please refresh the page to start a new session.")
            return[]

        if tracker.get_slot("current_puzzle_to_solve") is None:
            dispatcher.utter_message(text="There are no puzzles yet! Please enter your name first!")
            return[]

        current_puzzle = tracker.get_slot("current_puzzle_to_solve")

        if current_puzzle == "son_puzzle":
            current_hint_attempt = tracker.get_slot("son_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0

            if current_hint_attempt > 2:
                current_hint_attempt = 2

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("son_puzzle_hint_count", current_hint_attempt + 1)]

        if current_puzzle == "math_puzzle":
            current_hint_attempt = tracker.get_slot("math_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0

            if current_hint_attempt > 2:
                current_hint_attempt = 2

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("math_puzzle_hint_count", current_hint_attempt + 1)]
        

        if current_puzzle == "east_puzzle":
            current_hint_attempt = tracker.get_slot("east_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 1:
                current_hint_attempt = 1

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("east_puzzle_hint_count", current_hint_attempt + 1)]

        if current_puzzle == "north_puzzle":
            current_hint_attempt = tracker.get_slot("north_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 1:
                current_hint_attempt = 1

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("north_puzzle_hint_count", current_hint_attempt + 1)]

        if current_puzzle == "south_puzzle":
            current_hint_attempt = tracker.get_slot("south_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 1:
                current_hint_attempt = 1

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("south_puzzle_hint_count", current_hint_attempt + 1)]

        if current_puzzle == "chess_puzzle":
            current_hint_attempt = tracker.get_slot("chess_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 2:
                current_hint_attempt = 2

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("chess_puzzle_hint_count", current_hint_attempt + 1)]


        if current_puzzle == "activate_puzzle":
            current_hint_attempt = tracker.get_slot("activate_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 2:
                current_hint_attempt = 2

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("activate_puzzle_hint_count", current_hint_attempt + 1)]

        if current_puzzle == "wires_puzzle":
            current_hint_attempt = tracker.get_slot("wires_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 2:
                current_hint_attempt = 2

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("wires_puzzle_hint_count", current_hint_attempt + 1)]

        if current_puzzle == "signal_puzzle":
            current_hint_attempt = tracker.get_slot("signal_puzzle_hint_count")
            if current_hint_attempt is None:
                current_hint_attempt = 0
                
            if current_hint_attempt > 2:
                current_hint_attempt = 2

            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][current_hint_attempt]}")
            return[SlotSet("signal_puzzle_hint_count", current_hint_attempt + 1)]


        if current_puzzle == "direction_puzzle":
            dispatcher.utter_message(text=f"{puzzle_hints[current_puzzle][0]}")
            return[]

        


class ActionPickItem(Action):
    def name(self) -> Text:
        return "action_pick_something"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        is_game_over = tracker.get_slot("is_game_over")
        if is_game_over:
            dispatcher.utter_message("The game is over. Please refresh the page to start a new session.")
            return[]

        picked_item = tracker.get_slot("picked_item")
        current_puzzle_to_be_solve = tracker.get_slot("current_puzzle_to_solve")

        if picked_item:
            current_room = tracker.get_slot("current_room")
            if current_room != "hosna_room":
                dispatcher.utter_message("Sorry is not possible!")
                return[]
            if picked_item == "laptop" or picked_item == "computer" or picked_item == "notebook":
                dispatcher.utter_message("Please select one of the 2 existing types of laptops! (Ios or Windows)")

            elif picked_item.find("ios") != -1:
                current_lives = tracker.get_slot("lives")
                if current_lives:
                    if current_lives - 1 < 1:
                        dispatcher.utter_message(text=f"GAME OVER.")
                        dispatcher.utter_message(text=f"If you want to play again please refresh the page.")
                        return[SlotSet("is_game_over", True)]
                    dispatcher.utter_message("You picked the wrong one!")
                    dispatcher.utter_message(text=f"You have lost 1 life! You have {current_lives-1} lives left.")
                    return [SlotSet("lives", current_lives-1)]

            elif picked_item.lower().find("windows") != -1:
                dispatcher.utter_message("You can see a puzzle on the screen saver. Solve it to turn it on!")
                dispatcher.utter_message("According to the first three equations, try to find the answer to the fourth one.")
                dispatcher.utter_message("21+10=31")
                dispatcher.utter_message("22+20=84")
                dispatcher.utter_message("23+30=159")
                dispatcher.utter_message("24+50=?")

                return [SlotSet("current_puzzle_to_solve", "math_puzzle")]
            else:
                dispatcher.utter_message(f"You can't pick the {picked_item}!")
        else:
            dispatcher.utter_message(f"No Item was picked")

        return []


class ActionLookItem(Action):
    def name(self) -> Text:
        return "action_look_at"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        is_game_over = tracker.get_slot("is_game_over")
        if is_game_over:
            dispatcher.utter_message("The game is over. Please refresh the page to start a new session.")
            return[]

        looked_item = tracker.get_slot("looked_item")

        if looked_item:
            # if looked_item == "pocket":
            #     current_room = tracker.get_slot("current_room")
            #     if current_room == "hosna_room":
            #         dispatcher.utter_message("You found the last puzzle in his pocket")
            #         dispatcher.utter_message("There are 4 people in a room, Sam is reading, Mahsa is watching TV, Rayan is playing chess, what Sepehr is doing?")
            #         return[SlotSet("current_puzzle_to_solve", "chess_puzzle")]
            #     else:
            #         dispatcher.utter_message(f"There is no such {looked_item}. Try something else!")
            #         return[]

            if looked_item.lower() == "son":
                current_room = tracker.get_slot("current_room")
                if current_room == "hosna_room":
                    dispatcher.utter_message("There is no son but there is a beautiful sunset in the north!")
                    return[]
                else:
                    dispatcher.utter_message(f"There is no such {looked_item}. Try something else!")
                    return[]

            if looked_item.lower() == "around" or looked_item.lower() == "surroundings" or looked_item.lower() == "surrounding":
                current_room = tracker.get_slot("current_room")
                if current_room == "tareq_room":
                    dispatcher.utter_message("In the middle of the room stands the captain's chair.")
                    dispatcher.utter_message("In front there is the navigation screen.")
                    dispatcher.utter_message("There is also an airlock door leading to the escape pods.")
                    dispatcher.utter_message("Next to the captain's chair is the communication console.")
                    return[]
                if current_room == "hosna_room":
                    dispatcher.utter_message("In the north you see a window overlooking the ocean (yes that's weird because she is living in the jungle where polar bears are living!). You can enjoy a beautiful sunset there!")
                    dispatcher.utter_message("In the east you see a table with some objects on it.")
                    dispatcher.utter_message("In the south there is door which seems to be the exit door!")
                    dispatcher.utter_message("In the west you see a board with some lines written on it and also a broken chair")
                    return[]
            if looked_item.lower().find("captain") != -1 or looked_item.lower().find("chair") != -1:
                current_room = tracker.get_slot("current_room")
                if current_room == "tareq_room":
                    dispatcher.utter_message("The captain's chair is equipped with several controls and a power switch, which is currently turned OFF. Nearby there is a compartment for storing essential items.")
                    return[]
                else:
                    dispatcher.utter_message(f"There is no such {looked_item}. Try something else!")
                    return[]

            if looked_item.lower().find("navigation") != -1 or looked_item.lower().find("screen") != -1:
                current_room = tracker.get_slot("current_room")
                if current_room == "tareq_room":
                    is_activate_solved = tracker.get_slot("is_activate_solved")
                    if is_activate_solved:
                        is_wires_puzzle_solved = tracker.get_slot("is_wires_puzzle_solved")
                        if is_wires_puzzle_solved:
                            dispatcher.utter_message("The navigation screen displays the current date and time: 16/08/2023 14:08")
                            return []
                        dispatcher.utter_message("The navigation screen displays a distorted star map. Some wires seem to be loose, indicating a possible malfunction.")
                        return[]
                    else:
                        dispatcher.utter_message("The navigation screen is currently inactive as it seems to be experiencing a lack of energy required for its proper functioning.")
                        return[]
                else:
                    dispatcher.utter_message(f"There is no such {looked_item}. Try something else!")
                    return[]

            if looked_item.lower().find("airlock") != -1 or looked_item.lower().find("door") != -1:
                current_room = tracker.get_slot("current_room")
                if current_room == "tareq_room":
                    dispatcher.utter_message("There's a numerical keypad on the side, suggesting a security lock.")
                    return[]
                else:
                    dispatcher.utter_message(f"There is no such {looked_item}. Try something else!")
                    return[]

            if looked_item.lower().find("communication") != -1 or looked_item.lower().find("console") != -1:
                current_room = tracker.get_slot("current_room")
                if current_room == "tareq_room":
                    dispatcher.utter_message(f"The communication console features a large window, which shows the vast expanse of outer space. A satellite dish, crucial for sending a distress signal, can be seen through the window. Additionally, on top of the console there is a LEFT and a RIGHT button to adjust the satellite position and a CENTER button to send the distress signal")
                    return[]
                else:
                    dispatcher.utter_message(f"There is no such {looked_item}. Try something else!")
                    return[]

            if looked_item.lower().find("wire") != -1:
                current_room = tracker.get_slot("current_room")
                if current_room == "tareq_room":
                    is_wires_puzzle_solved = tracker.get_slot("is_wires_puzzle_solved")
                    if is_wires_puzzle_solved:
                        dispatcher.utter_message("The red cable is already connected.")
                        return[]
                    dispatcher.utter_message(f"There are three different wires hanging loosely from the system. Each wire has a unique color and number assigned to it: a red wire labeled '1A' a green wire labeled '2A' and a blue wire labeled '3A'")
                    dispatcher.utter_message(f"Near the wires, you find a single input port that seems to belong to one of the wires. It appears to have suffered from an overload, potentially causing the system to shut down.")
                    dispatcher.utter_message(f"You might need to reconnect the wire correctly to restore the system's functionality and gain valuable information. But be careful, choosing the wrong cable can cost you your life and hinder your chances of escape!")
                    return[]
                else:
                    dispatcher.utter_message(f"There is no such {looked_item}. Try something else!")
                    return[]

            if looked_item.lower().find("compartment") != -1:
                current_room = tracker.get_slot("current_room")
                if current_room == "tareq_room":
                    dispatcher.utter_message(f"The compartment is locked with a 5 digit number. Next to the compartment there is a picture of the captain's hometown M...Please enter the digits to unlock it.")
                    return[]
                else:
                    dispatcher.utter_message(f"There is no such {looked_item}. Try something else!")
                    return[]

            else:
                dispatcher.utter_message(f"You can't look at that")
        else:
            dispatcher.utter_message(f"There is nothing to look at")
        return []

class ActionActivatePuzzle(Action):

    def __init__(self):
        self.puzzle_name = "activate_puzzle"

    def name(self) -> Text:
        return "action_activate_puzzle"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        is_game_over = tracker.get_slot("is_game_over")
        if is_game_over:
            dispatcher.utter_message("The game is over. Please refresh the page to start a new session.")
            return[]

        name = tracker.get_slot("name")

        current_room = tracker.get_slot("current_room")
        name = tracker.get_slot("name")
        if current_room:
            if current_room != "tareq_room":
                dispatcher.utter_message(f"Hey, please focus on the game!")
                return[]

        current_puzzle_to_be_solve = tracker.get_slot("current_puzzle_to_solve")
        if current_puzzle_to_be_solve:
            if current_puzzle_to_be_solve == "activate_puzzle":
                dispatcher.utter_message("With the power supply restored, some systems begin to operate normally.")
                dispatcher.utter_message("Try exploring the surroundings to collect more clues!")
                return[SlotSet("current_puzzle_to_solve", "wires_puzzle"), SlotSet("is_activate_solved", True)]

        return[]


class ActionplayActivity(Action):
    def name(self) -> Text:
        return "action_play_activity"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        is_game_over = tracker.get_slot("is_game_over")
        if is_game_over:
            dispatcher.utter_message("The game is over. Please refresh the page to start a new session.")
            return[]

        name = tracker.get_slot("name")

        current_room = tracker.get_slot("current_room")
        if current_room:
            if current_room != "hosna_room":
                dispatcher.utter_message(f"Hey, please focus on the game!")
                return[]

        play_action = tracker.get_slot("play_action")

        if play_action:
            if play_action.lower() == "chess":
                dispatcher.utter_message("Yes! You opened the box and you got the key with the serial number 39104.")
                dispatcher.utter_message("Congratulations! You have successfully completed the first room!")
                dispatcher.utter_message("You woke up again but now you are a member of an elite team of astronauts aboard the spaceship Galactic Starfire. During a mission to explore the far reaches of the galaxy, the ship gets ensnared in a mysterious space anomaly that causes critical malfunctions. Your task is to repair the ship and escape the anomaly before it's too late!")
                dispatcher.utter_message("The room is filled with a soft humming sound, indicating that the ship's power is down.")
                dispatcher.utter_message("In the middle of the room stands the captain's chair.")
                dispatcher.utter_message("In front there is the navigation screen.")
                dispatcher.utter_message("There is also an airlock door leading to the escape pods.")
                dispatcher.utter_message("Next to the captain's chair is the communication console.")
                
                dispatcher.utter_message(f"You can always type 'look around' to gather useful information about your surroundings")


                dispatcher.utter_message(f"What do you want to do first?")
                return [SlotSet("current_room", "tareq_room"), SlotSet("current_puzzle_to_solve", "activate_puzzle")]


            else:
                dispatcher.utter_message(f"Sorry try again!")
        else:
            dispatcher.utter_message(f"Sorry I did not get it. Please rephrase your message")
        return []



class ActionUseItem(Action):
    def name(self) -> Text:
        return "action_use_item"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        is_game_over = tracker.get_slot("is_game_over")
        if is_game_over:
            dispatcher.utter_message("The game is over. Please refresh the page to start a new session.")
            return[]

        name = tracker.get_slot("name")

        current_room = tracker.get_slot("current_room")
        if current_room:
            if current_room != "tareq_room":
                dispatcher.utter_message(f"Hey, please focus on the game!")
                return[]

        used_item = tracker.get_slot("used_item")
        signal_position = tracker.get_slot("signal_position")
        current_puzzle_to_be_solve = tracker.get_slot("current_puzzle_to_solve")
        
        

        if used_item:
            if current_puzzle_to_be_solve == "activate_puzzle":
                if used_item.lower().find("left") != -1:
                    dispatcher.utter_message("You pressed the left button but nothing happened. Probably there is no energy to operate it")
                    return[]
                elif used_item.lower().find("right") != -1:
                    dispatcher.utter_message("You pressed the right button but nothing happened. Probably there is no energy to operate it")
                    return[]
                elif used_item.lower().find("center") != -1:
                    dispatcher.utter_message("You pressed the center button but nothing happened. Probably there is no energy to operate it")
                    return[]

            if current_puzzle_to_be_solve == "wires_puzzle":
                if used_item.lower().find("green") != -1 or used_item.lower().find("2a") != -1:
                    current_lives = tracker.get_slot("lives")
                    if current_lives:
                        dispatcher.utter_message(text=f"You have received a strong electrical charge and lost a life. You have {current_lives-1} lives left.")
                        dispatcher.utter_message(text=f"Try maybe with another one")
                        if current_lives-1 <= 0:
                            dispatcher.utter_message(text=f"GAME OVER")
                            dispatcher.utter_message(text=f"If you want to play again please refresh the page.")
                            return[SlotSet("is_game_over", True)]
                        return[SlotSet("lives", current_lives-1)]
                elif used_item.lower().find("blue") != -1 or used_item.lower().find("3a") != -1:
                    current_lives = tracker.get_slot("lives")
                    if current_lives:
                        dispatcher.utter_message(text=f"You have received a strong electrical charge and lost a life. You have {current_lives-1} lives left.")
                        dispatcher.utter_message(text=f"Try maybe with another one")
                        if current_lives-1 <= 0:
                            dispatcher.utter_message(text=f"GAME OVER")
                            dispatcher.utter_message(text=f"If you want to play again please refresh the page.")
                            return[SlotSet("is_game_over", True)]
                        return[SlotSet("lives", current_lives-1)]
                elif used_item.lower().find("red") != -1 or used_item.lower().find("1a") != -1:
                    dispatcher.utter_message("That was the right one!")
                    dispatcher.utter_message("The navigation system is now displaying the ship's current date and time: 16/08/2023 14:08")
                    dispatcher.utter_message("That information could be useful later - keep exploring!")
                    return [SlotSet("current_puzzle_to_solve", "signal_puzzle"), SlotSet("is_wires_puzzle_solved", True)]

                elif used_item.lower().find("left") != -1:
                    signal_position -= 1 
                    if signal_position <= 1:
                        signal_position = 1
                    dispatcher.utter_message(f"The the satellite dish was moved to the 14:0{signal_position} position.")
                    dispatcher.utter_message("You can send a distress signal but be careful cause there is not much energy left. Sending the wrong signal may come with risks!")
                    return[SlotSet("signal_position", signal_position)]
                elif used_item.lower().find("right") != -1:
                    signal_position += 1 
                    if signal_position >= 9:
                        signal_position = 9
                    dispatcher.utter_message(f"The the satellite dish was moved to the 14:0{signal_position} position.")
                    dispatcher.utter_message("You can send a distress signal but be careful cause there is not much energy left. Sending the wrong signal may come with risks!")
                    return[SlotSet("signal_position", signal_position)]

                elif used_item.lower().find("center") != -1:
                    signal_position = tracker.get_slot("signal_position")
                    is_activate_solved = tracker.get_slot("is_activate_solved")

                    if not is_activate_solved:
                        dispatcher.utter_message("You can't send anything at the moment")
                        return[]
        
                    if signal_position:
                        if signal_position == 8:
                            dispatcher.utter_message("Congratulations, brave astronaut! You've successfully aligned the satellite dish and sent a powerful distress signal to the coordinates Latitude: 52.1352507 and Longitude: 11.6388062. Your message has been received, and rescue ships are en route to your location. Help is on the way!")
                            dispatcher.utter_message("As you stand by the communication console, the anxiety and intensity of the mission begin to fade. A sense of surreal clarity washes over you, and you suddenly realize the truth – it was all a vivid dream. You take a deep breath, relieved to be safely back in the realm of reality. The control panels, the navigation screen, the airlock door – all dissolve into the fading echoes of the dream. You find yourself waking up in your own comfortable bed, surrounded by the familiar comforts of your home.")
                            return[SlotSet("is_game_over", True)]
                        else:
                            current_lives = tracker.get_slot("lives")
                            if current_lives:
                                dispatcher.utter_message("Uh-oh, it seems there might have been a slight miscalculation. The distress signal you sent encountered interference and failed to reach its intended destination.")
                                dispatcher.utter_message(f"You have lost precious time and a life. You have {current_lives-1} lives left.")
                                if current_lives-1 <= 0:
                                    dispatcher.utter_message(text=f"GAME OVER")
                                    dispatcher.utter_message(text=f"If you want to play again please refresh the page.")
                                    return[SlotSet("is_game_over", True)]
                                
                                return[SlotSet("lives", current_lives-1)]
                else:
                    dispatcher.utter_message(f"Sorry try again!")
            
            elif current_puzzle_to_be_solve == "signal_puzzle":
                if used_item.lower().find("left") != -1:
                    signal_position -= 1 
                    if signal_position <= 1:
                        signal_position = 1
                    dispatcher.utter_message(f"The the satellite dish was moved to the 14:0{signal_position} position.")
                    dispatcher.utter_message("You can send a distress signal but be careful cause there is not much energy left. Sending the wrong signal may come with risks!")
                    return[SlotSet("signal_position", signal_position)]

                elif used_item.lower().find("right") != -1:
                    signal_position += 1 
                    if signal_position >= 9:
                        signal_position = 9
                    dispatcher.utter_message(f"The the satellite dish was moved to the 14:0{signal_position} position.")
                    dispatcher.utter_message("You can send a distress signal but be careful cause there is not much energy left. Sending the wrong signal may come with risks!")
                    return[SlotSet("signal_position", signal_position)]

                
                elif used_item.lower().find("center") != -1:
                    signal_position = tracker.get_slot("signal_position")
                    is_activate_solved = tracker.get_slot("is_activate_solved")

                    if not is_activate_solved:
                        dispatcher.utter_message("You can't send anything at the moment")
                        return[]
        
                    if signal_position:
                        if signal_position == 8:
                            dispatcher.utter_message("Congratulations, brave astronaut! You've successfully aligned the satellite dish and sent a powerful distress signal to the coordinates Latitude: 52.1352507 and Longitude: 11.6388062. Your message has been received, and rescue ships are en route to your location. Help is on the way!")
                            dispatcher.utter_message("As you stand by the communication console, the anxiety and intensity of the mission begin to fade. A sense of surreal clarity washes over you, and you suddenly realize the truth – it was all a vivid dream. You take a deep breath, relieved to be safely back in the realm of reality. The control panels, the navigation screen, the airlock door – all dissolve into the fading echoes of the dream. You find yourself waking up in your own comfortable bed, surrounded by the familiar comforts of your home.")
                            return[SlotSet("is_game_over", True)]
                        else:
                            current_lives = tracker.get_slot("lives")
                            if current_lives:
                                dispatcher.utter_message("Uh-oh, it seems there might have been a slight miscalculation. The distress signal you sent encountered interference and failed to reach its intended destination.")
                                dispatcher.utter_message(f"You have lost precious time and a life. You have {current_lives-1} lives left.")
                                if current_lives-1 <= 0:
                                    dispatcher.utter_message(text=f"GAME OVER")
                                    dispatcher.utter_message(text=f"If you want to play again please refresh the page.")
                                    return[SlotSet("is_game_over", True)]
                                
                                return[SlotSet("lives", current_lives-1)]


                dispatcher.utter_message(f"You can't use the {used_item}")
                return[]
            else:
                dispatcher.utter_message(f"Sorry you can't use {used_item}!")
                return[]
        else:
            dispatcher.utter_message(f"Sorry I did not get it. Please rephrase your message")
        return []

class ActionSendSignal(Action):
    def name(self) -> Text:
        return "action_send_signal"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        is_game_over = tracker.get_slot("is_game_over")
        if is_game_over:
            dispatcher.utter_message("The game is over. Please refresh the page to start a new session.")
            return[]

        name = tracker.get_slot("name")

        current_room = tracker.get_slot("current_room")
        if current_room:
            if current_room != "tareq_room":
                dispatcher.utter_message(f"Hey, please focus on the game!")
                return[]

        signal_position = tracker.get_slot("signal_position")
        is_activate_solved = tracker.get_slot("is_activate_solved")

        if not is_activate_solved:
            dispatcher.utter_message("You can't send anything at the moment")
            return[]
        

        if signal_position:
            if signal_position == 8:
                dispatcher.utter_message("Congratulations, brave astronaut! You've successfully aligned the satellite dish and sent a powerful distress signal to the coordinates Latitude: 52.1352507 and Longitude: 11.6388062. Your message has been received, and rescue ships are en route to your location. Help is on the way!")
                dispatcher.utter_message("As you stand by the communication console, the anxiety and intensity of the mission begin to fade. A sense of surreal clarity washes over you, and you suddenly realize the truth – it was all a vivid dream. You take a deep breath, relieved to be safely back in the realm of reality. The control panels, the navigation screen, the airlock door – all dissolve into the fading echoes of the dream. You find yourself waking up in your own comfortable bed, surrounded by the familiar comforts of your home.")
                return[SlotSet("is_game_over", True)]
            else:
                current_lives = tracker.get_slot("lives")
                if current_lives:
                    dispatcher.utter_message("Uh-oh, it seems there might have been a slight miscalculation. The distress signal you sent encountered interference and failed to reach its intended destination.")
                    dispatcher.utter_message(f"You have lost precious time and a life. You have {current_lives-1} lives left.")
                    if current_lives-1 <= 0:
                        dispatcher.utter_message(text=f"GAME OVER")
                        dispatcher.utter_message(text=f"If you want to play again please refresh the page.")
                        return[SlotSet("is_game_over", True)]
                    
                    return[SlotSet("lives", current_lives-1)]
        else:
            dispatcher.utter_message(f"Sorry I did not get it. Please rephrase your message")
        return []