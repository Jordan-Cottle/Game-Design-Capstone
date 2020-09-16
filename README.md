# Combined Ai and Capstone Project: Starcorp

Starcorp is a space themed mmorpg/rts. Players join the galaxy as CEOs of a newly founded company and vie for control over limited resources.

Since players assume the role of a CEO, the game's mechanics will focus primarily on resource management. The galaxy is a dangerous place though, so
security will also be a concern if large operations are going to be sustainable. Not only will other players have the opportunity to raid production facilities,
but the other entities in the universe may not appreciate having their planets covered in industrial zones.

## Setting/Theme
As a space themed game, Starcorp will take place on a galactic scale. Initially players will start on Earth for a tutorial, but limited space and resources there will force
players to migrate off the planet, and eventually to other solar systems.

## Core Gameplay Mechanics

### Economics
Starcorp will feature an engaging economic model that will simultaneously require players to cooperate to maintain large cities and compete for limited space and resources.

Cities will form the backbone of the Starcorp economy as they provide a reliable market for players to sell their goods. As more goods are consumed in a city, the city will grow
and require even more goods. However, the land on each planet can only sustain a certain level of resource generation. As more and more players join the game, competition for
the limited resources will force companies to find alternative locations to continue expanding production to meet continually rising demands.

### Politics
In addition to the economic contention, the government of cities, planets, and systems will be run by players themselves. Their influence in the respective zones will contribute
to their political power, which they can use to vote for a specific leader (including themselves). Large players will be enticed to gather their strength and make an attempt
at one of the ruling seats, turning their economic power into political power.

Players who control a seat of power will have the opportunity to set laws for their zone of control that allow them to restrict certain markets or collect taxes on imports/exports.

### Military
In the depths of space, the only law is the one you can enforce yourself. With so many valuable goods being transported across large distances, it would be silly to leave
them without an escort. Companies in Starcorp are responsible for securing their own assets against theft and destruction.

In Starcorp, what starts off as a simple security patrol can quickly turn into a full scale military operation. Players will have the opportunity to employ an array of defensive
and offensive weapons to both protect and "acquire" their assets. 

### Exploration
The Earth alone is only capable of supplying so many resources. In Starcorp the depths of space are available for exploitation, as long as you can make it there and back again
safely. Other players will also be attempting to secure their own trade routes, and may not always be welcome to additional competition in their area.

In Starcorp players won't be the only entities in the universe. There are also other factions that have very little interest in the survival of the human species. Alien races may
not be as welcoming to player advances as the empty planets found in the solar system. Once provoked, the alien races will strike back and take much more interest in the actions
of specific players in their territories. How players handle them is an individual choice. Alien alliances may provide useful tech and exotic good, while making enemies may free
up land for additional factories.

## Player Interface
Players directly control their CEO by expending action points that accrue over time to perform actions. Other units/mercenaries that are under a company's control can be
issued commands that they execute over time. Outside of the player's themselves, the world will play out actions in discrete turns that happen at regular intervals.

The game space will be divided into tiles that will have different attributes that make them more desireable for different industries. Tiles are collected into regions that
may make up a planet or section of space. These regions are then also collected together to form larger systems.

Resources are primarily found on the surfaces of planets. They can be gathered by players with the proper equipment, or by facilities that gather over time.

In addition to constructing buildings on planets, space stations may also be built to save space and provide more convenient locations for things. Some things like advanced
ship construction can only be done in space.

## Technical details
Player client will be implemented in Unity. Server will be implemented as a REST api written in python using flask.

All unit movement in the game will be driven by a pathfinding algorithm. Cities will also have forces automated to defend against aggressors.

To provide a more interesting challenge, raiders and other enemies will appear in the unsettled areas of the universe to attack players. These server controlled factions will be
driven by an ai to manage their troops and target vulnerable facilities.

