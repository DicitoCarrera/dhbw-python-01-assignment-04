-- Enum for Pokémon types (Water, Fire, Grass, Electric)
data PokemonType = Water | Fire | Grass | Electric
  deriving (Show, Eq, Enum)

-- Health, Damage, and Level types
data Health = Health Int
  deriving (Show, Eq)

data Damage = Damage Int
  deriving (Show, Eq)

data Level = Level Int
  deriving (Show, Eq)

-- Type synonym for Effectiveness function
type Effectiveness = Pokemon -> Double

-- Pokémon with encapsulated effectiveness logic
data Pokemon = Pokemon
  { name :: String,
    pType :: PokemonType,
    health :: Health,
    damage :: Damage,
    level :: Level,
    effectiveness :: Effectiveness -- Use Effectiveness type alias here
  }
  deriving (Show, Eq)

-- Effectiveness logic per Pokémon
waterEffectiveness :: Effectiveness
waterEffectiveness opponent
  | pType opponent == Fire = 2.0 -- Water is effective against Fire
  | pType opponent == Grass = 0.5 -- Water is weak against Grass
  | otherwise = 1.0 -- Neutral against other types

fireEffectiveness :: Effectiveness
fireEffectiveness opponent
  | pType opponent == Grass = 2.0 -- Fire is effective against Grass
  | pType opponent == Water = 0.5 -- Fire is weak against Water
  | otherwise = 1.0 -- Neutral against other types

grassEffectiveness :: Effectiveness
grassEffectiveness opponent
  | pType opponent == Water = 2.0 -- Grass is effective against Water
  | pType opponent == Fire = 0.5 -- Grass is weak against Fire
  | otherwise = 1.0 -- Neutral against other types

electricEffectiveness :: Effectiveness
electricEffectiveness opponent
  | pType opponent == Water = 2.0 -- Electric is effective against Water
  | otherwise = 1.0 -- Neutral against other types

-- Example Pokémon with their effectiveness rules
pikachu :: Pokemon
pikachu =
  Pokemon
    { name = "Pikachu",
      pType = Electric,
      health = Health 100,
      damage = Damage 20,
      level = Level 5,
      effectiveness = electricEffectiveness
    }

charizard :: Pokemon
charizard =
  Pokemon
    { name = "Charizard",
      pType = Fire,
      health = Health 150,
      damage = Damage 35,
      level = Level 10,
      effectiveness = fireEffectiveness
    }

-- Battle function using Pokémon-specific effectiveness
battle :: Pokemon -> Pokemon -> (Pokemon, Pokemon)
battle p1 p2 =
  let effectiveness1 = effectiveness p1 p2 -- Use p1's effectiveness logic
      effectiveness2 = effectiveness p2 p1 -- Use p2's effectiveness logic
      p1Damage = calculateDamage (damage p1) effectiveness1
      p2Damage = calculateDamage (damage p2) effectiveness2
      newP1Health = Health (max 0 (healthValue (health p1) - p2Damage))
      newP2Health = Health (max 0 (healthValue (health p2) - p1Damage))
   in (p1 {health = newP1Health}, p2 {health = newP2Health})

-- Calculate the damage based on effectiveness
calculateDamage :: Damage -> Double -> Int
calculateDamage (Damage dmg) effectiveness = round (fromIntegral dmg * effectiveness)

-- Extract health value from Health type
healthValue :: Health -> Int
healthValue (Health h) = h

-- Level up a Pokémon
levelUp :: Pokemon -> Pokemon
levelUp p =
  let newLevel = Level (levelInt (level p) + 1)
      newHealth = Health (healthValue (health p) + 10)
      newDamage = Damage (damageValue (damage p) + 5)
   in p {level = newLevel, health = newHealth, damage = newDamage}

-- Extract the integer value from Level and Damage
levelInt :: Level -> Int
levelInt (Level l) = l

damageValue :: Damage -> Int
damageValue (Damage d) = d

-- Main function to simulate the game
main :: IO ()
main = do
  let (p1AfterBattle, p2AfterBattle) = battle pikachu charizard
  print p1AfterBattle
  print p2AfterBattle

  -- Leveling up Pikachu
  let pikachuLeveledUp = levelUp pikachu
  print pikachuLeveledUp
