# I Hate Documentation

Commands

    General:
        /start: start the robot
        /help: list commands
        /show: show the current board
        /register [passphrase] [OGL/GM] [House/Station] [OG/null]:
            register to play as an OGL/GM e.g.:
                /register G-4b=8Lh7vKZQ{-@ GM 1
                /register Yreby'#xZy~r&c?: OGL Strix 3

    OGLs:
        /points: view your OG's current points
        /position: view your House's current position
        /roll: roll the dice 
        /move: move 3 steps
        /sabo [House]: sabo another house 3 steps

    GMs:
        /addpoints [House] [OG] [points]: Add points to an OG (cannot subtract their points)

    Admin:
        /adminstartgame: Start the game
        /adminendgame: Pause the game
        /adminstartreg: Start Registration
        /adminstopreg: Stop Registration
        /adminview: View a House's Position and all its OG's points
        /adminsetpoints [House] [OG] [points]: Set an OG's points (can subtract their points)
        /adminsetpos [House] [position]: Set a House's position