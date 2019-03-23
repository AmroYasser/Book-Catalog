from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Categories, Items


engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create a dummy user
user1 = User(name="Mr Liberian", email="amr@udacityfsnd.com")
session.add(user1)
session.commit()

# Create book categories
category1 = Categories(name="Autobiographies")
session.add(category1)
session.commit()

category2 = Categories(name="Economics")
session.add(category2)
session.commit()

category3 = Categories(name="History")
session.add(category3)
session.commit()

category4 = Categories(name="Literature")
session.add(category4)
session.commit()

category5 = Categories(name="Philosophy")
session.add(category5)
session.commit()

category6 = Categories(name="MISC.")
session.add(category6)
session.commit()

# Add book items into each category
item1 = Items(
        user=user1,
        category=category1,
        name="Mein Kampf",
        author="Adolf Hitler",
        description="Madman, tyrant, animal - history has given Adolf Hitler many names. In Mein Kampf (My Struggle),\
         often called the Nazi bible, Hitler describes his life, frustrations, ideals, and dreams. ")

session.add(item1)
session.commit()

item2 = Items(
        user=user1,
        category=category1,
        name="Surely You're Joking, Mr. Feynman!",
        author="Richard P. Feynman",
        description="Richard Feynman (1918-1988), winner of the Nobel Prize in physics, thrived on outrageous\
         adventures. Here he recounts in his inimitable voice his experience trading ideas on atomic physics with\
         Einstein and Bohr and ideas on gambling with Nick the Greek; cracking the uncrackable safes guarding the most\
         deeply held nuclear secrets; painting a naked female toreador - and much else of an eyebrow-raising nature")

session.add(item2)
session.commit()

item3 = Items(
        user=user1,
        category=category1,
        name="The Autobiography of Malcolm X",
        author="Malcolm X and Alex Haley",
        description="Not only is this an enormously important record of the Civil Rights Movement in America, but also\
         the scintillating story of a man who refused to allow anyone to tell him who or what he was.")

session.add(item3)
session.commit()

item4 = Items(
        user=user1,
        category=category2,
        name="Freakonomics",
        author="Stephen Dubner and Steven Levitt",
        description="Freakonomics establishes this unconventional premise: If morality represents how we would like the\
         world to work, then economics represents how it actually does work. It is true that readers of this book will\
          be armed with enough riddles and stories to last a thousand cocktail parties. But Freakonomics can provide\
           more than that. It will literally redefine the way we view the modern world.	")

session.add(item4)
session.commit()

item5 = Items(
        user=user1,
        category=category2,
        name="The Communist Manifesto",
        author="Karl Marx",
        description="Originally published on the eve of the 1848 European revolutions, The Communist Manifesto is a\
         condensed and incisive account of the worldview Marx and Engels developed during their hectic intellectual and\
          political collaboration. Formulating the principles of dialectical materialism, they believed that labor\
           creates wealth, hence capitalism is exploitive and antithetical to freedom.	")

session.add(item5)
session.commit()

item6 = Items(
        user=user1,
        category=category3,
        name="Civilization and Capitalism",
        author="Fernand Braudel",
        description="By examining in detail the material life of pre-industrial peoples around the world, Fernand\
         Braudel significantly changed the way historians view their subject. Volume I describes food and drink, dress\
          and housing, demography and family structure, energy and technology, money and credit, and\
           the growth of towns.")

session.add(item6)
session.commit()

item7 = Items(
        user=user1,
        category=category3,
        name="The Collapse of Complex Societies",
        author="Joseph Tainter",
        description="Twenty-four examples of societal collapse help develop a new theory to account for their\
         breakdown. Detailed studies of the Roman, Mayan and Cacoan collapses clarify the processes of disintegration.")

session.add(item7)
session.commit()

item8 = Items(
        user=user1,
        category=category4,
        name="Crime and Punishment",
        author="Fyodor Dostoyevsky",
        description="Raskolnikov, a destitute and desperate former student, wanders through the slums of St Petersburg\
         and commits a random murder without remorse or regret. He imagines himself to be a great man, a Napoleon:\
          acting for a higher purpose beyond conventional moral law. But as he embarks on a dangerous game of cat and\
           mouse with a suspicious police investigator")

