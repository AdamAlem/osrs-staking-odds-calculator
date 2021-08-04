import gear

class Player:
    def __init__(self):
        #stats = [atk, str, def, hp]
        #bonuses = [[atkbonuses(stab/slash/crush)], [defbonuses(stab/slash/crush)], strbonus, wepspeed]
        self.stats, self.bonuses, self.weapon, self.armour = build_player()
    
        self.hp = self.stats[3]
        self.maxhit()
        self.speed = self.bonuses[-1]
        self.level = .325*self.stats[0] + .325*self.stats[1] + .25*self.stats[2] + .25*self.stats[3]
        
    def maxhit(self):
        eff_str = self.stats[1] + 8
        eff_str *= self.bonuses[2] + 64
        eff_str += 320
        eff_str /= 640
        self.max_hit = int(eff_str)
    
    def accuracy(self, otherdefbonus):
        atk_style = self.bonuses[0].index(max(self.bonuses[0]))
        atk_roll = int(self.stats[0] * (self.bonuses[0][atk_style]+64))
        def_roll = int(self.stats[2] * (otherdefbonus[atk_style]+64))
        if atk_roll > def_roll:
            return 1-((def_roll+2)/(2*(atk_roll)+1))
        else:
            return atk_roll/(2*(def_roll)+1)
    
    def changeWeapon(self):
        self.bonuses = [[self.bonuses[j][i] - gear.weapons[self.weapon][j][i] for i in range(3)] for j in range(2)]
        [self.bonuses.append(0) for i in range(2)]
        self.weapon = chooseWeapon()[1]
        self.bonuses = [[self.bonuses[j][i] + gear.weapons[self.weapon][j][i] for i in range(3)] for j in range(2)]
        [self.bonuses.append(gear.weapons[self.weapon][i-2]) for i in range(2)]
    
    def changeArmour(self):
        self.bonuses = [[self.bonuses[j][i] - gear.armour[self.armour][j][i] for i in range(3)] for j in range(2)]
        self.armour = chooseArmour()[1]
        self.bonuses = [[self.bonuses[j][i] + gear.armour[self.armour][j][i] for i in range(3)] for j in range(2)]
        [self.bonuses.append(gear.weapons[self.weapon][i-2]) for i in range(2)]
    
    def __repr__(self):
        return "Combat level: "+str(self.level)+" Weapon: "+self.weapon+" Armour: "+self.armour
        
def applyHit(hpvec, hitvec):
    old = [hp for hp in hpvec]
    hpvec = [0 for hp in hpvec]
    
    for i in range(len(hpvec)):
        for j in range(len(hitvec)):
            if i+j < len(hpvec)-1:
                hpvec[i+j] += old[i] * hitvec[j]
            else:
                hpvec[-1] += old[i] * hitvec[j]
    
    return hpvec

def Calc(p1, p2, food=[0, 0]):
    #Create hp vectors
    hpvec1 = [0] * (p1.hp+1+food[0])
    hpvec2 = [0] * (p2.hp+1+food[1])
    hpvec1[0] = 1
    hpvec2[0] = 1
    
    #Get accuracies
    p1accuracy = p1.accuracy(p2.bonuses[1])
    p2accuracy = p2.accuracy(p1.bonuses[1])
    #Create hit vectors
    hitvec1 = [0] * (p1.max_hit+1)
    hitvec2 = [0] * (p2.max_hit+1)
    hitvec1[0] = 1-p1accuracy
    hitvec2[0] = 1-p2accuracy
    hitvec1 = [hitvec1[i] + (p1accuracy)/(p1.max_hit+1) for i in range(len(hitvec1))]
    hitvec2 = [hitvec2[i] + (p2accuracy)/(p2.max_hit+1) for i in range(len(hitvec2))]
    p1odds = 0
    
    tick = 0
    while (1-hpvec1[-1]) * (1-hpvec2[-1]) > .0001: #Probability of no death
        tempdeath1 = hpvec1[-1]
        tempdeath2 = hpvec2[-1]
        
        if tick % p1.speed == 0:
            hpvec2 = applyHit(hpvec2, hitvec1) #p1 hits p2
        if tick % p2.speed == 0:
            hpvec1 = applyHit(hpvec1, hitvec2) #p2 hits p1
        
        d2 = hpvec2[-1] - tempdeath2 #Chance p2 dies this tick
        
        p1odds += (1-(hpvec1[-1]+tempdeath1)/2) * d2
        tick += 1
    p1odds *= 100
    p1odds = str("{:.2f}".format(p1odds))
    if p1odds < 50:
        betx = (1-p1odds)/p1odds
        betx = str("{:.6f}".format(betx))
        outstr = 'Fair staking odds: p2'+betx+'x p1'
    else:
        betx = p1odds/(1-p1odds)
        betx = str("{:.2f}".format(betx))
        outstr = 'Fair staking odds: p1'+betx+'x p2'.
    return "P1 has a "+p1odds+"% chance to win. "+outstr
        

def inputStats():
    print("Input character stats:")
    stats = [int(input("Attack:"))]
    stats.append(int(input("Strength:")))
    stats.append(int(input("Defence:")))
    stats.append(int(input("Hitpoints:")))
    return stats

def chooseWeapon():
    print("Choose a weapon")
    for i, wep in enumerate(gear.weapons.keys()):
        print (i+1, wep)
    wepindex = int(input("Select the weapon index you would like, or 0 for custom"))
    
    if wepindex > 0:
        wepbonus = [b for b in gear.weapons[list(gear.weapons)[wepindex-1]]]
        weaponname = list(gear.weapons)[wepindex-1]
    else:
        print("Input stab/slash/crush bonuses")
        bonuses = [[int(input("Stab"))], [0, 0, 0]]
        bonuses[0].append([int(input("Slash:"))])
        bonuses[0].append([int(input("Crush:"))])
        bonuses.append([int(input("Enter weapon strength bonus Ex:66 is dragon scim"))])
        bonuses.append([int(input("And finally ticks between attack Ex:4 is a scimitar, 5 is a longsword"))])
        weaponname = 'Custom'
    return wepbonus, weaponname

def chooseArmour():
    print("Choose an armour set")
    for i, arm in enumerate(gear.armour.keys()):
        print (i+1, arm)
    armindex = int(input("Select armour set index or 0 for custom"))
    
    if armindex > 0:
        armbonus = [b for b in gear.armour[list(gear.armour)[armindex-1]]]
        armourname = list(gear.armour)[armindex-1]
    else:
        print("Input stab/slash/crush defence bonuses")
        bonuses = [[0, 0, 0], [int(input('Stab:'))], 0, 0]
        bonuses[1].append([int(input("Slash:"))])
        bonuses[1].append([int(input("Crush:"))])
        armourname = 'Custom'
    return armbonus, armourname

def build_player():
    stats = inputStats()
    wepbonus, weaponname = chooseWeapon()
    armbonus, armourname = chooseArmour()
    wepbonus[:2] = [[wepbonus[j][i]+armbonus[j][i] for i in range(3)] for j in range(2)]
    return stats, wepbonus, weaponname, armourname
