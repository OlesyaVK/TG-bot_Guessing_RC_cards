# TG-bot_Guessing_RC_cards

**Core Components**:
- `states.py`: FSM states (waiting_for_card, waiting_for_attempts, etc.)
- `data/cards.py`: CARDS_DATA dictionary with character collections
- `handlers/`: 
  - `commands.py`: /start, /join 
  - `callbacks.py`: Card selection flow
  - `game.py`: Game session logic (active_games dict)

**Security**:
- Token stored in `.env` (gitignored)
- Required packages in `requirements.txt` (aiogram, python-dotenv)

**Key Patterns**:
1. State-driven conversation flow
2. Inline keyboard navigation
3. Multiplayer turn management via active_games

**Deployment Notes**:
- Configured for polling (alternative webhook setup available)
- Shared game state survives restarts (MemoryStorage)
