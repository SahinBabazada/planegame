from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent, GiftEvent
import threading

class TikTokService:
    def __init__(self, planes, username):
        self.planes = planes
        self.running = True
        self.user_map = {}  # Maps user IDs to their assigned country numbers
        self.client = TikTokLiveClient(unique_id=username)  # TikTok username or unique ID

        # Register event handlers using event classes
        self.client.add_listener(CommentEvent, self.on_comment)
        self.client.add_listener(GiftEvent, self.on_gift)

    def start_service(self):
        """Start the TikTok service in a new thread."""
        thread = threading.Thread(target=self.listen_for_actions)
        thread.start()

    def listen_for_actions(self):
        """Listen for TikTok comments and gifts to perform actions in the game."""
        while self.running:
            try:
                self.client.run()  # Start listening to TikTok live events
            except Exception as e:
                print(f"Error in TikTok service: {e}")

    async def on_comment(self, event: CommentEvent):
        """Handle comment events from TikTok."""
        user_id = event.user.unique_id
        try:
            country_number = int(event.comment)
            if 1 <= country_number <= 4:
                print(f"Assigning user {event.user.nickname} to country number: {country_number}")
                self.user_map[user_id] = country_number
        except ValueError:
            print("Invalid comment content, not a number.")

    async def on_gift(self, event: GiftEvent):
        """Handle gift events from TikTok."""
        user_id = event.user.unique_id
        if user_id not in self.user_map:
            print(f"User {event.user.nickname} not assigned to any country yet.")
            return

        country_number = self.user_map[user_id]  # Get the user's assigned country number
        print(f"{event.user.nickname} sent {event.gift.name} x{event.gift.diamond_count}")

        gift_name = event.gift.name.lower()

        plane = self.planes[country_number - 1]  # Access the corresponding plane
        if gift_name == 'rose':
            print(f"Moving plane {country_number} to the right.")
            plane.move_right()
        elif gift_name == 'finger heart':
            print(f"Moving plane {country_number} to the right.")
            plane.move_right(newSpeed=10)
        elif gift_name == 'doughnut':
            print(f"Shooting torpedo from plane {country_number}.")
            plane.shoot_torpedo(width=60, height=30, speed=15, direction='right')

    def stop_service(self):
        """Stop the TikTok service."""
        self.running = False
        self.client.stop()

