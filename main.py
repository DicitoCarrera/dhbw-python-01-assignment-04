from dataclasses import dataclass
from typing import Callable


# Enum for Pokémon types (Water, Fire, Grass, Electric)
class PokemonType:
    WATER = "Water"
    FIRE = "Fire"
    GRASS = "Grass"
    ELECTRIC = "Electric"


# Type alias for Effectiveness function
Effectiveness = Callable[["Pokemon"], float]


# Health, Damage, and Level types
@dataclass(frozen=True)
class Health:
    value: int


@dataclass(frozen=True)
class Damage:
    value: int


@dataclass(frozen=True)
class Level:
    value: int


# Pokémon with encapsulated effectiveness logic
@dataclass(frozen=True)
class Pokemon:
    name: str
    p_type: str
    health: Health
    damage: Damage
    level: Level
    effectiveness: Effectiveness  # Effectiveness function specific to each Pokémon


# Effectiveness logic per Pokémon using match-case
def water_effectiveness(opponent: Pokemon) -> float:
    match opponent.p_type:
        case PokemonType.FIRE:
            return 2.0  # Water is effective against Fire
        case PokemonType.GRASS:
            return 0.5  # Water is weak against Grass
        case _:
            return 1.0  # Neutral against other types


def fire_effectiveness(opponent: Pokemon) -> float:
    match opponent.p_type:
        case PokemonType.GRASS:
            return 2.0  # Fire is effective against Grass
        case PokemonType.WATER:
            return 0.5  # Fire is weak against Water
        case _:
            return 1.0  # Neutral against other types


def grass_effectiveness(opponent: Pokemon) -> float:
    match opponent.p_type:
        case PokemonType.WATER:
            return 2.0  # Grass is effective against Water
        case PokemonType.FIRE:
            return 0.5  # Grass is weak against Fire
        case _:
            return 1.0  # Neutral against other types


def electric_effectiveness(opponent: Pokemon) -> float:
    match opponent.p_type:
        case PokemonType.WATER:
            return 2.0  # Electric is effective against Water
        case _:
            return 1.0  # Neutral against other types


# Battle function using Pokémon-specific effectiveness
def battle(p1: Pokemon, p2: Pokemon) -> tuple[Pokemon, Pokemon]:
    effectiveness1 = p1.effectiveness(p2)  # Use p1's effectiveness logic
    effectiveness2 = p2.effectiveness(p1)  # Use p2's effectiveness logic

    p1_damage = calculate_damage(damage=p1.damage, effectiveness=effectiveness1)
    p2_damage = calculate_damage(damage=p2.damage, effectiveness=effectiveness2)

    new_p1_health = Health(value=max(0, p1.health.value - p2_damage))
    new_p2_health = Health(value=max(0, p2.health.value - p1_damage))

    p1_after_battle = Pokemon(
        name=p1.name,
        p_type=p1.p_type,
        health=new_p1_health,
        damage=p1.damage,
        level=p1.level,
        effectiveness=p1.effectiveness,
    )

    p2_after_battle = Pokemon(
        name=p2.name,
        p_type=p2.p_type,
        health=new_p2_health,
        damage=p2.damage,
        level=p2.level,
        effectiveness=p2.effectiveness,
    )

    return p1_after_battle, p2_after_battle


# Damage calculation based on effectiveness
def calculate_damage(damage: Damage, effectiveness: float) -> int:
    return round(damage.value * effectiveness)


# Level up a Pokémon
def level_up(pokemon: Pokemon) -> Pokemon:
    new_level = Level(value=pokemon.level.value + 1)
    new_health = Health(value=pokemon.health.value + 10)
    new_damage = Damage(value=pokemon.damage.value + 5)

    return Pokemon(
        name=pokemon.name,
        p_type=pokemon.p_type,
        health=new_health,
        damage=new_damage,
        level=new_level,
        effectiveness=pokemon.effectiveness,
    )


# Main function to simulate the game
def main() -> None:
    # Example Pokémon with their effectiveness rules
    pikachu = Pokemon(
        name="Pikachu",
        p_type=PokemonType.ELECTRIC,
        health=Health(value=100),
        damage=Damage(value=20),
        level=Level(value=5),
        effectiveness=electric_effectiveness,
    )

    charizard = Pokemon(
        name="Charizard",
        p_type=PokemonType.FIRE,
        health=Health(value=150),
        damage=Damage(value=35),
        level=Level(value=10),
        effectiveness=fire_effectiveness,
    )

    p1_after_battle, p2_after_battle = battle(p1=pikachu, p2=charizard)

    print(p1_after_battle)
    print(p2_after_battle)

    # Leveling up Pikachu
    pikachu_leveled_up = level_up(pokemon=pikachu)

    print(pikachu_leveled_up)


if __name__ == "__main__":
    main()