session.add(item8)
session.commit()

item9 = Items(
        user=user1,
        category=category4,
        name="War and Peace",
        author="Leo Tolstoy",
        description="Tolstoy's epic masterpiece intertwines the lives of private and public individuals during the\
         time of the Napoleonic wars and the French invasion of Russia. The fortunes of the Rostovs and the\
          Bolkonskys, of Pierre, Natasha, and Andrei, are intimately connected with the national history that is played\
           out in parallel with their lives.")

session.add(item9)
session.commit()

item10 = Items(
        user=user1,
        category=category4,
        name="Cairo Trilogy",
        author="Naguib Mahfouz",
        description="The Cairo Trilogy is a trilogy of novels written by the Egyptian novelist and Nobel Prize winner\
         Naguib Mahfouz, and one of the prime works of his literary career. The three novels are, in order: Palace\
          Walk Palace of Desire Sugar Street ")

session.add(item10)
session.commit()

item11 = Items(
        user=user1,
        category=category4,
        name="The Old Man and the Sea",
        author="Ernest Hemingway",
        description="Set in the Gulf Stream off the coast of Havana, Hemingway's magnificent fable is the story of an\
         old man, a young boy and a giant fish. In a perfectly crafted story, which won for Hemingway the Nobel Prize\
          for Literature, is a unique and timeless vision of the beauty and grief of man's challenge to the elements\
           in which he lives.")

session.add(item11)
session.commit()

item12 = Items(
        user=user1,
        category=category5,
        name="Beyond Good and Evil",
        author="Friedrich Nietzche",
        description='This work dramatically rejects the tradition of Western thought with its notions of truth and God,\
         good and evil. Nietzsche demonstrates that the Christian world is steeped in a false piety and infected with\
          a "slave morality." With wit and energy, he turns from this critique to a philosophy that celebrates the\
           present and demands that the individual imposes their own "will to power" upon the world.')

session.add(item12)
session.commit()

item13 = Items(
        user=user1,
        category=category5,
        name="On the Taboo Against Knowing Who You Are",
        author="Alan Watts",
        description="Modern Western culture and technology is inextricably tied to the belief in the existence of a\
         self as a separate ego, separated from and in conflict with the rest of the world. In this classic book, Watts\
          provides a lucid and simple presentation of an alternative view based on Hindi and Vedantic philosophy.")

session.add(item13)
session.commit()

item14 = Items(
        user=user1,
        category=category6,
        name="The Prince",
        author="Niccolo Machiavelli",
        description="The original blueprint for realpolitik, The Prince shocked sixteenth-century Europe with its\
         advocacy of ruthless tactics for gaining absolute power and its abandonment of conventional morality.")

session.add(item14)
session.commit()

item15 = Items(
        user=user1,
        category=category6,
        name="The Chomsky Reader",
        author="Noam Chomsky",
        description="The political and linguistic writings of America's leading dissident intellectual. He relates his\
         political ideals to his theories about language.")

session.add(item15)
session.commit()

item16 = Items(
        user=user1,
        category=category6,
        name="The Art of War",
        author="Sun Tzu",
        description="The Art of War is an ancient Chinese military treatise dating from the Late Spring and Autumn\
         Period. The work, which is attributed to the ancient Chinese military strategist Sun Tzu, is composed of 13\
          chapters. Each one is devoted to an aspect of warfare and how it applies to military strategy and tactics.")

session.add(item16)
session.commit()

item17 = Items(
        user=user1,
        category=category6,
        name="The Art of Deception",
        author="Kevin Mitnick",
        description="Social engineering. Part of the book is composed of real stories, and examples\
         of how social engineering can be combined with hacking. All, or nearly all, of the examples are fictional,\
          but quite plausible.")

session.add(item17)
session.commit()

print("Content added successfully!")