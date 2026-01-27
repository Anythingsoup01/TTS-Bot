from managers.twitch_manager import Twitch_Manager

if __name__ == '__main__':
    twitch = Twitch_Manager()

    twitch.run()
    
    twitch.shutdown()
