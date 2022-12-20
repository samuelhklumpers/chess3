The global TODO list.
Note that there are more # TODO comments in some files.

The lower hanging fruit is marked with a +.
The harder goals are marked with a !.
Things like !? and +? mean a bit hard or easy.

- [ ] client
    - [ ] + layout/css
        - [ ] + add "next" button
    - [ ] graphics/command processing
        - [ ] !? classes for cards with writeable fields (e.g. print the current hp on the card)
        - [ ] + images
- [ ] server
    - [ ] + add cards to cards.json and default_stack.json
    - [ ] ! implement computing rules on Ruleset
        - [ ] e.g. UnitDefense(Compute) computes the defense of a unit, incorporating dynamic modifiers such as Eannean's skill
    - [ ] structure
        - [ ] + dp counter
        - [ ] !? queues
        - [ ] movement
        - [ ] combat
    - [ ] rules
        - [ ] implement "next" handling in appropriate places (e.g. next in deploying stops deploying) 
        - [ ] tile restrictions (defer)
        - [ ] action subturn
            - [ ] fix act <-> subact interaction
            - [x] draw cards
            - [ ] + gain energy
            - [ ] !? add energy microturn
            - [?] ! play cards
            - [ ] promote operators 
            - [ ] ! retreat operators
        - [ ] movement subturn
            - [ ] ! rotation mechanism
        - [ ] skill subturn
            - [ ] +? energy mechanism
            - [ ] !!! add skills
        - [ ] combat subturn
            - [ ] health/damage
            - [ ] !!! range+rotation mechanics
        - [ ] win condition