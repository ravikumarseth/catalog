from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, GameGenre, Game

engine = create_engine('sqlite:///games.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

Arcade = GameGenre(name="Arcade", description="Games which require the player to navigate a maze or other obstacle")
session.add(Arcade)
session.commit()

Shooter = GameGenre(name="Shooter", description="Where the main purpose is to fight using guns")
session.add(Shooter)
session.commit()

Strategy = GameGenre(name="Strategy", description=" Where the purpose is to strategize. You have an opponent with the same abilities as you, more or less, and to beat him, you must use your abilities in a much more tactical way")
session.add(Strategy)
session.commit()

Musical = GameGenre(name="Musical", description="Where music is usually played. To win, the players must match the rhythm of the music by pushing the right button combination until their opponents are unable to keep up with them")
session.add(Musical)
session.commit()

Simulation = GameGenre(name="Simulation", description="Where you must manage and develop fictitious business")
session.add(Simulation)
session.commit()

Puzzle = GameGenre(name="Puzzle", description="Where you must solve puzzles in order to progress through the levels")
session.add(Puzzle)
session.commit()

Party = GameGenre(name="Party", description="Mostly suitable for multiple players and social gatherings")
session.add(Party)
session.commit()

Platform = GameGenre(name="Platform", description="Where the player must jump onto various platforms to evade obstacles and reach their goal, these games are fairly linear most of the time with levels adhering to a simple A to B structure")
session.add(Platform)
session.commit()

Fighting = GameGenre(name="Fighting", description="Where two or more playable characters fight")
session.add(Fighting)
session.commit()

Racing = GameGenre(name="Racing", description=" Either in the first-person or third-person perspective, in which the player partakes in a racing competition with any type of land, air, or sea vehicles")
session.add(Racing)
session.commit()

Role_playing = GameGenre(name="Role-Playing", description="It is a game where the player plays a character, and goes around pretending to be a real person in a fictitious world")
session.add(Role_playing)
session.commit()

Sports = GameGenre(name="Sports", description="Games that simulate playing real-life sports")
session.add(Sports)
session.commit()

Survival_Horror = GameGenre(name="Survival_Horror", description="The player is placed in a horrifying situation of which they must escape")
session.add(Survival_Horror)
session.commit()

Stealth = GameGenre(name="Stealth", description="The player must proceed through an environment or complete an objective without being seen")
session.add(Stealth)
session.commit()

print "all added genre!!"
